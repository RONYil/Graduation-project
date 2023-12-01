import sqlite3


def parse_data_block(data_block):
    parsed_data = {}
    lines = data_block.strip().split('\n')
    current_key = None

    for line in lines:
        if '：' in line:
            key, value = line.split('：', 1)
            current_key = key.strip()

            # 区分通用名和通用名称
            if current_key == '通用名':
                current_key = '通用名称'  # 将“通用名”更改为“通用名称”

            if current_key == '商品名':
                current_key = '商品名称'  # 将“商品名”更改为“商品名称”

            if current_key == '成分':
                current_key = '成份'  # 将“成分”更改为“成份”

            if current_key == '功能主治':
                current_key = '适应症'  # 将“成分”更改为“成份”

            parsed_data[current_key] = value.strip()
        else:
            # 如果当前有键，将值追加到上一个键对应的值后面
            if current_key is not None:
                parsed_data[current_key] += ' ' + line.strip()

    return parsed_data


def insert_data_into_db(data, cursor):
    cursor.execute('''
        INSERT INTO medicine_info (
            common_name, product_name, ingredients, characteristics,indication,
            usage, contraindications
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('通用名称', ''),
        data.get('商品名称', ''),
        data.get('成份', ''),
        data.get('性状', ''),
        data.get('适应症', ''),
        data.get('用法用量', ''),
        data.get('禁忌', '')
    ))


# 数据库连接
conn = sqlite3.connect('all_raw_data_final.db')
cursor = conn.cursor()

# 创建数据库表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicine_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        common_name TEXT,
        product_name TEXT,
        ingredients TEXT,
        characteristics TEXT,
        indication TEXT,
        usage TEXT,
        contraindications TEXT
    )
''')

# 从文件中读取数据块并插入数据库
with open('separator_output.txt', 'r', encoding='utf-8') as file:
    data_blocks = file.read().split('\n\n\n')  # 使用三个换行符作为数据块分隔
    for data_block in data_blocks:
        data = parse_data_block(data_block)
        insert_data_into_db(data, cursor)

# 提交更改并关闭连接
conn.commit()
conn.close()