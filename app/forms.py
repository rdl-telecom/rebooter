# coding: utf-8

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SelectMultipleField
from wtforms.validators import Required, ValidationError
import re
from device_list import DeviceList

field_re = re.compile(r'[a-zA-Z0-9]{5,20}')


def validate_field(form, field):
	if not field_re.match(field.data):
		raise ValidationError('поле должно содержать от 5 до 20 латинских букв и цифр')

class LoginForm(Form):
	username = TextField('Пользователь', validators = [ validate_field ])
	password = PasswordField('Пароль', validators = [ validate_field ])
	remember_me = BooleanField('Запомнить меня', default = False)

class MainForm(Form):
	device_list = DeviceList()
	devices = SelectMultipleField('Выберите устройства', choices = device_list.choices)
	configure = BooleanField('Запустить configurator', default = False)
	def get_device(self, key_value):
		return self.device_list[key_value]
