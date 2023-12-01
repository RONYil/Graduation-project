from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import mysql.connector

# 连接到数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='all_raw_data'
)

cursor = conn.cursor()

# 执行数据库查询
cursor.execute("SELECT * FROM all_data_final")
results = cursor.fetchall()

# 定义TF-IDF向量化器
vectorizer = TfidfVectorizer(
    token_pattern=r"(?u)\b\w+\b|\b[\u4E00-\u9FFF]+\b",
    min_df=1,
    max_df=0.8,
    stop_words=None,
    ngram_range=(1, 2)
)

# 向量化文档
documents = []
for row in results:
    row_string = ', '.join(str(item) for item in row)
    sentences = row_string.split()
    sent_words = [list(jieba.cut(sent0)) for sent0 in sentences]
    document = " ".join(" ".join(sent0) for sent0 in sent_words)
    documents.append(document)

# 训练TF-IDF模型
tfidf_matrix = vectorizer.fit_transform(documents)

# 关闭上一次的数据库连接，重新连接以获取新的查询结果
cursor.close()
cursor = conn.cursor()

cursor.execute("SELECT * FROM all_data_final")
drug_names = cursor.fetchall()

query = "气味较香"
print(type(query))
query_words = list(jieba.cut(query))
query_document = " ".join(query_words)

# Vectorized query documents
query_vector = vectorizer.transform([query_document])

# Calculate the cosine similarity
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

# Sort documents according to cosine similarity
related_docs_indices = cosine_similarities.argsort()[::-1]

top_n = 20
for i in range(top_n):
    print(f"Document #{i + 1}: {results[related_docs_indices[i]]}")
    print(f"Cosine Similarity: {cosine_similarities[related_docs_indices[i]]}")
    print("\n")

cursor.close()
conn.close()