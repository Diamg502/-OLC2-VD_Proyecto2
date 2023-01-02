FROM python:3.8-alpine


WORKDIR /server
COPY . .


RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install flask
RUN pip install flask-cors 
RUN pip install waitress 

EXPOSE 5000

CMD ["python", "app/main.py"]
