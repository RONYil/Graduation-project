import mysql.connector
from gensim.models import Word2Vec

# 加载模型
model = Word2Vec.load("word2vec_model.model")

# 建立数据库连接
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='all_raw_data'
)

# 创建游标
cursor = conn.cursor()

# Get words similar to "rong chang"
similar_words = model.wv.most_similar("荣昌", topn=3)
print(similar_words)

# Query statement
query = (
    "SELECT * FROM all_data_final WHERE "
    "CONCAT(common_name, ' ', product_name, ' ', characteristics, ' ', "
    "indication, ' ', `usage`, ' ', contraindications) LIKE %s"
)


# Iterate over similar words and execute the query
for similar_word, _ in similar_words:
    cursor.execute(query, (f"%{similar_word}%",))
    result = cursor.fetchall()

    # Processing query results
    if result:
        print(f"Results for {similar_word}:")
        for row in result:
            print(row)

# 关闭游标和数据库连接
cursor.close()
conn.close()