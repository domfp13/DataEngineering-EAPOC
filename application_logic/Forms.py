# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Enrique Fuentes Plata

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from application_logic.Datamodel import DataLoader

class TechnologyStack(FlaskForm):

    data_loader = DataLoader()
    technology_stack_name = StringField('Technology Stack Name:', validators=[DataRequired()])
    technology_capability_id = SelectField(u'Technology Capability:', choices=data_loader.get_technology_capability())

    def insert_data(self)->None:
        """This method uses and instance of application_logic.DataLoader and calls the insert_data_into_stack method
        """
        query = "INSERT INTO webapp.technology_stack (technology_stack_name, technology_capability_id) VALUES (%s, %s)"
        values = (self.technology_stack_name.data, self.technology_capability_id.data)
        TechnologyStack.data_loader.insert_data_into_stack(query, values)
