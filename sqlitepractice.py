import sqlite3

class Database():
    
    def __init__(self):

        self.table = 'datatable'
        self.create_sql_table = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            price INTEGER,
                            quantity INTEGER);
                            """
        self.create_plc_table = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            address TEXT NOT NULL,
                            data INTEGER);
                            """
        self.create_bar_qr_table = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type TEXT NOT NULL,
                            data TEXT NOT NULL);
                            """
        self.insert_sql = f"INSERT INTO {self.table} (name, description, price, quantity) VALUES ( ? , ? , ? , ? )"
        self.insert_barcode_qr_sql = f"INSERT INTO {self.table} (type, data) VALUES ( ? , ? )"
        self.insert_plc_sql = f"INSERT INTO {self.table} (address, data) VALUES ( ? , ? )"
        self.select_sql = f"SELECT * FROM {self.table}"
        self.delete_sql = f"DELETE FROM {self.table} WHERE name = ?"
        self.update_sql = f"UPDATE {self.table} SET price = ? WHERE name = ?"
        self.inout_sql = f"UPDATE {self.table} SET quantity = ? WHERE description = ?"
        self.remove_sql = f"DROP TABLE IF EXISTS {self.table};"
        # self.select_sql = f"SELECT {code_data} FROM {self.table} WHERE {code_data} = ?"

        
        self.input = input('DB파일명을 입력하세요. : ')
        self.name = f'{self.input}.db'

    def create_table(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute(self.create_plc_table)
        conn.commit()
        conn.close()

    def insert_bar_qr(self,params=()):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute(self.insert_barcode_qr_sql,params)
        conn.commit()
        conn.close()

    def insert_plc(self,params=()):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.executemany(self.insert_plc_sql,params)
        conn.commit()
        conn.close()

    def reset_table(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute(self.remove_sql)
        conn.commit()
        conn.close()

    def compare(self,_data):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table}")
        rows = cursor.fetchall()
     
        for row in rows:
            if _data == row[2]:
                return False
            else:
                continue
        
        return True

            
    # def execute_query(params=()):
    #     db = f'{input('DB파일명을 입력하세요. : ')}.db'
    #     conn = sqlite3.connect(db)
    #     cursor = conn.cursor()
    #     if isinstance(params,list):
    #         cursor.executemany(query,params)
    #     else:
    #         cursor.execute(query,params)
    #     conn.commit()
    #     conn.close()
    
    
    # 재고 입출고 관련 메서드드
    # def inout(self,params): 
    #     db = f'{input('DB파일명을 입력하세요. : ')}.db'
    #     conn = sqlite3.connect(db)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT description,quantity FROM my_table")
    #     rows = cursor.fetchall()
    #     params = list(params)
    #     for row in rows:
    #         if row[0] == params[1]:
    #             params[0] += row[1]
            
    #     cursor.execute(self.inout_sql,params)

    #     conn.commit()
    #     conn.close()

    # def fetch_all_data():
    #     db = f'{input('DB파일명을 입력하세요. : ')}.db'
    #     conn = sqlite3.connect(db)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM my_table")
    #     rows = cursor.fetchall()
    #     # print(rows)
    #     for row in rows:
    #         print(f'id[{row[0]}] / name : {row[1]} / description : {row[2]} / price : {row[3]}] / quantity : {row[4]}')
        
    #     conn.commit()
    #     conn.close()