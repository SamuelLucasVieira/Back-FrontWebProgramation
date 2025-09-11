import psycopg2
from abc import ABC, abstractmethod

# Classe abstrata que representa a interface DAO para Biomas
class Crud(ABC):
    
    @abstractmethod
    def __init__(self):
        """
        Inicializador do banco da API
        """
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """
        Estabelece uma conexão com o banco de dados usando a configuração fornecida.
        """
        if self.conn is None:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
    
   
    def closeConnection(self):
        """
        Fecha a conexão com o banco de dados, incluindo o cursor e a conexão.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.cursor = None
        self.conn = None
    
    @abstractmethod
    def getUser(self, **kwatributes):
        """
        Função de busca.
        """ 
    
    @abstractmethod
    def createUser(self, **kwatributes):
        """
        Função para criar usuário.
        """
        pass

    @abstractmethod
    def updateUser(self, **kwatributes):
        """
        Função para atualizar dados do usuário.
        """
        pass 

    @abstractmethod
    def deleteUser(self, **kwatributes):
        """
        Função para criar usuário.
        """
        pass
    