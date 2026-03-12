# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Automatische Verschlagwortung mit LLMs via Ollama #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

from os.path import join, dirname, abspath
import glob

import ollama

from help import sort_letters


def load_systemprompt():
    """
    Läd den Systemprompt aus der TXT-Datei.
    Returns: String (Systemprompt)
    """
    # Ordner mit llm_tests.py
    base_dir = dirname(abspath(__file__))
    # Datei-Ordner
    letters_folder = join(base_dir, "data", "systemprompt.txt")
    with open(letters_folder, "r", encoding="utf-8") as f:
        return f.read()


def ollama_query_keywords(model="llama3.3:70b"):
    """
    Sendet Queries zum Verschlagworten der Briefe an das gewählte Sprachmodell.
    model: String (Name des Sprachmodells)
    """

    results = {}

    base_dir = dirname(abspath(__file__))
    # Datei-Ordner
    letters_folder = join(base_dir, "data", "input", "25_briefe_laroche", "*.txt")
    # Systemprompt
    systemprompt = load_systemprompt()

    letters = glob.glob(letters_folder)
    # Sortiere Briefe nach Nummer
    letters_sorted = sort_letters(letters)

    i = 1
    for letter in letters_sorted:

        with open(letter, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Annotiere Schlagworte für {letter}...")

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": systemprompt},
                {
                    "role": "user",
                    "content": (
                        "Bitte analysiere den folgenden historischen Brieftext "
                        "und gib 1 bis 15 Schlagworte aus der definierten Liste zurück.\n\n"
                        f"{text}"
                    )
                }
            ]
        )

        content = response["message"]["content"]
        print(response.message.content)

        output_folder = join(base_dir, "data", "output", "LLM_keywords")
        output_file = join(output_folder, f"ollama_keywords_brief{i}")
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write(content)
        i = i+1


def main():

    print("Starte Schlagwortannotation...")
    ollama_query_keywords()


main()
