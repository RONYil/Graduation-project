# app.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/demo2', methods=['POST'])
def receive_data():
    try:
        # 获取小程序发送的数据
        data_from_mini_program = request.json.get('data')

        # 调试输出
        print(f"Received data from mini program: {data_from_mini_program}")
        print(f"Data type: {type(data_from_mini_program)}")

        # 在这里进行你的处理，运行你的项目，并获取结果
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='all_raw_data'
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM all_data_final")

        results = cursor.fetchall()

        # Define the LSA model with a smaller number of components
        svd_model = TruncatedSVD(n_components=100)

        # Define the vectorizer
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b|\b[\u4E00-\u9FFF]+\b", min_df=1, max_df=0.8,
                                     stop_words=None, ngram_range=(1, 2))

        # Define the LSA pipeline
        lsa_pipeline = make_pipeline(vectorizer, svd_model)

        # Fit the LSA model to the corpus
        documents = []
        for row in results:
            row_string = ', '.join(str(item) for item in row)
            sentences = row_string.split()
            sent_words = [list(jieba.cut(sent0)) for sent0 in sentences]
            document = " ".join(" ".join(sent0) for sent0 in sent_words)
            documents.append(document)

        # Fit the LSA model to the corpus
        lsa_pipeline.fit(documents)

        n_components_used = lsa_pipeline.named_steps['truncatedsvd'].n_components

        # Define the query
        query = data_from_mini_program

        query_words = list(jieba.cut(query))
        query_document = " ".join(query_words)

        # Transform the query into a vector
        query_vector = lsa_pipeline.transform([query_document]).flatten()

        # Transform the corpus into a vector
        corpus_vector = lsa_pipeline.transform(documents)

        # Now both query_vector and corpus_vector should have the same length
        # Compute the cosine similarity between the query vector and the corpus vectors
        cosine_similarities = cosine_similarity(query_vector.reshape(1, -1), corpus_vector).flatten()

        # Sort the documents by their cosine similarity to the query
        related_docs_indices = cosine_similarities.argsort()[::-1]

        # Print the top 3 most similar documents

        send_date = f"Document #{1}: {results[related_docs_indices[0]]}"
        print(send_date)
        print(type(send_date))
        top_n = 1
        for i in range(top_n):
            print(f"Document #{i + 1}: {results[related_docs_indices[i]]}")
            print(f"Cosine Similarity: {cosine_similarities[related_docs_indices[i]]}")
            print("\n")
        # 以下是一个简单的示例，将收到的数据返回给小程序
        result = send_date

        # 返回结果给小程序
        return jsonify({"success": True, "result": result, "received_data": data_from_mini_program, "data_type": str(type(data_from_mini_program))})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
