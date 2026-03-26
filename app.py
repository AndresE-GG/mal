from flask import Flask, render_template, request, jsonify
from mal import obtener_animes_oficial

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search")
def search():
    letra = request.args.get("q", "")
    if not letra:
        return jsonify({"error": "No se proporcionó ninguna búsqueda"}), 400
        
    resultados = obtener_animes_oficial(letra)
    
    if isinstance(resultados, dict) and "error" in resultados:
        return jsonify(resultados), 500
        
    return jsonify({"results": resultados})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
