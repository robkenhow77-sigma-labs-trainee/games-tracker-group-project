# games-tracker-group-project

### pipeline/

#### extract_epic.py

- Scrapes the epic game store page for games released today.

#### extract_steam.py

- Scrapes the steam store page for games released today.
- Can specify a target date to scrape until that date is reached. The script will scroll through the page 100 times.
- If more than 100 scrolls is needed there is a comment pointing out the number to change to the desired scrolls.
- Formats the data of all the games extracted in the form of a list of dictionaries.

#### extract.py

- Currently empty

#### load.py

- Currently empty

#### main.py

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

#### run_extract.sh

- Runs the steam_extract file with all logging sent a folder that will be created.
- Run with `bash run_extract.sh`

#### run_month.sh

- Runs the steam_extract file with all logging sent a folder that will be created. Will extract all games between today and the 11th of January 2025.
- Run with `bash run_month.sh`

#### test_extract.py

- Contains all tests related to the steam_extract file.
- Run `pytest` to see the test output.

#### test_transform.py

- Contains all tests related to the transform file.
- Run `pytest` to see the test output.

#### test.sh

- Runs `pytest` including outputting the test coverage.
- Run with `bash test.sh`

#### transform.py

- Takes the data from steam_extract.py and cleans it.
- Removes all erroneous data and formats all correct data into the form required by the database