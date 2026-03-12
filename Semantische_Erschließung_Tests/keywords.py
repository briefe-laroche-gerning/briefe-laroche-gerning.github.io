# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Automatische Verschlagwortung / Schlagwortextraktion mit YAKE und KeyBERT #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from os.path import join, dirname, abspath
import glob

from sklearn.feature_extraction.text import CountVectorizer
import yake
from keybert import KeyBERT

from help import fix_hyphenation, sort_letters


# Ordner mit keywords.py
base_dir = dirname(abspath(__file__))

# Datei-Ordner
letters_folder = join(base_dir, "data", "input", "25_briefe_laroche", "*.txt")
yake_output_folder = join(base_dir, "data", "output", "keywords_YAKE")
keybert_output_folder = join(base_dir, "data", "output", "keywords_keyBERT")
stopword_file = join(base_dir, "data", "stopwords_keywords.txt")

# Stoppwörter aus TXT-Datei laden
with open(stopword_file, "r", encoding="utf-8") as f:
    base_stopwords = {line.strip().lower() for line in f if line.strip()}
# Wörter in Groß- und Kleinschreibung zur Liste hinzufügen
stopwords_uppercase_lowercase = base_stopwords | {word.capitalize() for word in base_stopwords}
stopwords = list(stopwords_uppercase_lowercase)

# Multilinguales Modell für KeyBERT laden (unterstützt Deutsch als eine der Sprachen)
kw_model = KeyBERT(model="paraphrase-multilingual-MiniLM-L12-v2")


def yake_keyword_extraction(text):
    """
    Nutzt den YAKE-Algorithmus, um Schlagworte aus einem Text zu extrahieren.
    text: String
    Returns: Liste von Schlagworten
    """

    custom_kw_extractor = yake.KeywordExtractor(
        n=3,                   # N-Gramm-Größe
        dedupLim=0.9,          # Deduplication threshold
        dedupFunc='seqm',      # Deduplication function
        windowsSize=1,         # Context window
        top=10,                # Anzahl der zu extrahierenden Schlagworte
        stopwords = set(stopwords)
    )

    keywords = custom_kw_extractor.extract_keywords(text)
    print(keywords)

    return [tuple[0] for tuple in keywords] # Nur Schlagworte zurückgeben, nicht ihren Score


def keybert_keyword_extraction(text):
    """
    Nutzt den KeyBERT-Algorithmus, um Schlagworte aus einem Text zu extrahieren.
    text: String
    Returns: Liste von Schlagworten
    """

    vectorizer = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 3),         # N-Gramm-Größe
        lowercase=False
    )

    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, top_n=10)

    return [tuple[0] for tuple in keywords] # Nur Schlagworte zurückgeben, nicht ihren Score


def keybert_keyword_extraction_diverse(text):
    """
    Nutzt den KeyBERT-Algorithmus mit MMR, um Schlagworte aus einem Text zu extrahieren.
    Diese sind im Vergleich zur Anwendung von purem KeyBERT diversifiziert.
    text: String
    Returns: Liste von Schlagworten
    """

    vectorizer = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 3),
        lowercase=False
    )

    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer, top_n=10, use_mmr=True, diversity=0.7)

    return [tuple[0] for tuple in keywords] # Nur Schlagworte zurückgeben, nicht ihren Score
    

def main():

    letters = glob.glob(letters_folder)
    sorted_letters = sort_letters(letters)

    i=1
    for textfile in sorted_letters:
    
        with open(textfile, "r", encoding="utf-8") as f:
            text = f.read()
            text = fix_hyphenation(text)
            print(text)

            print(f"Schlagworte mit YAKE für Brief{i} extrahiert")
            yake_keywords = yake_keyword_extraction(text)
            yake_output_file = join(yake_output_folder, f"yake_brief{i}")
            with open(yake_output_file, "w", encoding="utf-8") as out_file:
                out_file.write('\n'.join('%s' % kw for kw in yake_keywords))

            print(f"Schlagworte mit KeyBERT für Brief{i} extrahiert")
            keybert_keywords = keybert_keyword_extraction(text)
            keybert_output_file = join(keybert_output_folder, f"keybert_brief{i}")
            with open(keybert_output_file, "w", encoding="utf-8") as out_file:
                out_file.write('\n'.join('%s' % kw for kw in keybert_keywords))

            print(f"Diversifizierte Schlagworte mit YAKE für Brief{i} extrahiert")
            keybert_keywords = keybert_keyword_extraction_diverse(text)
            keybert_output_file = join(keybert_output_folder, f"keybert_brief{i}_diverse")
            with open(keybert_output_file, "w", encoding="utf-8") as out_file:
                out_file.write('\n'.join('%s' % kw for kw in keybert_keywords))

            i += 1


main()
