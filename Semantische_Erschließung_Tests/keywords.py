from os.path import join, dirname, abspath

import glob
from sklearn.feature_extraction.text import CountVectorizer
import yake
from keybert import KeyBERT


# folder with keywords.py
base_dir = dirname(abspath(__file__))

# data folder
letters_folder = join(base_dir, "data", "input", "*.txt")
yake_output_folder = join(base_dir, "data", "output", "YAKE_keywords")
keybert_output_folder = join(base_dir, "data", "output", "keyBERT_keywords")
stopword_file = join(base_dir, "data", "stopwords.txt")


# Stopword list from .txt file
with open(stopword_file, "r", encoding="utf-8") as f:
    stopwords = [line.strip() for line in f]

# Load multilingual model (supports German as one of the languages) for keyBERT
kw_model = KeyBERT(model="paraphrase-multilingual-MiniLM-L12-v2")



def yake_keyword_extraction(text):
    """
    Uses the original YAKE implementation to extract keywors from a text.
    text: String
    Returns: list of tuples (keyword, score)
    """

    # With custom parameters
    custom_kw_extractor = yake.KeywordExtractor(
        lan="de",              # language
        n=3,                   # ngram size
        dedupLim=0.9,          # deduplication threshold
        dedupFunc='seqm',      # deduplication function
        windowsSize=1,         # context window
        top=10,                # number of keywords to extract
        features=None          # custom features
    )

    keywords = custom_kw_extractor.extract_keywords(text)

    return keywords



def keybert_keyword_extraction(text):


    vectorizer = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 2)
    )

    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, top_n=10)

    return keywords


def keybert_keyword_extraction_diverse(text):


    vectorizer = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 2)
    )

    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, top_n=10, use_mmr=True, diversity=0.7)

    return keywords
    



    


def main():

    i=1
    for textfile in glob.glob(letters_folder):
    
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()

            print(f"Keywords extracted with YAKE for brief{i}")
            yake_keywords = yake_keyword_extraction(text)
            yake_output_file = join(yake_output_folder, f"yake_brief{i}")
            with open(yake_output_file, "w", encoding="utf-8") as out_file:
                out_file.write('\n'.join('%s %s' % tuple for tuple in yake_keywords))


            print(f"Keywords extracted with KeyBERT for brief{i}")
            keybert_keywords = keybert_keyword_extraction(text)
            keybert_output_file = join(keybert_output_folder, f"keybert_brief{i}")
            with open(keybert_output_file, "w", encoding="utf-8") as out_file:
                out_file.write('\n'.join('%s %s' % tuple for tuple in keybert_keywords))


            print(f"Diverse keywords extracted with KeyBERT for brief{i}")
            keybert_keywords = keybert_keyword_extraction_diverse(text)
            keybert_output_file = join(keybert_output_folder, f"keybert_brief{i}_diverse")
            with open(keybert_output_file, "w", encoding="utf-8") as out_file:
                out_file.write('\n'.join('%s %s' % tuple for tuple in keybert_keywords))

            i += 1


main()
