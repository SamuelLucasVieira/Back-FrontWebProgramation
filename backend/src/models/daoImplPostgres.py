import psycopg2 # type: igonore
from config.config_reader import config_reader
from models.dao import Crud

# Chamada do com as credenciais de ambiente
config_reader = Config_reader()
app_config = config_reader.read_config('./config/config.yaml')
params = app_config.get('configuration_parameters', [])

# Função que busca o método do arquivo, config.yaml
def get_param(param_name):
    return next((param.get() for param in params if param_name in param), None)

# Chamada ao Banco de Dados Postgres
dbConfigApi = {
    'user' : get_param('user'),
    'host' : get_param('host'),
    'database' : get_param('database'),
    'password' : get_param('password'),
    'port' : get_param('port'),
}


class CrudDAOImplPGSQL(Crud):
    def __init__(self):
        """
        Conexão com o banco de dados, construtor da classe.
        """
        self.dbConfigApi = dbConfigApi
    def getUser(self, **kwatributes):
        idUser = kwatributes.get('user')
        try:
            self.connect()
            query = f"select name from users"
            parameters = []
            condition = []
            if idUser is not None:
                condition.append("name = %s")
                parameters.append(idUser)
            else:
                condition.append(";")
                parameters.append(query)
            self.cursor.execute(query, parameters)
            result = self.cursor.fetchall()
            return result if result else None
        except Exception as error:
            raise Exception(f"Error executing query: {error}")

        finally:
            self.close_connection()
   
    

valor = Crud()
valores = valor.getUser()
print(valores)    