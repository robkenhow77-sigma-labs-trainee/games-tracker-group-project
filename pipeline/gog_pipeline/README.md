# games-tracker-group-project

## GOG Store Pipeline

### Python Files in ETL process

#### gog_extract.py

- Scrapes the GOG store page for games released today.
- Formats the data of all the games extracted in the form of a list of dictionaries.

#### gog_transform.py

- Takes the data from gog_extract.py and cleans it.
- Removes all erroneous data and formats all correct data into the form required by the database

#### gog_load.py

- Takes the cleaned data from gog_transform.py
- Uploads it into our database successfully

#### gog_pipeline.py

- Calls the functions from steam_extract, gog_transform and gog_load
- Automates the ETL process in one file

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

### Bash Scripts in the folder

#### run_extract.sh

- Runs the gog_extract file with all logging sent a folder that will be created.
- Run with `bash run_extract.sh`

#### run_month.sh

- Runs the gog_extract file with all logging sent a folder that will be created. Will extract all games between today and the 11th of January 2025.
- Run with `bash run_month.sh`

#### test.sh

- Runs `pytest` including outputting the test coverage.
- Run with `bash test.sh`

### Testing Files

#### test_gog_extract.py

- Contains all tests related to the gog_extract file.
- Run `pytest` to see the test output.

#### test_gog_transform.py

- Contains all tests related to the gog_transform file.
- Run `pytest` to see the test output.

#### test_gog_load.py

- Contains all tests related to the gog_load file.
- Run `pytest` to see the test output.