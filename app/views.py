#!/usr/bin/env python2
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import render_template, flash, redirect, session, url_for, g
from app import app
from forms import LoginForm, MainForm
from users import User
import icomera
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def api_root():
	username = g.user.id
	fullname = g.user.fullname
	form = MainForm()
	if form.validate_on_submit():
		for device in form.devices.data:
			device_params = form.get_device(device)
			if icomera.reboot(device_params['ip'], form.configure.data, username):
				flash('Перезагружаю ' + device_params['name'], category='ok')
			else:
				flash('Не могу подключиться к ' + device_params['name'], category='error')
	return render_template('index.html', title = username, username = fullname, form = form)

@app.route('/login', methods = ['GET', 'POST'])
@lm.unauthorized_handler
def api_login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('api_root'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.get(form.username.data)
		if user and form.password.data == user.password:
			login_user(user)
			return redirect(url_for('api_root'))
		else:
			flash('Неверное имя пользователя или пароль')
	return render_template('login.html', title = 'login', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('api_root'))

@lm.user_loader
def load_user(id):
    return User.get(id)

@app.before_request
def before_request():
	g.user = current_user
