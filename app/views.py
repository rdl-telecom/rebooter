#!/usr/bin/env python2
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import render_template, flash, redirect
from app import app
from forms import LoginForm, MainForm
from users import users
import icomera

username = 'unknown'
fullname = 'Неизвестный'

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def api_root():
	if username == 'unknown':
		return redirect('/login')
	form = MainForm()
	if form.validate_on_submit():
		for device in form.devices.data:
			device_params = form.get_device(device)
			if icomera.reboot(device_params['ip'], form.configure.data):
				flash('Перезагружаю ' + device_params['name'], category='ok')
			else:
				flash('Не могу подключиться к ' + device_params['name'], category='error')
	return render_template('index.html', title = username, username = fullname, form = form)

@app.route('/login', methods = ['GET', 'POST'])
def api_login():
	global username, fullname
	form = LoginForm()
	if form.validate_on_submit():
		if form.username.data in users and form.password.data == users[form.username.data]['password']:
			username = form.username.data
			fullname = users[form.username.data]['fullname']
			return redirect('/index')
		else:
			flash('Неверное имя пользователя или пароль')
	return render_template('login.html', title = 'login', form = form)
