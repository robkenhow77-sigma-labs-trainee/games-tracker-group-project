<img src="https://raw.githubusercontent.com/robkenhow77-sigma-labs-trainee/games-tracker-group-project/refs/heads/main/dashboard/logo.png" alt="Logo" style="width:25%; height:auto;">

# GOG Pipeline

An ETL pipeline takes data, cleans it and then inserts it into a database. The `gog_pipeline.py` file will run the entire pipeline.

## How to use

This folder will require a `.env`. See the [main README](../../README.md) to see how to make a `.env` and add the following information:

```
DB_HOST="[Your database host url]"
DB_PORT=[Your database access port]
DB_PASSWORD="[Your database password]"
DB_USERNAME="[Your database username]"
DB_NAME="[Your database name]"
```

## Files

The files are broken down into three main types: `test_x.py files`, `x.py` files, `x.sh` files.

`x.py` files such as `gog_extract.py` contain all the code related to the ETL process (in this case extracting data from the GOG website). Run with `python3 x.py`.

`test_x.py` files such as `test_gog_transform.py` contain all unit tests for a file (in this case `gog_transform.py`). Run `pytest` in this folder to run all unit tests and ensure the code is working.

`x.sh` file such as `gog_pipeline_ECR.sh` contain bash scripts that exist largely for convenience (in this case automatic pushing a dockerised image of the gog_pipeline to the ECR). You should read each shell script and change it to suit your needs. Run with `bash x.sh`.