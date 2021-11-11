
echo "Using flake8 to check Python code"
flake8 ./src/*/*.py
echo "Using black to check Python code"
black --check ./src/*/*.py
echo "Using flake8 to check tests on src/"
pytest --cov=./src/ ./src
#--ignore-glob='*_pb2*' ./
