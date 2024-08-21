# create a class DatabaseConnector
# you will use to connect with and upload data to the database.
import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect


class DatabaseConnector:
    """
    This class provides methods to connect to and upload data to a database.
    """
    
    def __init__(self):
        pass
    
    #   extract the information from an AWS RDS database.
    def read_db_creds(self, file_path = 'db_creds.yaml'):
        with open(file_path, mode = "r") as file:
            creds = yaml.safe_load(file)
        return creds
    
    def read_local_db_creds(self, file_path = 'local_db_creds.yaml'):
        with open(file_path, mode = "r") as file:
            creds = yaml.safe_load(file)
        return creds

    def init_db_engine(self, creds=None):
         if creds is None:
            creds = self.read_db_creds()
         engine = create_engine(f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
         return engine

    def list_db_tables(self, creds=None):
        engine = self.init_db_engine(creds=creds)
        inspector = inspect(engine)
        return inspector.get_table_names()

    def upload_to_db(self, df, table_name, creds=None):
        engine = self.init_db_engine(creds = creds)
        df.to_sql(table_name, engine, if_exists='replace', index=False)


