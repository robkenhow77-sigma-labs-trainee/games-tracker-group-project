FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY epic_extract.py .

COPY get_rating.gql .

COPY query_all.gql .

COPY epic_transform.py .

COPY epic_load.py .

COPY epic_load_functions.py .

COPY epic_pipeline.py .

CMD ["epic_pipeline.lambda_handler"]