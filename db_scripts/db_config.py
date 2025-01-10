import asyncpg

class Database:
    def __init__(self, user, password, database, host="localhost", port=5432) -> None:
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.pool = None
        
    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=f'postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
    
    async def close(self):
        await self.pool.close()
        
    async def create_table(self, table_name):
        await self.connection.execute(
            f"""CREATE TABLE {table_name} (
                    id SERIAL PRIMARY KEY,
                    symbol VARCHAR(10) NOT NULL,
                    price DECIMAL NOT NULL,
                    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
        )
    
    async def select_from(self, columns, table_name):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(
                f"SELECT {columns} FROM {table_name};"
            )
            return result
            
    async def select_modifier_from(self, modifier, column, table_name):
        async with self.pool.acquire() as connection:
            result = await connection.fetch(
                f"SELECT {modifier}({column}) FROM {table_name};"
            )
            return result

    async def insert_into(self, table_name, columns, values):
        columns = ', '.join(columns)
        print(f"INSERT INTO {table_name} ({columns}) VALUES {values};")
        async with self.pool.acquire() as connection:
            await connection.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES {values};"
        )
