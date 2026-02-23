from lxml import etree
import json

letters = []

# -------------------------
# HTML-Transformation
# -------------------------
for i in range(1, 26):
    xml = etree.parse(f"brief{i}_tei.xml")
    xsl = etree.parse("transform_text.xsl")

    transform = etree.XSLT(xsl)
    html = transform(xml)

    with open(f"../briefe_html/brief{i}.html", "w", encoding="utf-8") as f:
        f.write(str(html))


# -------------------------
# JSON-Transformation + Fusion
# -------------------------
for i in range(1, 26):
    xml = etree.parse(f"brief{i}_tei.xml")
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    # Register-Entitäten extrahieren
    persons = set() # Duplikate verhindern
    for el in xml.xpath("//tei:persName", namespaces=ns):
        if el.get("key"):
            persons.add(el.get("key"))
        if el.get("ref"):
            for token in el.get("ref").split():
                if token.startswith("person"):          # Nur Personen-Nummern übernehmen, nicht GND-Links aus dem Header
                    persons.add(token)

    places = {
        el.get("key")
        for el in xml.xpath("//tei:placeName[@key]", namespaces=ns)
    }

    works = {
        el.get("key")
        for el in xml.xpath("//tei:name[@type='work'][@key]", namespaces=ns)
    }

    xsl = etree.parse("transform_tei_header.xsl")
    transform = etree.XSLT(xsl)
    result = transform(xml)

    json_string = str(result)
    data = json.loads(json_string)

    data["nr"] = i

    # Entitäten hinzufügen
    data["register_entities"] = {
        "persons": sorted(persons),
        "places": sorted(places),
        "works": sorted(works)
    }

    # einzelnes JSON schreiben
    with open(f"../briefe_json/brief{i}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Zur Gesamt-JSON hinzufügen
    letters.append(data)


with open("../briefe_json/alle_briefe.json", "w", encoding="utf-8") as f:
    json.dump(letters, f, ensure_ascii=False, indent=2)
