import asyncio
from typing import Any
import mysql.connector
from motor.motor_asyncio import AsyncIOMotorClient
import mariadb
import mysql.connector.cursor
from src.config import (
    DATABASE_CLIENT,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE,
)
from src.models.exceptions import CouldNotConnectWithDatabaseException
import src.logger


async def initialize_database() -> Any:
    match DATABASE_CLIENT:
        case "mysql":
            try:
                if DATABASE is None:
                    conn = mariadb.connect(
                        user=DATABASE_USERNAME,
                        password=DATABASE_PASSWORD,
                        host=DATABASE_HOST,
                        port=DATABASE_PORT,
                    )
                    cursor = conn.cursor()
                    cursor.execute(
                        "CREATE DATABASE planetae CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                    )
                    cursor.close()
                    conn.close()
                db = mysql.connector.connect(
                    user=DATABASE_USERNAME,
                    password=DATABASE_PASSWORD,
                    host=DATABASE_HOST,
                    database=DATABASE,
                )
                return db
            except Exception as e:
                src.logger.log_exception(CouldNotConnectWithDatabaseException(str(e)))
        case "mongodb":
            client = AsyncIOMotorClient(host=DATABASE_HOST, port=DATABASE_PORT)
            db = client[DATABASE]
            return db
        case "sqlite3":
            src.logger.log_exception(NotImplementedError)
        case _:
            src.logger.log_exception(
                CouldNotConnectWithDatabaseException(
                    f"{DATABASE_CLIENT} is not supported."
                )
            )


class Database:

    def __init__(self) -> None:
        self.db = None

    async def initialize(self) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def create_table(self, name: str, signature: dict) -> bool:
        src.logger.log_exception(NotImplementedError)
        return False

    async def add_collumn_to_table(self, table_name: str, signature: dict, after: str | None = None, first: bool = False) -> bool:
        src.logger.log_exception(NotImplementedError)
        return False

    async def remove_collumn_from_table(self, table_name: str, key: str) -> bool:
        src.logger.log_exception(NotImplementedError)
        return False

    async def change_table(self, name, signature: dict) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def delete_table(self, name: str) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def insert_document(self, table_name: str, document: dict) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def update_document(
        self, table_name: str, search_key: str, search_value: Any, document: dict
    ) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def delete_document(self, table_name: str, search_key: str, search_value: Any) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def create_index(self, table_name: str, key: str) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def find_document(self, table_name: str, query: dict[str, Any]) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def find_documents(self, table_name: str, query: dict[str, Any]) -> list[Any]:  # type: ignore
        src.logger.log_exception(NotImplementedError)


class SQLDatabase(Database):
    db: mariadb.Connection
    cursor: mariadb.Cursor

    def __init__(self) -> None:
        super().__init__()
        self.cursor = None

    async def initialize(self) -> Any:
        return await super().initialize()

    async def create_table(
        self, name: str, signature: dict[str, str], force: bool = False
    ) -> bool:
        """
        Creates a table in a SQL Database.

        :param #! learn how to do this
        """
        query = f"CREATE TABLE {name} (\n"
        index = None
        for variable, sig in signature.items():
            if "PRIMARY KEY" in sig:
                index = variable
                sig = sig.replace("PRIMARY KEY,", ",")
            query += f"{variable} {sig},\n"
        if index is None:
            index = "id"
            query = query.split("(\n")
            id_index = "(\nid int NOT NULL AUTO_INCREMENT,\n"
            query = "".join((query[0], id_index, query[1]))
        query += f"PRIMARY KEY({index})"
        query += ") default charset=utf8mb4;"
        try:
            if force is True:
                force_query = f"DROP TABLE IF EXISTS {name};"
                self.cursor.execute(force_query)
                src.logger.log_string(f"Dropped table {name} if it existed")
            self.cursor.execute(query)
            src.logger.log_string(f"Created table {name}")
            return True
        except Exception as e:
            src.logger.log_exception(e)
            return False

    async def add_collumn_to_table(self, table_name: str, signature: dict, after: str | None = None, first: bool = False) -> bool:
        item = tuple(signature.items())
        sig = f"{item[0]} {item[1]}"
        af = ""
        fi = "" 
        if after is not None:
            af += f" after {after}"
        elif first:
            fi += f" first"
        query = "ALTER TABLE " + table_name + " ADD COLLUMN " +  sig + af + fi + ";"
        try:
            self.cursor.execute(query)
            src.logger.log_string(f"Column {sig} added to table {table_name}" + af + fi)
            return True
        except Exception as e:
            src.logger.log_exception(e)
            return False

    async def remove_collumn_from_table(self, table_name: str, key: str) -> bool:
        query = "ALTER TABLE " + table_name + " DROP COLLUMN " + key + ";"
        try:
            self.cursor.execute(query)
            src.logger.log_string(f"Collumn {key} dropped from the table.")
            return True
        except Exception as e:
            src.logger.log_exception(e)
            return False
    
    async def change_signature_from_column(self, table_name: str, signature: dict):
        item = tuple(signature.items())
        query = "ALTER TABLE " + table_name + " " + item[0]

    async def change_table(self, name, signature: dict) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def delete_table(self, name: str) -> bool:
        try:
            self.cursor.execute(f"DROP TABLE {name};")
            src.logger.log_string(f"Dropped table {name}")
            return True
        except Exception:
            return False

    async def insert_document(self, table_name: str, document: dict) -> Any:
        pass

    async def update_document(
        self, table_name: str, search_key: str, search_value: Any, document: dict
    ) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def delete_document(self, table_name: str, search_key: str, search_value: Any) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def create_index(self, table_name: str, key: str) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def find_document(self, table_name: str, query: dict[str, Any]) -> Any:
        src.logger.log_exception(NotImplementedError)

    async def find_documents(self, table_name: str, query: dict[str, Any]) -> list[Any]:  # type: ignore
        src.logger.log_exception(NotImplementedError)


class MariaDB(SQLDatabase):
    async def initialize(self) -> "MariaDB | None":
        try:
            if DATABASE is None:
                conn = mariadb.connect(
                    user=DATABASE_USERNAME,
                    password=DATABASE_PASSWORD,
                    host=DATABASE_HOST,
                    port=DATABASE_PORT,
                )
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE planetae;")
                cursor.close()
                conn.close()
            self.db: mariadb.Connection = mariadb.connect(
                user=DATABASE_USERNAME,
                password=DATABASE_PASSWORD,
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database=DATABASE,
            )
            self.cursor: mariadb.Cursor = self.db.cursor()
            return self
        except mariadb.Error as e:
            src.logger.log_exception(CouldNotConnectWithDatabaseException(str(e)))


class NoSQLDatabase(Database):
    pass
