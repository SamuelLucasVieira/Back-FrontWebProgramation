import psycopg2
from contextlib import contextmanager
from pathlib import Path  # Usado para criar caminhos de arquivo robustos
import yaml # Você precisará de PyYAML: pip install PyYAML

# --- Carregamento da Configuração ---
# MUDANÇA 1: Centralizamos a lógica de leitura em uma função.
def get_db_config() -> dict:
    """
    Lê o arquivo de configuração YAML e retorna um dicionário com os parâmetros do banco.
    """
    try:
        config_path = Path(__file__).parent / 'config.yaml'

        with open(config_path, 'r') as f:
            app_config = yaml.safe_load(f)

        # MUDANÇA 3: Convertendo a lista de parâmetros em um dicionário de conexão.
        params_list = app_config.get('configuration_parameters', [])
        db_params = {}
        for item in params_list:
            db_params.update(item)

        if not db_params:
            raise ValueError("Parâmetros de configuração do banco não encontrados no config.yaml")
        
        return db_params

    except FileNotFoundError:
        print(f"ERRO: Arquivo de configuração não encontrado em '{config_path}'")
        raise
    except Exception as e:
        print(f"ERRO ao ler ou processar o arquivo de configuração: {e}")
        raise

# --- Gerenciamento da Conexão ---
@contextmanager
def get_db_connection():
    """Gerencia a conexão com o banco de dados, garantindo que seja fechada."""
    # MUDANÇA 4: Usamos a função para obter a configuração dinamicamente.
    db_config = get_db_config()
    conn = None # Inicializa a variável conn
    try:
        conn = psycopg2.connect(**db_config)
        print("Conexão com o banco de dados estabelecida.")
        yield conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        print("Verifique se os parâmetros (usuário, senha, host, etc.) estão corretos no config.yaml e se o banco de dados está online.")
        raise
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

@contextmanager
def get_db_cursor(commit=False):
    """Gerencia o cursor do banco, com opção de commit."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Erro durante a transação. Rollback executado. Erro: {e}")
            raise

# --- Bloco de Teste ---
# MUDANÇA 5: Adicionamos um bloco para testar a conexão de forma independente.
if __name__ == "__main__":
    print("Tentando conectar ao banco de dados para teste...")
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print("\nConexão bem-sucedida!")
            print(f"Versão do PostgreSQL: {db_version[0]}")
    except Exception as e:
        print("\nFalha no teste de conexão.")