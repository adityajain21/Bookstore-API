import requests
from flask import Flask, render_template, request, json, redirect, url_for, redirect
from flask.ext.mysql import MySQL

app = Flask(__name__)


@app.route("/")
def login():
	return render_template('index.html')

@app.route("/login",methods=['POST'])
def token():
	email = request.form['inputEmail']
	password = request.form['inputPassword']


	return "Login Succesful"


@app.route("/add")
def add():

	try:
		name = request.args.get('name')
		price = request.args.get('price')
		flag = request.args.get('flag')
		conn = mysql.connect()
		cursor = conn.cursor()
		if name and price:
			query = """INSERT INTO User (Name, Price, Available) VALUES (%s, %s, %s)"""
			cursor.execute(query,(name,price,flag))
			conn.commit()
			data = cursor.fetchall()
			if data is None:
				return "NOT Added"
			else:
				return "Added"
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/delete")
def delete():

	try:
		name = request.args.get('name')
		lt = request.args.get('lt')
		gt = request.args.get('gt')
		conn = mysql.connect()
		cursor = conn.cursor()
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
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/find")
def find():

	try:
		name = request.args.get('name')
		lt = request.args.get('lt')
		gt = request.args.get('gt')
		conn = mysql.connect()
		cursor = conn.cursor()
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
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()


@app.route("/edit")
def edit():

	try:
		bid = request.args.get('id')
		name = request.args.get('name')
		price = request.args.get('price')
		flag = request.args.get('flag')
		conn = mysql.connect()
		cursor = conn.cursor()
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