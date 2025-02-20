<img src="https://raw.githubusercontent.com/robkenhow77-sigma-labs-trainee/games-tracker-group-project/refs/heads/main/dashboard/logo.png" alt="Logo" style="width:25%; height:auto;">

# Dashboard

This folder contains all files related to running the streamlit dashboard. This is ultimately what the 'website' is, it is this dashboard hosted on AWS FARGATE.

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

`dashboard.py` contains all code related to running the dashboard. This can be run locally by typing `streamlit run dashboard.py`.

All files within the `pages` folder relate to the specific pages of the dashboard.