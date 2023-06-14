ARG FROM_IMAGE_NAME=nvcr.io/nvidia/pytorch:21.05-py3
FROM ${FROM_IMAGE_NAME}

ENV PYTHONPATH /app
WORKDIR /app
ADD ./requirements.txt .
RUN apt-get update && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive TZ=Europe/Warsaw apt-get -y install tzdata
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
	alsa-utils \
	libportaudio2 \
	libportaudiocpp0 \
	portaudio19-dev \
	ffmpeg \
	dialog \
	apt-utils \
	libasound-dev 

RUN pip install -r requirements.txt