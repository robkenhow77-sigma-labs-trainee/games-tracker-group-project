FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY marketplace.py .

RUN mkdir pages 

COPY pages/analytics.py pages

COPY pages/game_developers.py pages

COPY pages/game_publishers.py pages

COPY pages/games.py pages

COPY pages/platforms.py pages

COPY pages/subscribe.py pages

COPY logo.png .

ENTRYPOINT ["streamlit", "run", "marketplace.py", "--server.port=80", "--server.address=0.0.0.0"]
