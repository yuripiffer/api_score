# import MySQLdb
#
# nome_banco_de_dados = "exemplo_score"
# tabela = "pessoa"
#
# conn = MySQLdb.connect(host="localhost", user="root", db=nome_banco_de_dados )
# conn.autocommit(True)
# cursor=conn.cursor()
#
# def executa_e_persiste(self, comando: str):
#     self.cursor.execute(comando)
#     self.conexao.commit()
#
# def cadastrar_pessoa(self, cpf:str, nome:str, data_nascimento:str, divida=0.0, score=500):
#     """
#     :param cpf: str com apenas os números do cpf
#     :param nome: str nome completo que será transformado em uppercase antes de armazenar.
#     :param divida: valor com duas casas decimais. Padrão é 0.0
#     :param data_nascimento: str padrão MySQL: "YYYY-MM-DD"
#     :param score: valor inteiro de 0 a 1000
#     :return:
#     """
#     nome = nome.upper()
#     sql = f"""INSERT INTO {tabela} (cpf, nome, data_nascimento, divida, score) VALUES
#     ('{cpf}', '{nome}', '{divida}', '{data_nascimento}','{divida}', '{score}')"""
#     self.cursor.execute(sql)
#     self.conexao.commit()
#
#
# cadastrar_pessoa("080300822111", "Maria Elio Rio", "1985-12-05", 200, )