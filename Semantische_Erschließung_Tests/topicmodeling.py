from os.path import join, dirname, abspath
import os

from pathlib import Path
import glob
import little_mallet_wrapper as lmw


# Patch import_data function from little_mallet_wrapper to force UTF-8 writing on Windows (MALLET otherwise breaks German umlauts)
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
# zusätzlich: erzwinge die Änderung in den Globals der Funktion
lmw.quick_train_topic_model.__globals__['import_data'] = import_data_utf8





# folder with topicmodeling.py
base_dir = dirname(abspath(__file__))

# data folder
letters_folder = join(base_dir, "data", "input", "*.txt")
stopword_file = join(base_dir, "data", "stopwords.txt")




# path to local MALLET installation => change this if running the code on another computer
#mallet_path = join("C:", "mallet", "bin", "mallet")
mallet_path = "C:\\mallet\\bin\\mallet"





def remove_stopwords(texts_path, stopwordlist_path):
    """
    Removes stopwords from all text documents in the given folder.
    texts_path: path of the folder with the texts
    stopwordlist_path: path of the stopword list
    """
    
    with open(stopwordlist_path, "r", encoding="utf-8") as f:
        stopwords = set(w.strip() for w in f.readlines())

    cleaned_texts = []
    for textfile in glob.glob(texts_path):
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()
        tokens = text.lower().split()
        tokens = [t for t in tokens if t not in stopwords]
        cleaned_texts.append(" ".join(tokens))

    return cleaned_texts


def topicmodel():

    #cleaned_texts = remove_stopwords(letters_folder, stopword_file)

    cleaned_texts = []
    for textfile in glob.glob(letters_folder):
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned_texts.append(text)

    print(cleaned_texts)


    num_topics=20

    output_directory_path = "data/output/topics"
    #No need to change anything below here
    Path(f"{output_directory_path}").mkdir(parents=True, exist_ok=True)

    path_to_training_data           = f"{output_directory_path}/training.txt"
    path_to_formatted_training_data = f"{output_directory_path}/mallet.training"
    path_to_model                   = f"{output_directory_path}/mallet.model.{str(num_topics)}"
    path_to_topic_keys              = f"{output_directory_path}/mallet.topic_keys.{str(num_topics)}"
    path_to_topic_distributions     = f"{output_directory_path}/mallet.topic_distributions.{str(num_topics)}"

    lmw.quick_train_topic_model(path_to_mallet=mallet_path,
                                output_directory_path=output_directory_path,
                                num_topics=num_topics,
                                training_data=cleaned_texts)


def main():

    topicmodel()



main()

