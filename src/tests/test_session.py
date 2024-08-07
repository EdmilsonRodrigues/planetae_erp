import pytest
from src.session import MariaDB


@pytest.mark.asyncio
async def test_create_mariadb_table():
    global name, mariadb
    name = "test_table"
    signature = {
        "name": "varchar(30) NOT NULL",
        "phone": "char(12)",
        "email": "varchar(50) NOT NULL",
    }
    mariadb = await MariaDB().initialize()
    assert await mariadb.create_table(name=name, signature=signature)

@pytest.mark.asyncio
async def test_delete_mariadb_table():
    assert await mariadb.delete_table(name=name)
