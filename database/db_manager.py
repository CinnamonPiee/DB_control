import logging
from colorama import Fore, Style, init
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy import CursorResult, Engine, Inspector, MetaData, create_engine, text, inspect
from typing import Any, List


init(autoreset=True)

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


class DBManager:
    def __init__(self, dbm: str = None) -> None:
        self.engine = None
        self.metadata = MetaData()
        self.dbm: str = dbm
        self.url: str = None

    def check_dbm_url(self) -> None | str:
        if self.dbm == "MySQL":
            return "mysql+pymysql"
        
    def check_db_name(self, db_name: str, user: str, host: str, password: str) -> None | bool:
        try:
            self.url = f"{self.check_dbm_url()}://{user}:{password}@{host}"
            self.engine: Engine = create_engine(self.url, echo=False)
            with self.engine.connect() as conn:
                result: CursorResult[Any]= conn.execute(text("SHOW DATABASES;"))
                databases: list[str]= [str(row[0]) for row in result]
                if str(db_name) in databases:
                    return True
                else:
                    print(f"""Database '{db_name}' not fount in this server.You can try to write database correctly or choose one of this databases: {' '.join(databases)}.""")
                    return False
        except OperationalError as e:
            print(f"\n{Fore.RED}Error: connecting to server: {e}{Style.RESET_ALL}")
        except ProgrammingError as e:
            print(f"\n{Fore.RED}Error: connecting to server: {e.orig}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")

    def check_table_name(self, table_name: str, db_name: str, user: str, host: str, password: str) -> None | bool:
        try:
            self.url = f"{self.check_dbm_url()}://{user}:{password}@{host}/{db_name}"
            self.engine: Engine = create_engine(self.url, echo=False)
            # TODO stand here
            with self.engine.connect():
                pass
        except:
            pass

    def get_table_columns(self, db_name: str, table_name: str, user: str, host: str, password: str) -> None | list:
        try:
            self.url = f"{self.check_db_name()}://{user}:{password}@{host}/{db_name}"
            self.engine: Engine = create_engine(self.url, echo=False)
            inspector: Inspector = inspect(self.engine)
            columns: List[ReflectedColumn] = inspector.get_columns(table_name)
            columns_info: list = [(col["name"], str(col["type"])) for col in columns]
            return columns_info
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        finally:
            self.engine.dispose()
        
    def connect(self, user: str, password: str, host: str) -> None | bool:
        try:
            self.url = f"{self.check_dbm_url()}://{user}:{password}@{host}"
            self.engine: Engine = create_engine(self.url, echo=False)
            with self.engine.connect():
                print(f"\n{Fore.GREEN}Connection to server {self.dbm} established.{Style.RESET_ALL}")
            return True
        except OperationalError as e:
            print(f"\n{Fore.RED}Error: connecting to server: {e}{Style.RESET_ALL}")
        except RuntimeError:
            print(f"\n{Fore.RED}Error: Invalid password or username.{Style.RESET_ALL}")
        except ProgrammingError as e:
            print(f"\n{Fore.RED}Error: connecting to server: {e.orig}{Style.RESET_ALL}")

    def create_database(self, db_name: str, user: str, host: str, password: str) -> None:
        try:
            self.url = f"{self.check_dbm_url()}://{user}:{password}@{host}"
            self.engine: Engine = create_engine(self.url, echo=False)
            with self.engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            print(f"\n{Fore.GREEN}Database {db_name} created.{Style.RESET_ALL}")
        except OperationalError as e:
            print(f"\n{Fore.RED}Error creating database: {e.orig}{Style.RESET_ALL}")
        except RuntimeError:
            print(f"\n{Fore.RED}Error: Invalid password or username.{Style.RESET_ALL}")
        except ProgrammingError as e:
            print(f"\n{Fore.RED}Error: creating database: {e.orig}{Style.RESET_ALL}")

    def create_table(self, table_name: str, data: dict, db_name: str, user: str, host: str, password: str) -> None:
        try:
            self.url = f"{self.check_dbm_url()}://{user}:{password}@{host}/{db_name}"
            self.engine: Engine = create_engine(self.url, echo=False)
            with self.engine.connect() as conn:
                request: str = f"CREATE TABLE {table_name} (id INTEGER NOT NULL AUTO_INCREMENT, "
                for name, type in data.items():
                    request += f"{name} {type[0]} {' '.join(type[1])},"
                request += f"PRIMARY KEY (id));"
                conn.execute(text(request))
            print(f"\n{Fore.GREEN}Table {table_name} in {db_name} created.{Style.RESET_ALL}")
        except OperationalError as e:
            print(f"\n{Fore.RED}Error: connecting to server: {e}{Style.RESET_ALL}")
        except ProgrammingError as e:
            print(f"\n{Fore.RED}Error: connecting to server: {e.orig}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")