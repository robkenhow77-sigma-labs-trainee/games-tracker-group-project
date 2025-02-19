source .env
docker build -t send_emails .  
docker run -p 9002:8080 --env-file .env send_emails
