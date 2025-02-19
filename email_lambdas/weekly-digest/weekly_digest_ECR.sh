aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
docker build -t c15-play-steam-weekly-email . --platform="linux/amd64" --provenance=False
docker tag c15-play-steam-weekly-email:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c15-play-steam-weekly-email:latest
docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c15-play-steam-weekly-email:latest