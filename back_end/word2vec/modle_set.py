import mysql.connector
import nltk
import jieba
from nltk.corpus import stopwords
from gensim.models import Word2Vec

nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('chinese'))

# 使用with语句确保连接在退出时关闭
with mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='all_raw_data'
) as conn:
    with conn.cursor() as cursor:
        # 执行查询
        cursor.execute("SELECT * FROM all_data_final")

        # 获取数据
        data = cursor.fetchall()

        def preprocess_text_chinese(row):
            # 将每个字段的文本合并为一个字符串
            full_text = ' '.join(map(str, row[1:]))

            # 将文本转换为字符串
            full_text = str(full_text)

            words = [word.lower() for word in jieba.cut(full_text) if word.isalpha() and word.lower() not in stop_words]
            if not words:
                print(f"Empty words after preprocessing for text: {full_text}")
            return words

        # 对每条中文文本进行预处理
        processed_data_chinese = [preprocess_text_chinese(row) for row in data]

        # 输出处理后的数据
        print(processed_data_chinese)

        # 训练Word2Vec模型
        model = Word2Vec(sentences=processed_data_chinese, vector_size=100, window=5, min_count=1, workers=4)

        # 构建词汇表
        model.build_vocab(processed_data_chinese)

        # 训练Word2Vec模型
        model.train(processed_data_chinese, total_examples=model.corpus_count, epochs=10)

        # 保存模型
        model.save("word2vec_model.model")

