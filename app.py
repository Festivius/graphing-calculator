from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import re
from sympy import sympify, symbols, lambdify
import uuid


def crop_image(img_path, left, top, right, bottom):
    with Image.open(img_path) as img:
        cropped = img.resize((1000,1000))
        cropped = cropped.crop((left,top,right,bottom))
        return cropped
    

def preprocess(expr):
    if expr.__contains__('='):
        x = expr.index('=')
        expr = expr[x+1:]
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)([a-zA-Z]+\()', r'\1*\2', expr)
    expr = re.sub(r'(\))(\d|[a-zA-Z])', r'\1*\2', expr)
    if expr.__contains__('|'):
        ind = expr.index('|')
        expr = expr[:ind]+'abs('+expr[ind+1:]
        ind = expr.index('|')
        expr = expr[:ind]+')'+expr[ind+1:]
    return expr


def graph(equation, x_size,y_size):
    plt.figure(figsize=(x_size*2,y_size*2))
    x = np.linspace(-x_size,x_size,x_size*100+1)

    processed = preprocess(equation)

    var = symbols('x')
    parsed = sympify(processed)
    f = lambdify(var,parsed,modules='numpy')

    y = []

    for i in x:
        try:
            val = f(i)
            if val > y_size or val < -y_size:
                val = np.nan
            y.append(val)
        except:
            val = np.nan

    y = np.array(y)

    plt.plot(x,y)
    plt.grid(color='gray', linestyle='--', linewidth=1)

    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.axhline(0, color='black', linewidth=2)
    plt.axvline(0, color='black', linewidth=2)

    x_ticks = np.linspace(-x_size, x_size, 21)
    y_ticks = np.linspace(-y_size, y_size, 21)

    ax.set_xticklabels(['0'+' '*6 if x == 0 else str(x) for x in x_ticks])
    ax.set_yticklabels(['' if y == 0 else str(y) for y in y_ticks])

    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    
    save_dir = os.path.join(os.getcwd(), 'static', 'images')
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(save_dir, filename)

    plt.xlim(-10,10)
    plt.ylim(-10,10)

    plt.savefig(filepath)
    plt.close()

    cropped_image = crop_image(filepath, left=180, top=170, right=850, bottom=840)
    cropped_filepath = os.path.join(save_dir, f"plot_{filename}")
    cropped_image.save(cropped_filepath)

    return f"plot_{filename}"


matplotlib.use('Agg')
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/run_python', methods=['POST'])
def run_python():
    if request.method == 'OPTIONS':
        response = Flask.make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    try:
        data = request.get_json()
        input_value = data.get('input',0)
        output_value = graph(input_value, 10, 10)
        return jsonify({"output": output_value})
    except Exception as e:  
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port,debug=True, use_reloader=False)
