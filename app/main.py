from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    #return("Hola","Mundo")
    listas = ['PHP,','PYTHON','JAVA','KITLIN','DART','JAVASCRIPT']
    data = {
        'titulo'        : 'PROYECTO2',
        'bienvenida'    : 'Diego Martinez - 201700355',
        'cursos'        : listas,
        'numero_listas' : len(listas)
    }
    return render_template('index.html', data=data)

@app.route('/resultados')
def Hola_Mundo():
    return("Diego","Martinez","USAC","Compi2")

@app.before_request
def before_request():
    print("Antes de la peticion...")

@app.after_request
def after_request(response):
    print("Despues de la petición")
    return response

if __name__ == "__main__":
    from waitress import serve
    serve(app, port=5000)