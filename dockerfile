FROM python:3.12-slim
WORKDIR /bot
COPY . .
RUN mkdir -p uploads
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
CMD ["python3", "-u", "main.py"]