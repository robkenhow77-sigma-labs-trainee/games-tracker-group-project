FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY dashboard.py .

COPY logo.png .

CMD ["streamlit run dashboard.py"]