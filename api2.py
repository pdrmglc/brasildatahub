import psycopg2
import redis
import tempfile
import os

# Conexão com Redis
r = redis.Redis(
    host='ip do banco',
    port='porta do banco',
    password=None,
    decode_responses=True
)

# Defina o diretório temporário desejado
TEMP_DIR = ""  # Substitua pelo seu diretório desejado

# Função para entregar arquivos
def entregar_arquivos(contexto, ano_inicial, ano_final, formato):
    connection = None
    cursor = None
    try:
        # Conectar ao PostgreSQL dentro da função
        connection = psycopg2.connect(
            user="nomeusuariobanco",
            password="senha",
            host="ip de host",
            port="porta do banco   ",
            database="nome do banco",
            options="-c client_encoding=UTF8"
        )
        cursor = connection.cursor()
        
        chave = f"{contexto}_{ano_inicial}_{ano_final}_{formato}"
        caminho = r.get(chave)
        current_directory = os.getcwd()

        if caminho is None:
            # Criar o arquivo temporário no diretório especificado
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{formato}", dir=TEMP_DIR) as temp_file:
                temp_file_path = temp_file.name

                #todos os casos
                if formato == "csv" and contexto != "PIB" and contexto != "População":
                    # Consulta para CSV
                    querycsv = f"COPY (SELECT * FROM {contexto} WHERE nu_ano BETWEEN '{ano_inicial}' AND '{ano_final}') TO STDOUT WITH CSV HEADER;"
                    with open(temp_file_path, 'w', newline='', encoding='utf-8') as file:
                        cursor.copy_expert(querycsv, file)

                #todos os casos
                elif formato == "json" and contexto != "PIB" and contexto != "População":
                    # Consulta para JSON
                    queryjson = f"SELECT row_to_json(t) FROM (SELECT * FROM {contexto} WHERE nu_ano BETWEEN '{ano_inicial}' AND '{ano_final}') t;"
                    with open(temp_file_path, 'w', encoding='utf-8') as file:
                        cursor.copy_expert(queryjson, file)

                elif formato == "csv" and contexto == "População":
                    querycsv_ibge_pop = f"COPY (SELECT * FROM ibge_pop WHERE ano BETWEEN '{ano_inicial}' AND '{ano_final}') TO STDOUT WITH CSV HEADER;"
                    with open(temp_file_path, 'w', newline='', encoding='utf-8') as file:
                        cursor.copy_expert(querycsv_ibge_pop, file)
                        
                elif formato == "csv" and contexto == "PIB":
                    querycsv_ibge_pib = f"COPY (SELECT * FROM ibge_pop WHERE ano BETWEEN '{ano_inicial}' AND '{ano_final}') TO STDOUT WITH CSV HEADER;"
                    with open(temp_file_path, 'w', newline='', encoding='utf-8') as file:
                        cursor.copy_expert(querycsv_ibge_pib, file)

            # Salvar o conteúdo do arquivo temporário no Redis
            with open(temp_file_path, 'rb') as file:
                r.set(chave, temp_file_path)
            
            # Definir o caminho do arquivo para retorno
            caminho = temp_file_path

            if formato == "csv":
                caminho_pronto = os.path.join(current_directory,"dados", "CSV", caminho)
                return caminho_pronto

            elif formato == "json":
                caminho_pronto = os.path.join(current_directory, "dados", "JSON", caminho)
                return caminho_pronto
            
        elif formato == "csv":
            caminho_pronto = os.path.join(current_directory,"dados", "CSV", caminho)
            return caminho_pronto
        
        elif formato == "json":
            caminho_pronto = os.path.join(current_directory, "dados", "JSON", caminho)
            return caminho_pronto

    except Exception as e:
        print(f"Falhou: {e}")
        return None

    finally:
        # Fechar conexões e cursores
        if cursor:
            cursor.close()
        if connection:
            connection.close()
