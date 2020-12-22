# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved

from flask import (Flask, render_template, session,
                   redirect, url_for, request)
from flask_wtf import FlaskForm 
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField, SelectField, TextField,
                     TextAreaField, SubmitField)
from wtforms.validators import DataRequired
from os import environ

#from ptest.DataHandler import DataLoader

app = Flask(__name__)

# Change this for an env virable
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    breed = StringField('Technology-Capability Name:', validators=[DataRequired()])
    neutered  = BooleanField("Have you been neutered?")
    mood = RadioField('Please choose your mood:', choices=[('mood_one','Happy'),('mood_two','Excited')])
    food_choice = SelectField(u'Pick Your Favorite Food:',
                          choices=[('chi', 'Chicken'), ('bf', 'Beef'),
                                   ('fish', 'Fish')])
    feedback = TextAreaField()
    submit = SubmitField('Submit')

class TechnologyCapability(FlaskForm):
    """This general class gets information about the Technology Capability.
    Mainly a way to go through many of the WTForms Fields.

    Args:
        Backend (string): This will be the name of technology capability.

    Returns:
        None
    """
    name = StringField('TechnologyCapability Name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def index():
    number_list = [1,2,3]
    return render_template("index.html", number_list=number_list)

@app.route("/services")
def services():
    name = "Enrique"
    return render_template("services.html", name=name)

@app.route("/submitted")
def submitted():
    info_1 = request.args.get('info_1')
    info_2 = request.args.get('info_2')
    return render_template("submitted.html", info_1=info_1, info_2=info_2)

@app.route("/formTest", methods=['GET','POST'])
def other():
    
    form = InfoForm()

    if form.validate_on_submit():
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data
        
        return redirect(url_for("thankyou"))
    
    return render_template('01-home.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('01-thankyou.html')

@app.route("/tc", methods=['GET','POST'])
def technology_capability():
    
    form = TechnologyCapability()

    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for("thankyou"))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))
    app.run(debug=True, host='0.0.0.0', port=8080) # run without container