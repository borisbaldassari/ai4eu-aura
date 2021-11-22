"""
Train a Machine Learning model from a dataset.

This script imports ml_dataset (with specific time window, quality and
consensus, train as model and uploads artificts and metrics to MLFlow.

This file can also be imported as a module and contains the following
fonctions:

    * compute_metrics - for a model, X and y, computes and uploads metrics and
    graphs to analyse the model to MLFlow
    * train_model - From a DataFrame, trains a Random Forest Classifier with
    grid search and exports it with metrics in MLFlow
    * main - the main function of the script
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import os
import sys

from joblib import dump
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, recall_score,\
                            roc_auc_score, precision_score,\
                            confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from typing import List

sys.path.append('.')
from src.usecase.utilities import convert_args_to_dict

OUTPUT_FOLDER = 'output/model'
MODEL_PARAM = {
    'model': RandomForestClassifier(),
    'grid_parameters': {
        'min_samples_leaf': np.arange(1, 5, 1),
        'max_depth': np.arange(11, 16, 1),
        'max_features': ['auto'],
        'n_estimators': np.arange(15, 20, 1)}}


def compute_metrics(prefix: str,
                    y_pred: np.array,
                    y_true: np.array,
                    results_dict: dict,
                    output_folder: str = OUTPUT_FOLDER,
                    total_seconds=None) -> dict:
    """Compute and log metrics in MLFlow.

    From a model, features X, targets y_true, computes several metrics and
    upload them to ML Flow

    Parameters
    ----------
    model :
        Sklearn model to evaluate
    X : np.array
        Explicative features
    y_pred : np.array
        Target data
    """
    try:
        results_dict[f'{prefix}_Accuracy'] = accuracy_score(y_true, y_pred)
        results_dict[f'{prefix}_f1-score'] = f1_score(y_true, y_pred)
        results_dict[f'{prefix}_Recall'] = recall_score(y_true, y_pred)
        results_dict[f'{prefix}_precision'] = precision_score(y_true, y_pred)
    except TypeError:
        pass

    cm = confusion_matrix(y_true, y_pred)

    try:
        tn, fp, fn, tp = cm.ravel()
        results_dict[f'{prefix}_tp'] = tn
        results_dict[f'{prefix}_fp'] = fp
        results_dict[f'{prefix}_fn'] = fn
        results_dict[f'{prefix}_tp'] = tp
        results_dict[f'{prefix}_tp_rate'] = tn/np.sum(cm)
        results_dict[f'{prefix}_fp_rate'] = fp/np.sum(cm)
        results_dict[f'{prefix}_fn_rate'] = fn/np.sum(cm)
        results_dict[f'{prefix}_tp_rate'] = tp/np.sum(cm)

    except ValueError:
        print('cannot compute metrics')
    except TypeError:
        pass

    try:
        results_dict[f'{prefix}_ROC_AUC_score'] = roc_auc_score(y_true, y_pred)

    except ValueError:
        print('cannot compute ROC_AUC_score')
    except TypeError:
        pass

    try:
        titles_options = [(f'{prefix} - Confusion Matrix', None),
                          (f'{prefix} - Normalized Confusion Matrix', 'true')]
        for title, normalize in titles_options:

            if normalize is None:
                cm_disp = np.round(cm, 0)
            else:
                cm_disp = np.round(cm/np.sum(cm.ravel()), 2)

            disp = ConfusionMatrixDisplay(confusion_matrix=cm_disp,
                                          display_labels=[0, 1])
            disp = disp.plot(cmap=plt.cm.Blues)
            disp.ax_.set_title(title)
            temp_name = f'{output_folder}/{title}.png'
            plt.savefig(temp_name)

        if total_seconds is not None:
            titles_options = [
                (f'{prefix} - Confusion Matrix Minutes', None, 'minutes'),
                (f'{prefix} - Confusion Matrix Seconds', None, 'seconds')]

            for title, normalize, time_unit in titles_options:

                if time_unit == 'minutes':
                    cm_disp = np.round(
                        cm*total_seconds/(60*np.sum(cm.ravel())), 2)
                else:
                    cm_disp = np.round(
                        cm*total_seconds/(np.sum(cm.ravel())), 2)

                disp = ConfusionMatrixDisplay(confusion_matrix=cm_disp,
                                              display_labels=[0, 1])
                disp = disp.plot(cmap=plt.cm.Blues)
                disp.ax_.set_title(title)
                temp_name = f'{output_folder}/{title}.png'
                plt.savefig(temp_name)

    except ValueError:
        print('cannot generate confusion matrices')

    except TypeError:
        pass

    return results_dict


def clean_ml_dataset(df_ml: pd.DataFrame,
                     target_treshold: float = 0.5) -> pd.DataFrame:
    """
    Clean ml dataset before pre-processing and model training.

    parameters
    ----------
    df_ml : pd.DataFrame
        ML Dataset to clean
    target_treshold : float
        Create binary target accord to a treshold of value

    returns
    -------
    df_ml : pd.DataFrame
        The clean ml dataset
    """
    print(f'Lines before Nan removal : {df_ml.shape[0]}')
    df_ml = df_ml.dropna()
    print(f'Lines after Nan removal : {df_ml.shape[0]}')

    df_ml['label'] = df_ml['label'].apply(
        lambda x: 1 if x >= target_treshold else 0)

    return df_ml


def train_model(ml_dataset_path: str,
                model_param: dict = MODEL_PARAM,
                output_folder: str = OUTPUT_FOLDER) -> str:
    """
    Machine Learning training pipeline.

    parameters
    ----------
    ml_dataset_path : str
        The path to ML dataset
    model_param: dict
        Parameters for the grisearch: model and hyper-parameters
    output_folder : str
        output for model and performance log
    """

    df_ml = pd.read_csv(ml_dataset_path)
    df_ml = clean_ml_dataset(df_ml, target_treshold=0.5)

    X = df_ml.iloc[:, :-1]
    y = df_ml.iloc[:, -1]

    # Making train and test variables
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    # Convertion of pandas DataFrames to numpy arrays
    # before using scikit-learn

    X_train = X_train.values
    X_test = X_test.values
    y_train = y_train.values
    y_test = y_test.values

    # Model Training
    grid_search = GridSearchCV(estimator=model_param['model'],
                               param_grid=model_param['grid_parameters'],
                               scoring='f1',
                               cv=5,
                               verbose=5,
                               n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Preparing data for performance assessement
    y_train_pred = grid_search.predict(X_train)
    y_test_pred = grid_search.predict(X_test)

    # Model and performance logging
    results_dict = {}
    os.makedirs(output_folder, exist_ok=True)

    dump(grid_search, f'{output_folder}/ml_model.pkl')

    grid_search_dict = grid_search.best_params_

    # Converting np.int64 to int for later json export
    for key in grid_search_dict.keys():
        if type(grid_search_dict[key]) == np.int64:
            grid_search_dict[key] = int(grid_search_dict[key])

    results_dict.update({'grid_search_param': grid_search_dict})

    results_dict = compute_metrics(
        'train',
        y_pred=y_train_pred,
        y_true=y_train,
        results_dict=results_dict,
        output_folder=output_folder
    )
    results_dict = compute_metrics(
        'test',
        y_pred=y_test_pred,
        y_true=y_test,
        results_dict=results_dict,
        output_folder=output_folder
    )

    # Converting int64 values to int for proper json export
    for key in results_dict.keys():
        if type(results_dict[key]) is np.int64:
            results_dict[key] = int(results_dict[key])

    # Export performance report
    with open(f'{output_folder}/ml_model_result.json', 'w') as fp:
        json.dump(results_dict, fp)


def parse_train_model_args(args_to_parse: List[str]) -> argparse.Namespace:
    """
    Parse arguments for adaptable input.

    parameters
    ----------
    args_to_parse : List[str]
        List of the element to parse. Should be sys.argv[1:] if args are
        inputed via CLI

    returns
    -------
    args : argparse.Namespace
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description='CLI parameter input')
    parser.add_argument('--ml-dataset-path',
                        dest='ml_dataset_path',
                        required=True)
    parser.add_argument('--output-folder',
                        dest='output_folder')
    args = parser.parse_args(args_to_parse)

    return args


if __name__ == '__main__':

    args = parse_train_model_args(sys.argv[1:])
    args_dict = convert_args_to_dict(args)
    train_model(**args_dict)
