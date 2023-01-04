FROM python:3.10.9


WORKDIR /server
COPY . .


RUN /usr/local/bin/python -m pip install --upgrade pip
ADD requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app/main.py"]
