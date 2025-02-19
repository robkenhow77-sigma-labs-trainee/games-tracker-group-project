FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY weekly_digest.py .

CMD ["weekly_digest.lambda_handler"]