from flask import Flask, request, send_file, render_template
import api2

app = Flask(__name__)

@app.route('/')

def main_page():
    return render_template("main_page.html")

@app.route('/downloads')
def download_page():
    return render_template("main_pag2.html")

@app.route('/get_data', methods=['POST'])
def get_data():
    ano_inicial = request.form['ano_inicial']
    ano_final = request.form['ano_final']
    contexto = request.form['contexto']
    formato = request.form['formato']
    
    caminho_arquivo = api2.entregar_arquivos(contexto, ano_inicial, ano_final, formato)

    if caminho_arquivo:
        print(caminho_arquivo)
        return send_file(caminho_arquivo, as_attachment=True)
    else:
        return "Erro ao gerar o arquivo", 500

if __name__ == "__main__":
    app.run(debug=False) 