FROM python:3.12-slim
WORKDIR /bot
COPY . .
RUN mkdir -p uploads
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]