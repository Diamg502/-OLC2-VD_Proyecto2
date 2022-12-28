FROM python


WORKDIR /server
COPY . .


RUN D:/Diego/USAC/2022/Diciembre/Compiladores 2/github/-OLC2-VD_Proyecto2/python -m pip install --upgrade pip
RUN pip install flask
RUN pip install flask-cors 
RUN pip install waitress 

EXPOSE 5800

CMD ["python", "app.py"]
