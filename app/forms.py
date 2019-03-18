from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from wtforms import StringField, validators
from app.model import User


class UserForm(ModelForm):
    name = StringField('name', default='Unnamed')
    nick = StringField('nick', [validators.Length(min=3)])
    avatar = StringField('avatar', [validators.Optional()], default='')
