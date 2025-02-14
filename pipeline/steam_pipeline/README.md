# games-tracker-group-project

## Steam ETL pipeline

### Python Files in ETL process

#### steam_extract.py

- Scrapes the steam store page for games released today.
- Can specify a target date to scrape until that date is reached. The script will scroll through the page 100 times.
- If more than 100 scrolls is needed there is a comment pointing out the number to change to the desired scrolls.
- Formats the data of all the games extracted in the form of a list of dictionaries.

#### steam_transform.py

- Takes the data from steam_extract.py and cleans it.
- Removes all erroneous data and formats all correct data into the form required by the database

#### steam_load.py

- Takes the cleaned data from steam_transform.py
- Uploads it into our database successfully

#### steam_pipeline.py

- Calls the functions from steam_extract, steam_transform and steam_load
- Automates the ETL process in one file

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

### Bash Scripts in the folder

#### run_extract.sh

- Runs the steam_extract file with all logging sent a folder that will be created.
- Run with `bash run_extract.sh`

#### run_month.sh

- Runs the steam_extract file with all logging sent a folder that will be created. Will extract all games between today and the 11th of January 2025.
- Run with `bash run_month.sh`

#### test.sh

- Runs `pytest` including outputting the test coverage.
- Run with `bash test.sh`

### Testing Files

#### test_steam_extract.py

- Contains all tests related to the steam_extract file.
- Run `pytest` to see the test output.

#### test_steam_transform.py

- Contains all tests related to the steam_transform file.
- Run `pytest` to see the test output.

#### test_steam_load.py

- Contains all tests related to the steam_load file.
- Run `pytest` to see the test output.
