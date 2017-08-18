import os
import requests
import json

from flask.json import jsonify
from flask import Flask, request, render_template, url_for

app = Flask(__name__)



@app.route("/")
def hello():
    # return "Hello world!"
    return render_template('index.html')

@app.route("/dns")
def dns():
    return render_template('dns.html')

@app.route("/dnsshow", methods=['GET','POST'])
def dnsshow():
    if request.method == 'POST':
        print(request.form['domain'])
        # result=request.form.getlist('domain')
        domain_prefix='http://dns-api.org/A/'
        domain_suffix=request.form['domain']
        domain_to_lookup=domain_prefix+domain_suffix
        print(domain_to_lookup)
        resp = requests.get(domain_prefix+domain_suffix)
        print(resp.json())
        all_a_records=[]
        for a in resp.json():
            all_a_records.append(a)
        print(len(all_a_records))
        # a_data
        # a_name = a_data[0]['name']
        # a_ttl = a_data[0]['ttl']
        # a_type = a_data[0]['type']
        # a_value = a_data[0]['value']
        # return str(a_data) + str(a_value)
        # return "a"
        return render_template('dns.html',
            all_a_records = all_a_records)
            # a_name = a_name, a_ttl = a_ttl, a_type = a_type, a_value = a_value)

@app.route("/exception", methods=['GET'])
def exception():
    return render_template('exception.html')

@app.route("/troubleshoot")
def troubleshoot():
    return render_template('troubleshoot.html')

@app.route("/echo", methods=['POST'])
def echo():
    return render_template('echo.html', text=request.form['text'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port, debug=True)

# from flask import Flask
# app = Flask(__name__)
#
#
#
# quarks = [{'name': 'up', 'charge': '+2/3'},
#           {'name': 'down', 'charge': '-1/3'},
#           {'name': 'charm', 'charge': '+2/3'},
#           {'name': 'strange', 'charge': '-1/3'}]
#
#
#
# @app.route('/', methods=['GET'])
# def hello_world():
#     return jsonify({'message' : 'Hello, World!'})
#
# @app.route('/quarks', methods=['GET'])
# def returnAll():
#     return jsonify({'quarks' : quarks})
#
# @app.route('/quarks/<string:name>', methods=['GET'])
# def returnOne(name):
#     theOne = quarks[0]
#     for i,q in enumerate(quarks):
#       if q['name'] == name:
#         theOne = quarks[i]
#     return jsonify({'quarks' : theOne})
#
# @app.route('/quarks', methods=['POST'])
# def addOne():
#     new_quark = request.get_json()
#     quarks.append(new_quark)
#     return jsonify({'quarks' : quarks})
#
# @app.route('/quarks/<string:name>', methods=['PUT'])
# def editOne(name):
#     new_quark = request.get_json()
#     for i,q in enumerate(quarks):
#       if q['name'] == name:
#         quarks[i] = new_quark
#     qs = request.get_json()
#     return jsonify({'quarks' : quarks})
#
# @app.route('/quarks/<string:name>', methods=['DELETE'])
# def deleteOne(name):
#     for i,q in enumerate(quarks):
#       if q['name'] == name:
#         del quarks[i]
#     return jsonify({'quarks' : quarks})
