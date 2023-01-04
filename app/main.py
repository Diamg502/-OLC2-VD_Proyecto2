from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import io
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plot
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing

import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/files'
f = ""

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/columnas', methods=['POST'])
def columnas():
    global f
    if request.method == 'POST':
        da = request.files['file']
        filename = secure_filename(da.filename)
        da.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)) # Then save the file
        f = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(filename))
        df = pd.read_csv(f)
        columnas = { 
            'columnas': df.columns.tolist(),
            'filename': filename
        }
        return render_template('generador.html', columnas=columnas)

@app.route('/grafica', methods=['POST'])
def grafica():
    global f
    if request.method == 'POST':
        variable1 = request.form['variable1']
        variable2 = request.form['variable2']
        grafica = request.form['tipo']
        filename = request.form['filename']
        
        datos = pd.read_csv(f)
        x = datos[variable1].values.reshape(-1,1)
        y = datos[variable2].values.reshape(-1,1)
     
        if grafica == 'g1':
            
            #Progresion Linear
            plt.clf()
            model = LinearRegression()
            model.fit(x,y)
            y_pred = model.predict(x)
            plt.figure(figsize=(5, 4))
            ax = plt.axes()
            ax.scatter(x, y)
            ax.plot(x, y_pred)

            rnse = np.sqrt(mean_squared_error(y,y_pred))
            r2 = r2_score(y,y_pred)

            ax.set_xlabel(variable1)
            ax.set_ylabel(variable2)

            ax.axis('tight')
            plt.plot(x,y_pred,color='r')

            img = io.BytesIO()

            plt.title("RMSE: "+ str(rnse) + " R2: "+ str(r2))
            plt.suptitle("GRAFICA LINEAL")
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #GRAFICA DE PUNTOS
            plt.clf()
            ax = plt.axes()
            ax.set_xlabel(variable1)
            ax.set_ylabel(variable2)
            plt.scatter(x,y)
            img2 = io.BytesIO()
            plt.title("GRAFICA PUNTOS")
            plt.savefig(img2,format='png')
            img2.seek(0)
            plot_url2 = base64.b64encode(img2.getvalue()).decode()
            
            return render_template('grafica.html', imagen={ 'imagen': plot_url }, imagen2={'imagen2':plot_url2})
        elif grafica == 'g2':
            #PROGRESION POLINIOMEAR
            plt.clf()
            poly = PolynomialFeatures(degree=2, include_bias=False)
            x_poly = poly.fit_transform(x)
            model = LinearRegression()
            model.fit(x_poly,y)
            y_pred = model.predict(x_poly)

            rmse = np.sqrt(mean_squared_error(y,y_pred))
            r2 = r2_score(y,y_pred)

            plt.scatter(x, y)
            plt.plot(x,y_pred,color='r')
            plt.title("REGRESION POLINOMIAL")
            img3 = io.BytesIO()
            plt.suptitle("rmse: "+ str(rmse) + " r2: "+ str(r2) + " Grado: 2")
            plt.savefig(img3,format='png')
            img3.seek(0)
            plot_url3 = base64.b64encode(img3.getvalue()).decode()
            print('lineas')
            return render_template('grafica.html', imagen={ 'imagen': plot_url3}, imagen2={'imagen2':plot_url3 })
        elif grafica == 'g3':
            print('pastel')
            return render_template('grafica.html', imagen={ 'imagen' })
        elif grafica == 'g4':
            print('g4')
            return render_template('grafica.html', imagen={ 'imagen' })
        else:
            print("nada")
            return render_template('grafica.html', imagen={ 'imagen'})

if __name__ == "__main__":
    from waitress import serve
    serve(app, port=5000)