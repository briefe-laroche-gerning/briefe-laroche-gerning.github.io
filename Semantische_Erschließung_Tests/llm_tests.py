from os.path import join, dirname, abspath, basename
import glob
import requests
import re
from operator import itemgetter

import ollama
from ollama import ChatResponse


"""
def get_installed_models():
    url = "http://localhost:11434/api/tags"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return [m["name"] for m in data.get("models", [])]
"""


def load_systemprompt():
    # folder with llm_tests.py
    base_dir = dirname(abspath(__file__))
    # data folder
    letters_folder = join(base_dir, "data", "systemprompt.txt")
    with open(letters_folder, "r", encoding="utf-8") as f:
        return f.read()


def ollama_query_keywords(model="llama3.3:70b"):

    results = {}

    # folder with llm_tests.py
    base_dir = dirname(abspath(__file__))
    # data folder
    letters_folder = join(base_dir, "data", "input", "25_briefe", "*.txt")
    # system prompt text
    systemprompt = load_systemprompt()

    letters = glob.glob(letters_folder)

    # Extract number from file name, listtuples (filename, number)
    letters_with_num = [
        (f, int(re.search(r'\d+', basename(f)).group()))
        for f in letters
    ]
    print(letters_with_num)

    # Sort by number
    letters_sorted = [f[0] for f in sorted(letters_with_num, key=itemgetter(1))]

    i = 1
    for letter in letters_sorted:

        with open(letter, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Extracting keywords for {letter}...")

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": systemprompt},
                {
                    "role": "user",
                    "content": (
                        "Bitte analysiere den folgenden historischen Brieftext "
                        "und gib 1 bis 10 Schlagworte aus der definierten Liste zurück.\n\n"
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

    print("Starting keyword extraction with qwen...")

    """
    ['qwen2.5:32b', 'deepseek-r1:32b', 'qwen2.5:latest', 'llama3.3:70b',
    'qwen2.5:72b', 'deepseek-r1:70b', 'codellama:70b', 'gemma2:27b', 'deepseek-r1:7b',
    'deepseek-r1:14b', 'mistral-small3.2:24b', 'qwen3:30b', 'gemma3:27b',
    'mistral-small3.1:24b', 'deepseek-coder:33b', 'qwen3-coder:30b', 'llama3.1:8b',
    'llama3.3:latest', 'deepseek-v3:latest', 'scomper/llama3-zh-inst:latest',
    'llama3.2:latest', 'llama3.1:70b', 'llama3.2-vision:90b', 'llama3.1:405b', 'llama3:70b']
    """
    ollama_query_keywords()


main()
