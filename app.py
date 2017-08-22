import os
import requests
import json
from datetime import datetime
import sys
import yagmail
import os
from flask.json import jsonify
from flask import Flask, request, render_template, url_for, flash, redirect, session, abort
from flask_sqlalchemy  import SQLAlchemy
import pymysql
# pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['CLEARDB_DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] =
db = SQLAlchemy(app)
app.secret_key = 'some_secret'

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True)
    email=db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username=username
        self.email=email

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    body=db.Column(db.Text)
    pub_date=db.Column(db.DateTime)

    category_id=db.Column(db.Integer, db.ForeignKey('category.id'))
    category=db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title=title
        self.body=body
        self.category=category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date=pub_date

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route("/")
def hello():
    # return "Hello world!"
    print(os.environ['CLEARDB_DATABASE_URL'])
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
        yag = yagmail.SMTP('exappv2', 'QWErty!@#456')
        title = '<h2>Exception Submission</h2>'
        sender = '<p><b>Agent: </b>{}</p>'.format(agent_name)
        sender_email = '<p><b>Agent Email: </b>{}</p>'.format(agent_email)
        manager = '<p><b>Manager: </b>{}</p>'.format(sup_name)
        approved_by = '<p><b>Approved by: </b>{}</p>'.format(approved_by)
        exception_date = '<p><b>Date: <b>{}</p>'.format(exception_date)
        start_time = '<p><b>Start Time: </b>{}</p>'.format(start_time)
        end_time = '<p><b>End Time: </b>{}</p>'.format(end_time)
        reason = '<p><b>Reason: </b>{}</p>'.format(reason)
        email_footer = '<br><p>=====================================</p></br><p>This email was automagically created and sent to {} using python 3, yag, and some coding judo.'.format(sup_name)
        contents = [title, sender, sender_email, manager, exception_date, start_time, end_time, reason, email_footer]
        # Send the email to the manager | Change the email in the functiion to the variable recipient
        yag.send('pastrana.steven.az@gmail.com', 'Exception Submission', contents)
        # Send the confirmation email
        yag.send(agent_email, 'Exception Confirmation', 'Your exception was successfuly submited.')
        flash('Submitted Exception')
        return render_template('exception.html')
    elif request.method == "GET":
        return render_template('exception.html')
    else: return render_template('error.html')

@app.route("/troubleshoot")
def troubleshoot():
    return render_template('troubleshoot.html')

@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        fb_agent_email = request.form['fb_agent_email']
        fb_agent_name = request.form['fb_agent_name']
        feedback = request.form['feedback']
        print(fb_agent_email)
        print(fb_agent_name)
        print(feedback)
        yag = yagmail.SMTP('exappv2', 'QWErty!@#456')
        title = '<h2>Feedback Submission</h2>'
        sender = '<p><b>Agent: </b>{}</p>'.format(fb_agent_name)
        sender_email = '<p><b>Agent Email: </b>{}</p>'.format(fb_agent_email)
        feedback = '<p><b>Feedback: </b>{}</p>'.format(feedback)
        contents = [title, sender, sender_email, feedback]
        default_reply= '<p>Thanks for the feedback. Your submission will go a long way towards making this project a better resource for everyone that uses it</p>'
        yag.send('steven.antonio.dev@gmail.com', 'TBP Feedback Submission', contents)
        yag.send(fb_agent_email, 'Thanks you for your feedback', default_reply)
        # flash('Feedback Sent')
        return render_template('feedback.html')
    elif request.method == 'GET':
        return render_template('feedback.html')
    else: return render_template('error.html')

@app.route("/products", methods=['POST', 'GET', 'DELETE'])
def products():
    return "The products GEet"

@app.route("/products-login", methods=['POST', 'GET'])
def productslogin():
    return "The login page"

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
