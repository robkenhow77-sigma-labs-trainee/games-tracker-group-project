source .env
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -U $DB_USERNAME -d $DB_NAME -p $DB_PORT 