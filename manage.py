#!flask/bin/python
from flask import Flask
import json, requests #импорт библиотек

def keys(dist):#функция получения ключей словаря
	v = str(dist.keys())
	v = v[11: -2]
	vv = ""
	for i in range(len(v)):
		if(v[i] != "'" and v[i:i+2] != " '"):
			vv += v[i]

	return vv.split(",")

def list():#функция получения готового словаря
	source = json.loads(requests.get("https://job.firstvds.ru/spares.json").content.decode("latin1"))
	edit = json.loads(requests.get("https://job.firstvds.ru/alternatives.json").content.decode("latin1"))['alternatives']
	edit["PC4 16G"][0] = "RAM 16GB PC4-2400 REG"
	edit["PC4 16G"][1] = "RAM 16Gb PC4-2133 REG"	
	exit = {}
	keys_source = keys(source)
	keys_edit = keys(edit)
	keys_exit = []
	for i in source:
		a = True
		for j in keys_edit:
			for o in edit[j]:
				if(i == o):
					a = False
					test = True
					for k in keys_exit:
						if(j == k):
							test = False
					if(test):
						keys_exit.append(j)
		if(a):
			keys_exit.append(i)
	x = 0
	print(str(keys_exit))
	for i in keys_exit:
		exit[i] = {"mustbe": 0, 'arrive': 0, 'count': 0}
	for i in keys_exit:
		a = True
		for j in keys_edit:
			if(i == j):
				x += 1
				print(str(x))
				for o in edit[j]:
					exit[i]["mustbe"] = max(source[o]["mustbe"], exit[i]["mustbe"])
					exit[i]["arrive"] = int(source[o]["arrive"]) + int(exit[i]["arrive"])
					exit[i]["count"] = int(source[o]["count"]) + int(exit[i]["count"])
					a = False
		if(a):
			exit[i]["mustbe"] = source[i]["mustbe"]
			exit[i]["arrive"] = source[i]["arrive"]
			exit[i]["count"] = source[i]["count"]
	return [exit, keys_exit]

app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():#вывод словаря в html, с выделенными пунктами
	exit = list()
	keys_exit = exit[1]
	exit = exit[0]

	out = ""
	for i in keys_exit:
		d = exit[i]
		color = "#000"
		if(d["mustbe"] > (d['arrive'] + d['count'])):
			color = "#f00"	
		out += '<p style="color: ' + color + '">'
		out += str(i) + "<br>"
		out += "<br>  mustbe : " + str(d["mustbe"])
		out += "<br>  arrive : " + str(d["arrive"])
		out += '<br>  count  : ' + str(d["count"])
		out += "</p>"
	return str(out)

@app.route("/mustbe")
def mustbe():#вывод только красных
	exit = list()
	keys_exit = exit[1]
	exit = exit[0]

	out = ""
	for i in keys_exit:
		d = exit[i]
		color = "#000"
		if(d["mustbe"] > (d['arrive'] + d['count'])):
			color = "#f00"	
			out += '<p style="color: ' + color + '">'
			out += str(i) + "<br>"
			out += "<br>  mustbe : " + str(d["mustbe"])
			out += "<br>  arrive : " + str(d["arrive"])
			out += '<br>  count  : ' + str(d["count"])
			out += "</p>"
	#o = keys(exit)
	#for i in o:
	#	out += "<br>" + str(i) + str(exit[i])
	return str(out)

@app.route("/json")
def json_return():#вывод в json
	re = app.response_class(response=json.dumps(list()[0]), status=200, mimetype='application/json')
	return re
app.run(debug = True)