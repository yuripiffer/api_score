from flask import Flask, request
import MySQLdb
import json
import pandas as pd
from datetime import datetime, date

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", user="root", db="exemplo_score" )
conn.autocommit(True)
cursor = conn.cursor()



def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))



@app.route("/", methods=["GET"])
def index():
    return "API CONECTADA"

@app.route("/consulta/", methods = ["GET"])
@app.route("/consulta/<cpf>", methods = ["GET"])
def consulta(cpf=None):
    sql = "SELECT * FROM pessoa "
    if cpf:
        sql += f" WHERE cpf = {cpf}"
    cursor.execute(sql)

    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)

    ### vê se a idade é igual ou maior que 18 aplicando um map pela função calculate_age
    df = df.loc[df["data_nascimento"].apply(calculate_age) >= 18]
    ### converte de novo "data_nascimento" em string
    df["data_nascimento"] = df["data_nascimento"].astype(str)
    return df.to_json(orient="records")

@app.route("/score/<cpf>", methods = ["GET"])
def score(cpf):
    sql = f"SELECT nome, score, divida FROM pessoa WHERE cpf = {cpf} "
    cursor.execute(sql)
    resultado = cursor.fetchall()
    nome = resultado[0][0]
    score = resultado[0][1]
    divida = resultado[0][2]

# Tratar cpf passado errado
# Tratar cpf menor que 18 anos

    frase=""
    if divida>0:
        frase = f"""
        Nome: {nome}
        Score: {score}
        Usuário possui dívidas cadastradas:
        -- total de dívidas: R$ {divida}
        """
    elif divida ==0:
        frase = f"""
        Nome: {nome}
        Score: {score}
        Usuário não possui dívidas cadastradas.
        """
    return frase

@app.route("/quitacao/", methods = ["PUT"])
def quitacao():
    raw_request = request.data.decode("utf-8")
    dict_values = json.loads(raw_request)
    cpf = dict_values["cpf"]
    valor_pagamento = dict_values["valor_pagamento"]

    sql = f"SELECT divida FROM pessoa WHERE cpf = {cpf} "
    cursor.execute(sql)
    resultado = cursor.fetchall()
    divida = resultado[0][0]

    #checar se a dívida não é R$0.00

    if divida != valor_pagamento:
        frase = f"Valor de pagamento difere do valor da dívida. DÍVIDA = {divida}," \
                f"VALOR DE PAGAMENTO = R$ {valor_pagamento}"
    else:
        sql = f" UPDATE pessoa SET score = 1000 WHERE cpf = {cpf} "
        cursor.execute(sql)
        frase = "Dívida paga com sucesso! Score atual = 1000 pontos."
    return frase


# # Dropar colunas
# df = df.drop(["cpf", "data_nascimento"], axis=1)

# # Verificar se a pessoa tem mais de 18 anos
# df["data_nascimento"] = pd.to_datetime(df["data_nascimento"])
# def calculate_age(born):
#     today = datetime.date.today()
#     return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
# df = df.loc[df["data_nascimento"].apply(calculate_age) >= 18]



app.run(debug=True)