from psycopg_pool import ConnectionPool
import os, sys, re
from utils.bcolors import bcolors
from flask import current_app as app

class DB:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        self.init_pool()


    # Create a PostgreSQL pool connection
    def init_pool(self):
        self.print_in_colors(string="INIT_POOL")
        connection_url = os.getenv("CONNECTION_URL")
        if "cruddur_pinata" in connection_url:
            print(f"    {bcolors.OKGREEN}Connecting to: AWS RDS production db{bcolors.ENDC}")
        self.pool = ConnectionPool(connection_url)
        print(f"    {self.pool}")
        print(f"    {bcolors.OKGREEN}Connection pool successful{bcolors.ENDC}\n")

    
    # File opener. 
    # Reads in the file and returns the content. 
    def template(self, *args):
        PATH = list((app.root_path, 'db', 'sql') + args)
        PATH[-1] = f"{PATH[-1]}.sql"
        print(f"PATH: {PATH}")

        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

        TEMPLATE_PATH = os.path.join(*PATH)
        print(f"    \n{OKCYAN}SQL TEMPLATE-[{TEMPLATE_PATH}]-------{ENDC}\n")

        with open(TEMPLATE_PATH, 'r') as f:
            template_content = f.read()
        return template_content


    def load_sql(self):
        pass


    # Print SQL statement in color. 
    def print_sql(self, title, sql):
        CYAN = '\033[96m'
        ENDC = '\033[0m'
        print(f"{CYAN}SQL STATEMENT-[{title}]---------{ENDC}\n")
    
    # Print string in color.
    def print_in_colors(self, string):

        print(f"{bcolors.OKCYAN}{string}{bcolors.ENDC}\n")        


    # Commit data such as an insert
    # Be sure to check for 'RETURNING' in all uppercases. 
    def query_commit(self, sql, params={}):
        self.print_sql("commit with returning id", sql)

        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql)

        try:
            with self.pool.connection() as conn:
                cur = conn.cursor()
                cur.execute(sql, *args)

            if is_returning_id:
                returning_id = cur.fetchone()[0]
                self.print_in_colors("returning_id: ")
            else: 
                self.print_in_colors("No match found.")

            conn.commit()

            if is_returning_id:
                return returning_id

        except Exception as err:
            self.print_err(err)


    # Return a json object
    def query_json_object(self, sql, params={}):
        self.print_sql('json', sql)
        wrapped_sql = self.query_wrap_object(sql)
        
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()
                return json[0]
    
    # Return an array of json object
    def query_json_array(self, sql, params={}):
        self.print_sql("Array", sql)

        wrapped_sql = self.query_wrap_json_array(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                # this will return a tuple 
                # the first field being the data
                json = cur.fetchone()

                print("=====================PRINT ROW======================")
                for dictionary in json[0]:
                    for key, value in dictionary.items():
                        print(f"{key}: {value}")
                print("\n\n")

                return json[0]


    def query_wrap_json_object(self, template):
        self.print_sql("Object", sql)

        sql = f"""
            (SELECT COALESCE(row_to_json(object_row), '{{}}'::json) 
                FROM ({template}) object_row);
            """
        print(f"template: {template}")
        print(f"sql: {sql}")
        return sql


    def query_wrap_json_array(self, template):
        self.print_in_colors(string="QUERY_WRAP_JSON_ARRAY")
        sql = f"""
            (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))), '[]'::json) 
                FROM ({template}) array_row);
            """
        print(f"template: {template}")
        print(f"sql: {sql}")
        return sql


    def print_err(self, err):
        # Get details about the exception.
        err_type, err_obj, traceback = sys.exc_info()

        # Get the line number when exception occurred.
        line_num = traceback.tb_lineno

        # Print the connect() error
        print(f"\npsycopg2 ERROR: {err} on line number: {line_num}")
        print(f"psycopg2 traceback: {traceback} -- type: {err_type}")

        # psycopg2 extensions.Diagnostics object attribute
        print(f"\nextensions.Diagnostics: {err}") # err.diag

        # Print the pgcode and pgerror exceptions
        # print(f"pgerror: {err.pgerror}")
        # print(f"pgcode: {err.pgcode}\n")

db = DB()