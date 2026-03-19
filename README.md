# briefe-laroche-gerning.github.io

Dieses Repository gehört zur Masterarbeit "Digitale Edition der Briefe Sophie von La Roches an Johann Isaak von Gerning (1795–1800): Möglichkeiten der semantischen Erschließung". an der Universität Trier.<br>
März 2026, Rachel Georg, Betreuung: Dr. Claudia Bamberg und Prof. Dr. Christof Schöch

## Projektstruktur

Der Ordner **docs** enthält den Webseiten-Build für Github-Pages, erreichbar unter https://briefe-laroche-gerning.github.io/

Der Ordner **Webseite** enthält alle Dateien der Webseite der digitalen Edition.
Um die Webseite lokal zu bauen, kann im Ordner **Webseite\briefedition** der Befehl "npm run serve" verwendet werden (siehe dazu auch die README-Datei in diesem Ordner). Die TEI-Dateien der Briefe, sowie die Register-Dateien liegen in **Webseite\briefedition\public\data**. Hier finden sich auch die XSLT-Dateien, um die TEI-Dateien in HTML- bzw. JSON-Dateien umzuwandeln.

Der Order **Semantische_Erschließung_Tests** enthält alle Python-Skripte, die zum Testen der verschiedenen Methoden der semantischen Erschließung der Briefe (Automatische Schlagwort-Extraktion, Topic Modeling, Schlagwort-Annotation mit Large Language Models) verwendet wurden. **data** enthält hierbei die Ergebnisse der manuellen Erschließung, sowie alle Input- und Output-Dateien der getesteten digitalen Methoden. Der Input-Ordner enthält die 25 Briefe Sophie von La Roches ohne Empfangsadresse und -bestätigung als TXT-Dateien mit originalen Zeilenumbrüchen, sowie die für das Topic Modeling hinzugefügten TXT-Dateien der Brieftexte aus den Korrespondenzen der Frühromantik. Der Output-Ordner enthält die Ergebnisse der verschiedenen Methoden als TXT-Dateien und zugehörige Abbildungen.

**requirements.txt** enthält alle Python-Libraries, die nötig sind, um die Tests zu reproduzieren.
