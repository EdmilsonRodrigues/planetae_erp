import asyncio
from typing import Any, Dict
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
from models.exceptions import CouldNotConnectWithDatabaseException
import sys


async def initialize_database():
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
                raise CouldNotConnectWithDatabaseException(e)
        case "mongodb":
            client = AsyncIOMotorClient(host=DATABASE_HOST, port=DATABASE_PORT)
            db = client[DATABASE]
            return db
        case "sqlite3":
            raise NotImplementedError
        case _:
            raise CouldNotConnectWithDatabaseException(
                f"{DATABASE_CLIENT} is not supported."
            )


class Database:

    def __init__(self) -> None:
        self.db = None

    async def initialize(self) -> "Database":
        raise NotImplementedError

    async def create_table(self, name: str, signature: dict):
        raise NotImplementedError

    async def update_table(self, name: str, signature: dict):
        raise NotImplementedError

    async def change_table(self, name, signature: dict):
        raise NotImplementedError

    async def delete_table(self, name: str):
        raise NotImplementedError

    async def insert_document(self, document: dict):
        raise NotImplementedError

    async def update_document(self, search_key: str, search_value: Any, document: dict):
        raise NotImplementedError

    async def delete_document(self, search_key: str, search_value: Any):
        raise NotImplementedError

    async def create_index(self, key: str):
        raise NotImplementedError


class SQLDatabase(Database):
    db: mariadb.Connection
    cursor: mariadb.Cursor

    def __init__(self) -> None:
        super().__init__()
        self.cursor = None

    async def initialize(self) -> "SQLDatabase":
        return await super().initialize()

    async def create_table(self, name: str, signature: Dict[str, str]) -> bool:
        query = f"CREATE DATABASE IF NOT EXISTS {name} ("
        index = None
        for variable, sig in signature.items():
            if "PRIMARY KEY" in sig:
                index = variable
                sig = sig.replace("PRIMARY KEY,", ",")
            query += f"{variable} {sig},"
        if index is None:
            index = "id"
            query = query.split("(")
            id_index = "(id int NOT NULL AUTO_INCREMENT,"
            query = "".join((query[0], id_index, query[1]))
        query += f"PRIMARY KEY({index})"
        query += ") default charset=utf8mb4;"
        try:
            self.cursor.execute(query)
            return True
        except Exception as e:
            return False

    async def update_table(self, name: str, signature: dict):
        raise NotImplementedError

    async def change_table(self, name, signature: dict):
        raise NotImplementedError

    async def delete_table(self, name: str) -> bool:
        try:
            self.cursor.execute(f"DROP TABLE {name};")
            return True
        except Exception:
            return False

    async def insert_document(self, document: dict):
        raise NotImplementedError

    async def update_document(self, search_key: str, search_value: Any, document: dict):
        raise NotImplementedError

    async def delete_document(self, search_key: str, search_value: Any):
        raise NotImplementedError

    async def create_index(self, key: str):
        raise NotImplementedError


class MariaDB(SQLDatabase):
    async def initialize(self) -> "MariaDB":
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
            raise CouldNotConnectWithDatabaseException(e)


class NoSQLDatabase(Database):
    pass
