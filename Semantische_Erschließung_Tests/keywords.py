from os.path import join, dirname, abspath
import glob

from sklearn.feature_extraction.text import CountVectorizer
import yake
from keybert import KeyBERT

from help import fix_hyphenation, sort_letters


# folder with keywords.py
base_dir = dirname(abspath(__file__))

# data folder
letters_folder = join(base_dir, "data", "input", "25_briefe", "*.txt")
yake_output_folder = join(base_dir, "data", "output", "YAKE_keywords")
keybert_output_folder = join(base_dir, "data", "output", "keyBERT_keywords")
stopword_file = join(base_dir, "data", "stopwords_keywords.txt")


# Stopword list from .txt file
# with open(stopword_file, "r", encoding="utf-8") as f:
#    stopwords = [line.strip() for line in f]

with open(stopword_file, "r", encoding="utf-8") as f:
    base_stopwords = {line.strip().lower() for line in f if line.strip()}

stopwords_uppercase_lowercase = base_stopwords | {word.capitalize() for word in base_stopwords}

stopwords = list(stopwords_uppercase_lowercase)

print(stopwords)


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
        n=3,                   # ngram size
        dedupLim=0.9,          # deduplication threshold
        dedupFunc='seqm',      # deduplication function
        windowsSize=1,         # context window
        top=10,                # number of keywords to extract
        stopwords = set(stopwords)
    )

    keywords = custom_kw_extractor.extract_keywords(text)

    print(keywords)

    return [tuple[0] for tuple in keywords] # Only return keywords, not score



def keybert_keyword_extraction(text):


    vectorizer = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 3),
        lowercase=False
    )

    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, top_n=10)

    return [tuple[0] for tuple in keywords] # Only return keywords, not score


def keybert_keyword_extraction_diverse(text):


    vectorizer = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 3),
        lowercase=False
    )

    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, top_n=10, use_mmr=True, diversity=0.7)

    return [tuple[0] for tuple in keywords] # Only return keywords, not score
    



    


def main():

    letters = glob.glob(letters_folder) # glob does not sort the files in the directory
    sorted_letters = sort_letters(letters)

    i=1
    for textfile in sorted_letters:
    
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()
            text = fix_hyphenation(text)
            print(text)

            print(f"Keywords extracted with YAKE for brief{i}")
            yake_keywords = yake_keyword_extraction(text)
            yake_output_file = join(yake_output_folder, f"yake_brief{i}")
            with open(yake_output_file, "w", encoding="utf-8") as out_file:
                #out_file.write('\n'.join('%s %s' % tuple for tuple in yake_keywords))
                out_file.write('\n'.join('%s' % kw for kw in yake_keywords))


            print(f"Keywords extracted with KeyBERT for brief{i}")
            keybert_keywords = keybert_keyword_extraction(text)
            keybert_output_file = join(keybert_output_folder, f"keybert_brief{i}")
            with open(keybert_output_file, "w", encoding="utf-8") as out_file:
                #out_file.write('\n'.join('%s %s' % tuple for tuple in keybert_keywords))
                out_file.write('\n'.join('%s' % kw for kw in keybert_keywords))



            print(f"Diverse keywords extracted with KeyBERT for brief{i}")
            keybert_keywords = keybert_keyword_extraction_diverse(text)
            keybert_output_file = join(keybert_output_folder, f"keybert_brief{i}_diverse")
            with open(keybert_output_file, "w", encoding="utf-8") as out_file:
                #out_file.write('\n'.join('%s %s' % tuple for tuple in keybert_keywords))
                out_file.write('\n'.join('%s' % kw for kw in keybert_keywords))


            i += 1


main()
