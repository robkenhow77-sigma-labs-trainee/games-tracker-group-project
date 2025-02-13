# games-tracker-group-project

### database/

- Type `vim .env` and then add the following by going into edit mode by pressing `i`:

```
DB_HOST=[Your database host address]
DB_NAME=[Your database name]
DB_PASSWORD=[Your database password]
DB_PORT=[Your database access port]
DB_USERNAME=[Your database username]
```

followed by `esc` then type `wq!` to save those changes and quit out of vim.

#### connect_to_db.sh

- Contains a bash script that will connect you to your database.
- Run with `bash connect_to_db.sh`

#### main.py

- Currently empty

#### README.md

- Contains information relevant to the folder

#### requirements.txt

- A list of libraries required for using the scripts in this folder
- In a [venv](https://docs.python.org/3/library/venv.html) (use `python3 -m venv .venv` followed by `source .venv/bin/activate`) run `pip install -r requirements.txt` to install them.

#### reset_database.sh

- WARNING: ONLY RUN THIS IF YOU KNOW WHAT YOU ARE DOING.
- Contains a bash script that will connect you to your database and remove all data.
- Run with `bash reset_database.sh`

#### schema.sql

- Contains the postgres SQL required to set up the database as the script is expecting.
- Running reset_database.sh will seed the database with this architecture.