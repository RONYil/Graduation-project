from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.metrics.pairwise import cosine_similarity
import jieba
import mysql.connector

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
vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b|\b[\u4E00-\u9FFF]+\b", min_df=1, max_df=0.8, stop_words=None, ngram_range=(1, 2))


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
query = "除湿杀虫"
print(type(query))
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
top_n = 2
for i in range(top_n):
    print(f"Document #{i + 1}: {results[related_docs_indices[i]]}")
    print(f"Cosine Similarity: {cosine_similarities[related_docs_indices[i]]}")
    print("\n")


cursor.execute("SELECT * FROM all_data_final")

results = cursor.fetchall()

# Loop through each row in the results
top_n = 4
output_count = 0  # Initialize the output count

for i in range(len(results)):
    # Process each row in the results
    drug_id = results[i][0]
    drug_name = results[i][1]

    # Process drug_name (similar to the original code)
    query_words = list(jieba.cut(drug_name))
    query_document = " ".join(query_words)

    # Transform the query into a vector
    query_vector = lsa_pipeline.transform([query_document]).flatten()

    # Transform the corpus into a vector
    corpus_vector = lsa_pipeline.transform(documents)

    # Compute the cosine similarity between the query vector and the corpus vectors
    cosine_similarities = cosine_similarity(query_vector.reshape(1, -1), corpus_vector).flatten()

    # Sort the documents by their cosine similarity to the query
    related_docs_indices = cosine_similarities.argsort()[::-1]

    # Print the top N most similar documents
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

# Close the database cursor and connection
cursor.close()
conn.close()