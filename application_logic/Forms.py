# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) CompuCom, All Rights Reserved
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, RadioField, SelectField, TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# This can be a connection to Snowflake
class Capability:

    def __init__(self, tuple_list:list):
        self.tuple_list = tuple_list
    
    def get_list(self):
        return self.tuple_list

class TechnologyStack(FlaskForm):

    capability_obj = Capability([(1,'Backend'),(2,'Infrastructure'),(3,'Data'),(4,'Other')])
    technology_stack_name = StringField('Technology Stack Name:', validators=[DataRequired()])
    technology_capability_id = SelectField(u'Technology Capability:', choices=capability_obj.get_list())
    submit = SubmitField('Submit')
    