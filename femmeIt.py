
from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

perfils = [{"id": e, "nome": "Usuario "+str(e), "email":"E-mail "+str(e), "linkedin": "Linkedin "+str(e),
"telefone1":"Telefone "+str(e), 
"foto":"https://nailtime.com.br/wp-content/uploads/2018/11/00-Empoderamento-Feminino.jpg", "perfil": "Perfil "+str(e)} for e in range(1,11)]   

@app.route("/perfils", methods=['GET'])
def get():
    return jsonify(perfils)

@app.route("/perfils/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in perfils if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/perfils", methods=['POST'])
def post():
    global perfils
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in perfils]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        perfils.append(content)
        return jsonify({"status":"OK", "msg":"Usuário adicionada com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/perfils/<int:id>", methods=['DELETE'])
def delete(id):
    global perfils
    try:
        perfils = [e for e in perfils if e["id"] != id]
        return jsonify({"status":"OK", "msg":"Usuário removida com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	d = random.choice(perfils)
	data = {
		"to": token,
		"notification" : {
			"title":d["nome"],
			"body":"Você tem um novo evento em "+d['nome']
		},
		"data" : {
			"perfilId":d['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')