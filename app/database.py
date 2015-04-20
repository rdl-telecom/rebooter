#!/usr/bin/env python2
import sqlite3
import re

re_str = re.compile(r'^[\w\s\(\)-]*$')
db_query = 'select id, name, ip from bundles where name not like "Auto%%" and name not like "Reserved%%" and name like "%s" %s order by name'
db_path = '/opt/modgud/3.0.0/etc/modgud/configuration.sqlite3'
db_exclude = 'and name not like "%%%s%%" '

# /opt/modgud/3.0.0/var/log/modgudd.sqlite3
# select bundle_id from bundle_stats where last_connect > last_disconnect;

def get_list(string=''):
	if not re_str.match(string) or len(string) > 30:
		return ''
	param='%'
	exclude=''
	for el in string.split():
		if el[:1] == '-':
			exclude += db_exclude%el[1:]
		else: 
			param += el
			param += '%'
	result = []
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()
		cur.execute(db_query%(param, exclude))
		result = cur.fetchall()
		con.close()
	except:
		pass
	return result
