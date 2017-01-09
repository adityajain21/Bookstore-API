import requests
from flask import Flask, render_template, request, json, redirect, url_for, redirect
from flask.ext.mysql import MySQL
import hashlib


app = Flask(__name__)

def check(token):
	conn = mysql.connect()
	cursor = conn.cursor()
	query = """SELECT * FROM Token WHERE Hash=%s"""
	cursor.execute(query,(token))
	conn.commit()
	data = cursor.fetchall()
	if len(data):
		return 1
	else:
		return 0


@app.route("/")
def login():
	return render_template('index.html')


@app.route("/login",methods=['POST'])
def token():

	try:
		_email = request.form['inputEmail']
		_pass = request.form['inputPassword']
		m = hashlib.md5()
		m.update(_email + _pass)
		_hash = m.hexdigest()
		conn = mysql.connect()
		cursor = conn.cursor()
		if _email and _pass and _hash:
			query = """INSERT INTO Token (Email, Pass, Hash) VALUES (%s, %s, %s)"""
			cursor.execute(query,(_email,_pass,_hash))
			conn.commit()
			data = cursor.fetchall()
			if data is None:
				return "NOT Added"
			else:
				return render_template('token.html',has=_hash)
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/add")
def add():

	try:
		token = request.args.get('token') 
		name = request.args.get('name')
		price = request.args.get('price')
		flag = request.args.get('flag')
		conn = mysql.connect()
		cursor = conn.cursor()
		
		if token and check(token):
			if name and price:
				query = """INSERT INTO User (Name, Price, Available) VALUES (%s, %s, %s)"""
				cursor.execute(query,(name,price,flag))
				conn.commit()
				data = cursor.fetchall()
				if data is None:
					return "NOT Added"
				else:
					return "Added"
		else:
			return render_template('unauth.html')
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/delete")
def delete():

	try:
		token = request.args.get('token') 
		name = request.args.get('name')
		lt = request.args.get('lt')
		gt = request.args.get('gt')
		conn = mysql.connect()
		cursor = conn.cursor()
		
		if token and check(token):
			if name:
				query = """DELETE FROM User WHERE name=%s"""
				cursor.execute(query,(name))
				conn.commit()
				data = cursor.fetchall()
				if data is None:
					return '0'
				else:
					return '1'
			elif (lt and gt):
				query = """DELETE FROM User WHERE (price>=%s and price<=%s)"""
				cursor.execute(query,(lt,gt))
				conn.commit()
				data = cursor.fetchall()
				if data is None:
					return '0'
				else:
					return '1'
		else:
			return render_template('unauth.html')
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/find")
def find():

	try:
		token = request.args.get('token')
		name = request.args.get('name')
		lt = request.args.get('lt')
		gt = request.args.get('gt')
		conn = mysql.connect()
		cursor = conn.cursor()

		if token and check(token):
			if name:
				query = """SELECT * FROM User WHERE name=%s"""
				cursor.execute(query,(name))
				conn.commit()
				data = cursor.fetchall()
				print data
				if data is None:
					return '0'
				else:
					return '1'
			elif (lt and gt):
				query = """SELECT * FROM User WHERE (price>=%s and price<=%s)"""
				cursor.execute(query,(lt,gt))
				conn.commit()
				data = cursor.fetchall()
				print data
				if data is None:
					return '0'
				else:
					return '1'
		else:
			return render_template('unauth.html')
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/edit")
def edit():

	try:
		token = request.args.get('token')
		bid = request.args.get('id')
		name = request.args.get('name')
		price = request.args.get('price')
		flag = request.args.get('flag')
		conn = mysql.connect()
		cursor = conn.cursor()

		if token and check(token):
			if bid:
				if name:
					query = """UPDATE User SET name=%s WHERE id=%d"""
					cursor.execute(query,(name,bid))
					conn.commit()
					data = cursor.fetchall()
					print data
					if data is None:
						return '0'
					else:
						return '1'
				elif price:
					query = """UPDATE User SET price=%s WHERE id=%d"""
					cursor.execute(query,(price,bid))
					conn.commit()
					data = cursor.fetchall()
					print data
					if data is None:
						return '0'
					else:
						return '1'
				elif flag:
					query = """UPDATE User SET Available=%s WHERE id=%d"""
					cursor.execute(query,(flag,bid))
					conn.commit()
					data = cursor.fetchall()
					print data
					if data is None:
						return '0'
					else:
						return '1'
		else:
			return render_template('unauth.html')
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


if __name__ == "__main__" :
	mysql = MySQL()

	mysql_config_file = "config.json"

	with open(mysql_config_file) as data_file:
		data = json.load(data_file)
		
		# MySQL configurations
		app.config['MYSQL_DATABASE_HOST'] = data["hostname"]
		app.config['MYSQL_DATABASE_USER'] = data["username"]
		app.config['MYSQL_DATABASE_PASSWORD'] = data["password"]
		app.config['MYSQL_DATABASE_DB'] = data["database"]

	mysql.init_app(app)
	app.run(debug=True)