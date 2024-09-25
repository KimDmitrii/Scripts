import psycopg2
import csv


host = "*"
port = "*"
dbname = "*"
user = "*"
password = "*"


tables = [
    "AMO Сделки",
    "AMO Параметры сделок",
    "AMO Дополнительные параметры сдело",
    "AMO Справочник воронок",
    "AMO Справочник этапов продаж",
    "AMO Параметры пользователей",
    "SHD Параметры дат",
    "SHD Параметры источников данных"
]


def export_table_to_csv(cursor, table_name):
    
    query = f'SELECT * FROM "{table_name}";'
    
    
    cursor.execute(query)
    
    
    
    rows = cursor.fetchall()
    
    
    colnames = [desc[0] for desc in cursor.description]
    
    
    with open(f"{table_name}.csv", mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        
        writer.writerow(colnames)
        
        
        writer.writerows(rows)
    
    print(f"Таблица {table_name} успешно выгружена в {table_name}.csv")

try:
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    
    cur = conn.cursor()
    
    
    for table in tables:
        export_table_to_csv(cur, table)
    
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"Ошибка подключения или выполнения запроса: {e}")