<template>
<!-- HINWEIS: Der Inhalt des <script>-Blocks dieser Datei wurde Schritt für Schritt mithilfe von GPT-5 generiert und anschließend überarbeitet und kommentiert. -->
  
  <div class="letters-overview container">

    <h1>Briefübersicht</h1>

    <!-- Filter (nach Metadaten) -->
    <div class="filters row mb-4">
      <div class="col-md-3">
        <h5>Jahr</h5>
        <select v-model="selectedYear" class="form-select">
          <option value="">Alle</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>

      <div class="col-md-3">
        <h5>Absendeort</h5>
        <select v-model="selectedSenderLocation" class="form-select">
          <option value="">Alle</option>
          <option v-for="location in sender_locations" :key="location" :value="location">
            {{ location }}
          </option>
        </select>
      </div>

      <div class="col-md-3">
        <h5>Empfangsort</h5>
        <select v-model="selectedRecipientLocation" class="form-select">
          <option value="">Alle</option>
          <option v-for="location in recipient_locations" :key="location" :value="location">
            {{ location }}
          </option>
        </select>
      </div>

      <div class="col-md-3">
        <h5>Typ</h5>
        <select v-model="selectedManuscriptType" class="form-select">
          <option value="">Alle</option>
          <option v-for="type in manuscript_types" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>
    </div>
  
    <!-- Schlagwort-Filter (Buttons) -->
    <h5>Keywords</h5>
    <div class="keyword-filter">
      <div v-for="(group, groupKey) in keywordGroups" :key="groupKey" class="keyword-group">
        <span v-for="kw in group" :key="kw.label" class="keyword-badge"
          :class="[kw.cssClass, { active: selectedKeywords.includes(kw.label) }]" @click="toggleKeyword(kw.label)">
          {{ kw.label }}
        </span>
      </div>
    </div>
    <br>

    <!-- Listenanzeige der Briefe (geordnet aufsteigend nach Nummer, also nach Datum) -->
    <div class="letters-list">

      <!-- Eine Zeile pro Brief-->
      <div v-for="letter in filteredLetters" :key="letter.nr" class="row align-items-center letter-row mb-3">

        <!-- Vorschaubild -->
        <div class="col-sm-1">
          <router-link :to="{ name: 'brief', params: { nr: letter.nr } }" class="letter-link">
            <img :src="`/img/digitalisate/brief${letter.nr}_1.jpg`" class="thumbnail" alt="Kein Bild vorhanden"/>
          </router-link>
        </div>

        <!-- Datum, Absendeort, Empfangsort -->
        <div class="col-sm-3 meta">
          <div class="date">
            Datum: {{ letter.date }}
          </div>
          <div class="places">
            Absendeort: {{ letter.sender.place }}<br>
            Empfangsort: {{ letter.recipient.place || 'Keine Angabe' }}
          </div>
        </div>

        <!-- Keywords -->
        <div class="col-sm-7">
          <div class="keywords"> <!-- Klasse für wird dynamisch erstellt (Schlagworthierarchie gibt Tiefe des Farbtons an) -->
            <span v-for="kw in letter.keywords" :key="kw.label" class="keyword-badge" :class="'kw-' + keywordCategory(kw.label)">
              {{ kw.label }}
            </span>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>



<script>
import { KEYWORD_CATEGORIES, ALL_KEYWORDS, KEYWORD_TREE } from "./keyword_categories.js";

export default {
  data() {
    return {
      letters: [],                      //Liste der Briefe
      selectedYear: "",                 //Aktuell ausgewählte Filteroptionen
      selectedSenderLocation: "",
      selectedRecipientLocation: "",
      selectedManuscriptType: "",
      selectedKeywords: [],
      selectedCategories: []            //Durch Schlagwort-Filter ausgewählte Oberkategorien
    };
  },

  // Metadaten aller Briefe laden
  async mounted() {
    const res = await fetch("/data/briefe_json/alle_briefe.json");
    this.letters = await res.json();
  },

  computed: {
    // Alle Schlagworte als Liste
    ALL_KEYWORDS() {
      return ALL_KEYWORDS;
    },
    // Alle Kategorien (Schlagwortkategorie + Oberbegriff oder nicht)
    KEYWORD_CATEGORIES() {
      return KEYWORD_CATEGORIES;
    },
    // Gibt die Objekte für die Schlagwort-Filter-Badges zurück
    keywordGroups() {  // Return: Objekt der Form {literatur: [{label: "Literatur", cssClass: "kw-literatur_oberkategorie", isTopLevel: true}, {...}], politik: [...], ...}
      const groups = {};
      for (const [label, category] of Object.entries(KEYWORD_CATEGORIES)) {
        // Basis-Gruppe (literatur, politik, reisen, …) und Level in Hierarchie (1, 2, 3 oder 4) bestimmen
        const [groupKey, level] = category.split('_');
        const numericLevel = parseInt(level, 10);
        // Wenn Gruppe noch nicht existiert: neue erstellen
        if (!groups[groupKey]) {
          groups[groupKey] = [];
        }
        groups[groupKey].push({
          label,
          cssClass: 'kw-' + category,
          level: numericLevel
        });
      }

      return groups;
    },
    // Verfügbare Jahre, Absende- und Empfangsorte und Handschrift-Typen
    years() {
      return ["1795", "1796", "1797", "[1797]", "1798", "1799", "1800"];
    },
    sender_locations() {
      return ["Offenbach", "[Offenbach]", "Schönebeck"]
    },
    recipient_locations() {
      return ["Frankfurt", "Weimar", "[Weimar]", "Keine Angabe"]
    },
    manuscript_types() {
      return ["Original", "Abschrift"]
    },
    // Gefilterte Briefe
    filteredLetters() {
      return this.letters.filter(letter => {
      // Filter nach Jahr
      if (this.selectedYear) {
        const year = this.extractYear(letter.date);
        if (year !== this.selectedYear) return false;
      }
      // Filter nach Absendeort
      if (this.selectedSenderLocation) {
        if (letter.sender.place !== this.selectedSenderLocation) {
          return false;
        }
      }
      // Filter nach Empfangsort
      if (this.selectedRecipientLocation) {
        const recipientLocation = letter.recipient.place || "Keine Angabe";
        if (recipientLocation !== this.selectedRecipientLocation) {
          return false;
        }
      }
      // Filter nach Manuskript-Typ
      if (this.selectedManuscriptType) {
        if (letter.object.subtype !== this.selectedManuscriptType) {
          return false;
        }
      }
      // Filter nach Keywords (rekursiv: auch Unterkategorien werden gezählt, wenn nach ihrer Oberkategorie gefiltert wird)
      if (this.selectedKeywords.length) {
        const letterKeywordLabels = letter.keywords?.map(k => k.label) || [];

        // Für jedes aktive Filter-Keyword
        for (const filterLabel of this.selectedKeywords) {

          const node = this.findNodeByLabel(KEYWORD_TREE, filterLabel); //Knoten im Baum passend zu label suchen
          // Alle passenden Keywords unter diesem Knoten
          const allowedKeywords = node
            ? this.collectKeywords(node)
            : [filterLabel];
          // Brief muss mindestens eines davon enthalten
          const matches = allowedKeywords.some(kw =>
            letterKeywordLabels.includes(kw)
          );
          if (!matches) return false;
        }
      }
      return true;
      });
    }
  },

  methods: {
    // Sammelt alle Keywords (Labels) unter einem Knoten in der Hierarchie (einer Oberkategorie), inklusive des Knotens selbst
    collectKeywords(node, result = []) {
      if (!node) return result;
      // Knoten-Label hinzufügen (falls vorhanden)
      if (node.label) {
        result.push(node.label);
      }
      // Wenn es Kinder gibt, rekursiv sammeln
      if (node.children) {
        Object.values(node.children).forEach(child =>
          this.collectKeywords(child, result)
        );
      }
      return result;
    },

    // Mapped Oberkategorie-Schlagwort auf Knoten im Baum
    findNodeByLabel(tree, label) {
      for (const node of Object.values(tree)) {
        if (node.label === label) return node;
        // Wenn Label nicht gefunden -> Suche in Kindern weiter
        if (node.children) {
          const found = this.findNodeByLabel(node.children, label);
          if (found) return found;
        }
      }
      return null;
    },

    // Aktiviert/Deaktiviert Schlagwort
    toggleKeyword(kw) {
      const i = this.selectedKeywords.indexOf(kw);
      if (i === -1) this.selectedKeywords.push(kw);
      else this.selectedKeywords.splice(i, 1);
    },

    // Sucht entweder yyyy oder [yyyy] in Datumsangabe des Briefs
    extractYear(date) {
      if (!date) return null;
      const match = date.match(/\[?\d{4}\]?$/);
      return match ? match[0] : null;
    },

    // Gibt Schlagwort-Kategorien zurück (nur Kategorien)
    keywordCategory(label) {
      return KEYWORD_CATEGORIES[label] || "default";
    }
  }
};
</script>

<style>
/* Abstand zum Rand oben und unten auf der Seite */
.letters-overview {
  margin-top: 20px;
  margin-bottom: 20px;
}

/* Vorschaubilder der Faksimiles */
.thumbnail {
  width: 80px;
  height: auto;
  border: 1px solid #ccc;
}

/* Metadaten der Briefe */
.meta {
  min-width: 180px;
}
.date {
  font-weight: bold;
}
.places {
  font-size: 0.9rem;
  color: #555;
}
.keywords {
  margin-left: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.h5 {
  font-weight: bold;
}

/* Schlagwort-Badges */
.keyword-filter {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 2rem;
}

.keyword-group {
  display: flex;
  flex-wrap: wrap; /* Unterkeywords in der Gruppe umbrechen */
  gap: 0.4rem;    /* Abstand zwischen Unterkeywords */
}

.keyword-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 0.4rem;
  font-size: 0.85rem;
  cursor: pointer;
  white-space: nowrap; /* Verhindert, dass der Text umbricht */
}

.keyword-badge.oberkategorie {
  font-weight: bold;
  margin-right: 0.5rem; /* Abstand zu Unterkeywords */
}

.keyword-badge.active { /* Aktive (angeklickte) Keywords sind dunkel eingefärbt */
  background: #333;
  color: white;
}

/* Filter */
.keyword-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

/* Keyword-Kategorien: Oberkategorien sind dunkler/gesättigter eingefärbt als Unterkategorien */

.kw-literatur_1 {
  background-color: #ad2601;
  color: #ffffff;
}

.kw-literatur_2 {
  background-color: #ca0707ae;
}

.kw-literatur_3 {
  background-color: #ca07076d;
}

.kw-beziehungen_1 {
  background-color: #f98800;
  color: #ffffff;
}

.kw-beziehungen_2 {
  background-color: #ff8c00c6;
}

.kw-beziehungen_3 {
  background-color: #ff8c0081;
}

.kw-persoenliches_1 {
  background-color: #044b8b;
  color: #ffffff;
}

.kw-persoenliches_2 {
  background-color: #044c8b88;
}

.kw-politik_1 {
  background-color: #6b0f7c;
  color: #ffffff;
}

.kw-politik_2 {
  background-color: #6c0f7c82;
}

.kw-politik_3 {
  background-color: #6c0f7c43;
}

.kw-reisen_1 {
  background-color: #3ea06d;
  color: #ffffff;
}

.kw-reisen_2 {
  background-color: #3ea06da6;
}

.kw-reisen_3 {
  background-color: #3ea06d4a;
}

.kw-emotion_1 {
  background-color: #03717bb5;
  color: #ffffff;
}

.kw-emotion_2 {
  background-color: #2cafbb6e;
}

.kw-sprechakt_1 {
  background-color: #e7b100;
  color: #ffffff;
}

.kw-sprechakt_2 {
  background-color: #f9bf00a1;
}

.kw-sprechakt_3 {
  background-color: #f9bf0065;
}

.kw-sprechakt_4 {
  background-color: #f9bf003b;
}

.kw-warensendung_1 {
  background-color: #e20372;
  color: #ffffff;
}

.kw-warensendung_2 {
  background-color: #e2037288;
}

.kw-zitat_1 {
  background-color: #753b08;
  color: #ffffff;
}

.kw-zitat_2 {
  background-color: #753b0896;
}

.kw-andere_1 {
  background-color: gray;
  color: #ffffff;
}

</style>
