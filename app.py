# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

from flask import (Flask, render_template, session, redirect, url_for, request)
from os import environ
from application_logic.Forms import TechnologyStack
from application_logic.GenericFunctions import get_secret_key, getCredentials
#from application_logic.Datamodel import DataLoader

app = Flask(__name__)

# Change this for an env virable
app.config['SECRET_KEY'] = get_secret_key()

#dataloader = DataLoader(getCredentials())

@app.route("/")
def index():
    number_list = [1,2,3]
    #number_list = dataloader.get_technology_stack()
    return render_template("index.html", number_list=number_list)

@app.route("/technology_stack", methods=['GET','POST'])
def technology_stack():
    
    form = TechnologyStack()

    if form.validate_on_submit():
        
        session['technology_stack_name'] = form.technology_stack_name.data
        session['technology_capability_id'] = form.technology_capability_id.data

        return redirect(url_for('submitted'))
    
    return render_template('technology_stack.html', form=form)

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    server_port = int(environ.get('PORT', '8080'))
    app.run(debug=True, host='0.0.0.0', port=server_port)