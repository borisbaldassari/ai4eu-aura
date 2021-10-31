
IMAGES="edf_databroker_train"
#IMAGES="aura_dataprep aura_ml_trainer edf_databroker_predict edf_databroker_train"

echo "This script is not ready yet. Exiting."
exit

echo "# Building all docker images."

for img in $IMAGES; do 
    echo "* Preparing [$img]"
    echo "  - Copying data samples from $img/data/"
    cp ../data/ $img/
    echo "  - Copying scripts to $img/scripts/"
    cp ../src/scripts/ $img/
    img_name="bbaldassari/$img"
    echo "  - Building image [$img_name]"
    docker build $img -t $img_name
done
    
