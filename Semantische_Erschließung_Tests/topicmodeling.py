from os.path import join, dirname, abspath, basename
import os

from pathlib import Path
import glob
import re
from operator import itemgetter

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer



import little_mallet_wrapper as lmw
from bertopic import BERTopic

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Patch import_data function and load_topic_keys from little_mallet_wrapper to force UTF-8 writing on Windows (MALLET otherwise breaks German umlauts)
def import_data_utf8(path_to_mallet,
                path_to_training_data,
                path_to_formatted_training_data,
                training_data,
                training_ids=None,
                use_pipe_from=None):

    # Write training.txt in UTF-8!
    training_data_file = open(path_to_training_data, 'w', encoding='utf-8')
    for i, d in enumerate(training_data):
        if training_ids:
            training_data_file.write(str(training_ids[i]) + ' no_label ' + d + '\n')
        else:
            training_data_file.write(str(i) + ' no_label ' + d + '\n')
    training_data_file.close()

    if use_pipe_from:
        print('Importing data using pipe...')
        os.system(path_to_mallet + ' import-file --input "' + path_to_training_data + '"' 
                                             + ' --output "' + path_to_formatted_training_data + '"' \
                                             + ' --keep-sequence' \
                                             + ' --use-pipe-from "' + use_pipe_from + '"'
                                             + ' --preserve-case')
        
    else:
        print('Importing data...')
        os.system(path_to_mallet + ' import-file --input "' + path_to_training_data + '"' 
                                             + ' --output "' + path_to_formatted_training_data + '"' \
                                             + ' --keep-sequence'
                                             + ' --preserve-case')

    print('Complete')

lmw.import_data = import_data_utf8
lmw.quick_train_topic_model.__globals__['import_data'] = import_data_utf8

def load_topic_keys_utf8(topic_keys_path):
    return [line.split('\t')[2].split() for line in open(topic_keys_path, 'r', encoding='utf-8')]

lmw.load_topic_keys = load_topic_keys_utf8
lmw.quick_train_topic_model.__globals__['load_topic_keys'] = load_topic_keys_utf8


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #





# folder with topicmodeling.py
base_dir = dirname(abspath(__file__))

# data folder
letters_folder = join(base_dir, "data", "input", "großes_korpus", "*.txt")
# letters_folder = join(base_dir, "data", "input", "25_briefe", "*.txt")
stopword_file = join(base_dir, "data", "stopwords.txt")
output_directory_path =  join(base_dir, "data", "output", "topics")
bert_figure_directory_path =  join("Semantische_Erschließung_Tests", "data", "output", "bertopic", "images")

# path to local MALLET installation => change this if running the code on another computer
#mallet_path = join("C:", "mallet", "bin", "mallet")
mallet_path = "C:\\mallet\\bin\\mallet"





def remove_stopwords(texts_path, stopwordlist_path):
    """
    Removes stopwords from all text documents in the given folder.
    texts_path: path of the folder with the texts
    stopwordlist_path: path of the stopword list
    Returns: list of (filename, cleaned_text)
    """
    
    with open(stopwordlist_path, "r", encoding="utf-8") as f:
        stopwords = [w.strip() for w in f.readlines()]

    cleaned_texts = []
    for textfile in glob.glob(texts_path):
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()
        tokens = text.lower().split()
        tokens = [t for t in tokens if t not in stopwords]
        cleaned_text = " ".join(tokens)

        # Use cleaning function from little-mallet-wrapper
        cleaned_text = lmw.process_string(cleaned_text,
                           lowercase=True,
                           remove_short_words=True,
                           remove_stop_words=True,
                           remove_punctuation=True,
                           numbers="remove",
                           stop_words=stopwords
                           )

        filename = os.path.basename(textfile)
        cleaned_texts.append((filename, cleaned_text))

        #print(cleaned_texts)


    return cleaned_texts


def topicmodel_mallet(topic_num):
    """
    Performs topic modeling using MALLET.
    topic_num: the number of topics
    Returns: The topic model as ([...],[...])
    """

    cleaned_texts_with_names = remove_stopwords(letters_folder, stopword_file)
    # Get the names of the documents (makes it possible to later filter for letter 1 - letter 25)
    doc_names = [name for (name, _) in cleaned_texts_with_names]

    # Only the texts without filenames
    cleaned_texts = [text for (_, text) in cleaned_texts_with_names]

    num_topics=topic_num

    output_directory_path =  join(base_dir, "data", "output", "topics")

    Path(f"{output_directory_path}").mkdir(parents=True, exist_ok=True)

    topicmodel= lmw.quick_train_topic_model(path_to_mallet=mallet_path,
                                        output_directory_path=output_directory_path,
                                        num_topics=num_topics,
                                        training_data=cleaned_texts)
    
    generate_heatmap_mallet(topicmodel, doc_names)
    
    return topicmodel
    

def generate_heatmap_mallet(topicmodel_results, doc_names):

    topic_words, topic_distribution = topicmodel_results
    
    # Filter for the first 25 letters
    laroche_letters = [f"brief{i}" for i in range(1, 26)]
    filtered_indices = [
        i for i, name in enumerate(doc_names)
        if any(name.lower().startswith(letter) for letter in laroche_letters)
    ]
    filtered_topic_distribution = [topic_distribution[i] for i in filtered_indices]

    # Create labels for letters
    letter_labels = [f"Brief {i+1:02d}" for i in range(25)]

    # Create labels for topics: the first three words of a topic
    topic_labels = [
        ", ".join(words[:3])
        for words in topic_words
    ]

    #dimension=(len(filtered_doc_names), len(topic_labels))
    dimension = (25, 25)

    lmw.plot_categories_by_topics_heatmap(labels=letter_labels,
                                          topic_distributions=filtered_topic_distribution,
                                          topic_keys=topic_words,
                                          output_path=output_directory_path,
                                          target_labels=letter_labels,
                                          dim=dimension)
    

def topicmodel_BERTopic(topic_num, texts_path, stopwordlist_path):
    """
    Performs topic modeling using BERTopic.
    topic_num: the number of topics
    texts_path: The folder path of the input texts
    Returns:
    """

    # cleaned_texts = remove_stopwords(letters_folder, stopword_file)

    # Use CountVectorizer with German stopword removal
    with open(stopwordlist_path, "r", encoding="utf-8") as f:
        stopwords = f.read().splitlines()
    vectorizer_model = CountVectorizer(stop_words=stopwords)

    # Use multilingual embedding model (supports German as one of the languages)
    # embedding ="paraphrase-multilingual-MiniLM-L12-v2"
    embedding = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    # Minimum size of a topic can be:
    min_topicsize = 10
    # Use kMeans instead of HDBSCAN
    cluster_model = KMeans(n_clusters=topic_num)

    docs = []

    letters =glob.glob(texts_path)
    # Extract number from file name, listtuples (filename, number)
    letters_with_num = [
        (f, int(re.search(r'\d+', basename(f)).group()))
        for f in letters
    ]
    # Sort by number
    letters_sorted = [f[0] for f in sorted(letters_with_num, key=itemgetter(1))]

    for textfile in letters_sorted:
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(text)
    topic_model = BERTopic(vectorizer_model=vectorizer_model, embedding_model=embedding, hdbscan_model=cluster_model, min_topic_size=min_topicsize)
    topics, probabilities = topic_model.fit_transform(docs)

    print(topic_model.get_topic_info())
    doc_df = topic_model.get_document_info(docs)
    # Print the first 25 documents and their primary topic
    print(doc_df.head(25))



    topic_distr, _ = topic_model.approximate_distribution(docs)
    for i in range(25):
        
        fig = topic_model.visualize_distribution(topic_distr[i])
        fig.write_image(file=join(bert_figure_directory_path, f"brief{i}.jpg"), format="jpg")


    
    return topics, probabilities


def main():

    # topicmodel_mallet(topic_num=20)   # Perform topic modeling with 20 topics
    topicmodel_BERTopic(10, letters_folder, stopword_file)



main()

