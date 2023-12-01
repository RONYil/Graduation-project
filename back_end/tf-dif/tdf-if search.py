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

# 执行数据库查询，只获取 drug_name 列的数据
cursor.execute("SELECT * FROM all_data_final")
drug_names = cursor.fetchall()

# 循环查询每一个药物名称
top_n = 10
output_count = 0  # Initialize the output count
for i, drug_name_result in enumerate(drug_names):
    drug_name = drug_name_result[1]  # Assuming drug_name is in the first column, adjust as needed
    drug_id = drug_name_result[0]

    # 定义查询文档
    query_words = list(jieba.cut(drug_name))
    query_document = " ".join(query_words)

    # 向量化查询文档
    query_vector = vectorizer.transform([query_document])

    # 计算余弦相似度
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # 排序文档根据余弦相似度
    related_docs_indices = cosine_similarities.argsort()[::-1]

    # 打印相似度最高的前几个文档
    for j in range(top_n):
        if (
                cosine_similarities[related_docs_indices[j]] >= 0
                and drug_id == results[related_docs_indices[j]][0]
        ):
            output_count += 1  # Increment the output count
            print(f"Output #{output_count}")
            print(f"ID: {drug_id}")
            print(f"Drug: {drug_name}")
            print(f"Document #{j + 1}: {results[related_docs_indices[j]]}")
            print(f"Cosine Similarity: {cosine_similarities[related_docs_indices[j]]}")
            print("\n")

# 关闭数据库连接
cursor.close()
conn.close()

