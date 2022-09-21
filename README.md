# recipe-finder

## Download the source data

This appliation uses the data that is available on Kaggle [here](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/metadata). It was scraped from Food.com using Beautiful Soup.

Citation: 
Shuyang Li. (2019). <i>Food.com Recipes and Interactions</i> [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/783630


To use this data, extract it to the /data folder.

## Common Commands

Set up environment: `poetry install`
Run JupyterLab: `jupyter lab`
Lint: `poetry run pre-commit`
Test: `poetry run python -m pytest`
Local env: `poetry install --without pyspark`

`docker-compose build && docker-compose up -d` then navigate to http://<docker_url>:8888/lab
