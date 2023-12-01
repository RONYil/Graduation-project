Description
The aim of the project is to create a drug inquiry platform based on China's diverse environment. It aims to help immigrants with communication problems use and understand drugs in their daily lives and prevent the dangers caused by misuse of drugs. Based on MYSQL database, this project uses NLP algorithm for keyword analysis (and compares various algorithms through the data obtained by operation) to provide patients with targeted drug information.

A.Back-end, algorithm test comparison(python)
datafix(The raw data is processed and a database is generated):
        1.all_raw_data.txt indicates raw data
        2.It is processed by 1.Data-deletion.py to get Data_deletion_output.txt
        3.Then launch 2.separator.py to get separator_output.txt
        4.Finally run 3.Database_modification_storage.py to get all_raw_data_final.db

topn:The amount of information obtained by the user.
lsa(The linear algebraic relationship between lsa algorithm query keywords, LSA and topn is realized):
        lsa search.py:Implement lsa query keywords
        lsa test.py:The relationship between lsa algorithm query keywords and topn
        Lagrange_interpolation.py:The function is obtained by Lagrange interpolation


tf-idf(The linear algebraic relationship between tf-idf algorithm query keywords, tf-idf and topn is realized):
        tdf-if search.py:Implement tf-idf query keywords
        tdf-if test.py:The relationship between tf-idf algorithm query keywords and topn

word2vec(Build a word2vec model and use the model to query keywords):
        modle_set.py:Construct word2vec model based on database
        word2vec_model.model:Generated model
        word2vec_search.py:Implement query

Back_end_connection.py:The back-end. It needs to run the back end first, and then use the front end.

B.Front-end construction(Run through wechat developer platform)
Use the wechat developer platform to open the front-end folder to run.(warning:There are parts of the code that call the API, which may require the use of a VPN)