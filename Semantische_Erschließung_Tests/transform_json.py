import json
from os.path import join, dirname, abspath


# folder with keywords.py
base_dir = dirname(abspath(__file__))

# data folder
person_json = join(base_dir, "data", "register", "personenregister.json")
werk_json = join(base_dir, "data", "register", "werkregister.json")
ort_json = join(base_dir, "data", "register", "ortsregister.json")

new_person_json = join(base_dir, "data", "register", "personenregister_transformed.json")
new_werk_json = join(base_dir, "data", "register", "werkregister_transformed.json")
new_ort_json = join(base_dir, "data", "register", "ortsregister_transformed.json")



def transform_person_json(input_path, output_path):
    """
    Adds IDs (Numbers) to each JSON object in the file.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed = {
        f"person{i+1}": obj
        for i, obj in enumerate(data)
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=4)

    print(f"Transformed JSON was saved at {output_path}")

def transform_werk_json(input_path, output_path):
    """
    Adds IDs (Numbers) to each JSON object in the file.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed = {
        f"werk{i+1}": obj
        for i, obj in enumerate(data)
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=4)

    print(f"Transformed JSON was saved at {output_path}")

def transform_ort_json(input_path, output_path):
    """
    Adds IDs (Numbers) to each JSON object in the file.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed = {
        f"ort{i+1}": obj
        for i, obj in enumerate(data)
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=4)

    print(f"Transformed JSON was saved at {output_path}")


def main():
    transform_person_json(person_json, new_person_json)
    transform_werk_json(werk_json, new_werk_json)
    transform_ort_json(ort_json, new_ort_json)

main()
