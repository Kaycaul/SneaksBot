FROM python:3.12-slim
# install ffmpeg (very slow)
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
# setup env
WORKDIR /bot
RUN mkdir -p uploads
# install modules (slow)
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy any new code
COPY . .
# run the bot
CMD ["python3", "-u", "main.py"]