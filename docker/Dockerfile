ARG FROM_IMAGE_NAME=nvcr.io/nvidia/pytorch:21.05-py3
FROM ${FROM_IMAGE_NAME}

ENV PYTHONPATH /app`
WORKDIR /app
ADD ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .                  