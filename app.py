import os
import requests
import json
import sys

from flask.json import jsonify
from flask import Flask, request, render_template, url_for, flash, redirect

app = Flask(__name__)
app.secret_key = 'some_secret'


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
        domain_suffix=request.form['domain']
        try:
            # DECLARING EMPTY LISTS TO STORE THE KEY VALUE PAIRS THAT RETURN FROM THE HTTP RESPONSE
            all_a_records=[]
            all_aaaa_records=[]
            all_mx_records=[]
            all_cn_records=[]
            all_soa_records=[]
            all_txt_records=[]
            all_ns_records=[]
            # DOMAIN PREFIXES
            a_domain_prefix='http://dns-api.org/A/'
            aaaa_domain_prefix = 'http://dns-api.org/AAAA/'
            mx_domain_prefix='http://dns-api.org/MX/'
            cn_domain_prefix='http://dns-api.org/CNAME/'
            soa_domain_prefix='http://dns-api.org/SOA/'
            txt_domain_prefix='http://dns-api.org/TXT/'
            ns_domain_prefix='http://dns-api.org/NS/'
            # @ RECORD LOOPUP==================
            domain_to_lookup=a_domain_prefix+domain_suffix
            resp = requests.get(domain_to_lookup)
            for a in resp.json():
                all_a_records.append(a)
            # =================================
            # AAAA RECORD LOOKuP
            domain_to_lookup = aaaa_domain_prefix+domain_suffix
            resp = requests.get(domain_to_lookup)
            print("finished the second lookup")
            for aaaa in resp.json():
                all_aaaa_records.append(aaaa)
            # =================================
            # MX RECORD LOOKUP
            domain_to_lookup=mx_domain_prefix+domain_suffix
            resp=requests.get(domain_to_lookup)
            print("finished the 3rd lookup")
            for mx in resp.json():
                all_mx_records.append(mx)
            # =================================
            # CNAME RECORD LOOKUP
            domain_to_lookup=cn_domain_prefix+domain_suffix
            resp=requests.get(domain_to_lookup)
            print("finished the 4th lookup")
            for cn in resp.json():
                all_cn_records.append(cn)
            # =================================
            # SOA RECORD LOOKUP
            domain_to_lookup=soa_domain_prefix+domain_suffix
            resp=requests.get(domain_to_lookup)
            print("finished the 5th lookup")
            for soa in resp.json():
                all_soa_records.append(soa)
            # =================================
            # TXT RECORD LOOKUP
            domain_to_lookup=txt_domain_prefix+domain_suffix
            resp=requests.get(domain_to_lookup)
            print("finished the sixth lookup")
            for txt in resp.json():
                all_txt_records.append(txt)
            # =================================
            # NAMESERVER RECORD LOOKUP
            domain_to_lookup=ns_domain_prefix+domain_suffix
            resp=requests.get(domain_to_lookup)
            print("finished the 7th lookup")
            for ns in resp.json():
                all_ns_records.append(ns)
            return render_template('dns.html',
                all_a_records = all_a_records,
                all_aaaa_records = all_aaaa_records,
                all_mx_records = all_mx_records,
                all_cn_records = all_cn_records,
                all_soa_records = all_soa_records,
                all_txt_records = all_txt_records,
                all_ns_records = all_ns_records,
                domain = domain_suffix)
        except:
            e = sys.exc_info()[0]
            flash('Please enter a domain')
            error = 'Please enter a domain'
            return redirect(url_for('dns'))
                # a_name = a_name, a_ttl = a_ttl, a_type = a_type, a_value = a_value)
@app.route("/exception", methods=['GET', 'POST'])
def exception():
    if request.method == 'POST':
        # GET ALL VALUES FROM FORM
        agent_name=request.form['agent_name']
        agent_email=request.form['agent_email']
        sup_name=request.form['sup_name']
        sup_email=request.form['sup_email']
        approved_by=request.form['approved_by']
        exception_date=request.form['exception_date']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        reason = request.form['reason']
        print(str(agent_name))
        print(str(agent_email))
        print(str(sup_name))
        print(str(sup_email))
        print(str(approved_by))
        print(str(exception_date))
        print(str(start_time))
        print(str(end_time))
        print(str(reason))
        
        return render_template('exception.html')
    elif request.method == "GET":
        return render_template('exception.html')
    else: return render_template('error.html')

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
