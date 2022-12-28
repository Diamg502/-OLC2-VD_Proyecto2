from flask import Flask

app = Flask(__name__)

@app.route('/')
def Hello_Word():
    return("Hola","Mundo")

@app.route('/hola_mundo')
def Hola_Mundo():
    return("Diego","Martinez","USAC","Compi2")

if __name__ == "__name__":
    from waitress import serve
    serve(app, port=5800)