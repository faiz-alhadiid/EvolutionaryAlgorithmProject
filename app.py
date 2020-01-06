from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
from gen_all import Population

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result/', methods=['POST'])
def find_result():
    data = request.get_json()
    print(data)
    pop = Population(
        data['machines'], 
        data['processes'], 
        data['pop_size'], 
        data['crossover_rate'], 
        data['mutation_rate']
    )
    result = pop.generate(data['iteration'])
    print()
    print(result)
    return jsonify(result)

