FROM python:latest
WORKDIR /bot
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]