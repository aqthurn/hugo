import mysql.connector

class Comunication:

    def __init__(self):
        self.bd = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='testebd'
        )
        print('Conexão realizada com sucesso!')

    def insert_transacoes(self, nometransacoes, data, valor, tipo, descricao):
        try:
            cursor = self.bd.cursor()
            sql = "INSERT INTO transacoes (nometransacoes, data, valor, tipo, descricao) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nometransacoes, data, valor, tipo, descricao))
            self.bd.commit()
            print('Inserção realizada com sucesso!')
        except mysql.connector.Error as err:
            print(f'Erro ao inserir dados: {err}')
        finally:
            cursor.close()

    def update_transacoes(self, nometransacoes, data, valor, tipo, descricao):
        try:
            cursor = self.bd.cursor()
            sql = "UPDATE transacoes SET data=%s, valor=%s, tipo=%s, descricao=%s WHERE nometransacoes=%s"
            cursor.execute(sql, (data, valor, tipo, descricao, nometransacoes))
            self.bd.commit()
            print('Atualização realizada com sucesso!')
        except mysql.connector.Error as err:
            print(f'Erro ao atualizar dados: {err}')
        finally:
            cursor.close()

    def delete_transacoes(self, nometransacoes):
        try:
            cursor = self.bd.cursor()
            sql = "DELETE FROM transacoes WHERE nometransacoes=%s"
            cursor.execute(sql, (nometransacoes,))
            self.bd.commit()
            print('Exclusão realizada com sucesso!')
        except mysql.connector.Error as err:
            print(f'Erro ao excluir dados: {err}')
        finally:
            cursor.close()

    def select_transacoes(self, nometransacoes):
        try:
            cursor = self.bd.cursor()
            sql = "SELECT * FROM transacoes WHERE nometransacoes LIKE %s"
            cursor.execute(sql, ('%' + nometransacoes + '%',))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f'Erro ao buscar dados: {err}')
        finally:
            cursor.close()

if __name__ == "__main__":
    comm = Comunication()
   