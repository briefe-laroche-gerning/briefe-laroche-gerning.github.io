# # # # # # # # # # # # # # # #
# Topicmodeling mit BERTopic  #
# # # # # # # # # # # # # # # #

from os.path import join, dirname, abspath

import glob
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic

from help import fix_hyphenation, sort_letters


# Ordner mit topicmodeling.py
base_dir = dirname(abspath(__file__))

# Datei-Ordner
letters_folder = join(base_dir, "data", "input", "großes_korpus", "*.txt")
stopword_file = join(base_dir, "data", "stopwords_topicmodel.txt")
bert_output_directory_path =  join("Semantische_Erschließung_Tests", "data", "output", "topicmodeling_bertopic", "bertopic")


def topicmodel_BERTopic(topic_num, texts_path, stopwordlist_path, nr):
    """
    Wendet Topic Modeling mit BERTopic an.
    topic_num: Anzahl Topics
    texts_path: Pfad zu den Input-Texten
    stopwordlist_path: Pfad zur Stoppwort-Datei
    nr: Anzahl der Topics
    """

    # CountVectorizer mit eigener Stoppwortliste
    with open(stopwordlist_path, "r", encoding="utf-8") as f:
        stopwords = f.read().splitlines()
    vectorizer_model = CountVectorizer(stop_words=stopwords)

    # Multilinguales Embedding-Modell (unterstützt Deutsch als eine der Sprachen)
    embedding = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    # Minimale Größe eines Topics
    min_topicsize = 10
    # Nutze kMeans anstatt HDBSCAN als Clustering-Algorithmus
    cluster_model = KMeans(n_clusters=topic_num)

    docs = []

    letters =glob.glob(texts_path)
    # Sortiere Briefe nach Nummer
    letters_sorted = sort_letters(letters)

    for textfile in letters_sorted:
        with open(textfile, "r", encoding="utf-8") as f:
            # Durch Bindestriche getrennte Wörter an Zeilenenden/-anfängen zusammenführen
            text = f.read()
            text = fix_hyphenation(text)
            docs.append(text)
    
    # Topic Model erstellen
    topic_model = BERTopic(top_n_words=12, vectorizer_model=vectorizer_model, embedding_model=embedding, hdbscan_model=cluster_model, min_topic_size=min_topicsize)
    topics, probabilities = topic_model.fit_transform(docs)
    # Eigene Label nutzen
    topic_labels = topic_model.generate_topic_labels(nr_words=3, separator=", ") # Topic Label sollen die ersten fünf Wörter eines Topics enthalten
    topic_model.set_topic_labels(topic_labels)

    print(topic_model.topic_sizes_)

    # Übersicht über Topics und Dokumente
    topic_info = topic_model.get_topic_info()
    topic_info.to_csv(join(bert_output_directory_path + nr, "bert_topic_info.csv"))
    doc_df = topic_model.get_document_info(docs)
    doc_df.to_csv(join(bert_output_directory_path + nr, "bert_document_info.csv"))
    
    # Übersicht über repräsentative Wörter der Topics
    topics = topic_model.get_topics()
    topic_words = []
    for topic_id, words in topics.items(): # words ist eine Liste aus Tupeln (Wort, c-TF-IDF score)
        word_list = [w for w, _ in words] # Nur Wörter
        word_str  = ", ".join(word_list)
        topic_words.append({
            "topic": topic_id,
            "words": word_str
        })
    df = pd.DataFrame(topic_words) # Alle Topics mit ihren repräsentativen Wörtern in Dataframe sammeln
    df.to_csv(join(bert_output_directory_path + nr,"bertopic_topics.csv"), index=False, encoding="utf-8")

    # Topic distribution (Übersicht über mehr als nur das primary topic) visualisieren
    # Topics werden ab einem Wert von 0.05 visualisiert
    # Nur die 25 relevanten Briefe werden visualisiert
    topic_distr, _ = topic_model.approximate_distribution(docs)
    for i in range(25):
        fig = topic_model.visualize_distribution(topic_distr[i], min_probability=0.05, custom_labels=True)
        fig.write_image(file=join(bert_output_directory_path + nr, f"brief{i+1}.jpg"), format="jpg")


def main():
    print("Topic Modeling gestartet")
    for i in range(1, 10):
        print(f"Durchgang Nummer {i}")
        # BERTopic mit 10 Topics und eigener Stoppwort-Liste
        topicmodel_BERTopic(10, letters_folder, stopword_file, str(i))


main()