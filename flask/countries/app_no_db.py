from flask import Flask, request, jsonify
import db
    
app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1

#consultar todos
@app.route("/countries",methods=['GET'])
def get_countries():
    return jsonify(countries)

#consultar por id
@app.route("/countries/<int:id>", methods=['GET'])
def obter_countries_id(id):
    for countrie in countries: #percorrer os itens
        if countrie.get('id') == id: # procurar um item com o mesmo id passado
            return jsonify(countrie) #devolve a pesquisa
        
#editar
@app.route("/countries/<int:id>", methods=['PUT'])
def editar_countries_por_id(id):
    countrie_alterado = request.get_json() #recebendo os dados do usuário
    for indice,countrie in enumerate(countries):
        if countrie.get('id') == id:
            countries[indice].update(countrie_alterado)
            return jsonify(countries[indice])
        
#excluir
@app.route("/countries/<int:id>", methods=['DELETE'])
def excluir_countries_por_id(id):
    for indice,countrie in enumerate(countries):
        if countrie.get('id') == id:
            del countries[indice]
            return jsonify(countries)
        


@app.route("/countries",methods=['POST'])
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8090)