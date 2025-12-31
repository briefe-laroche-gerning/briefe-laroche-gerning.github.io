<template>
  <div class="letters-overview container">

    <h1>Briefübersicht</h1>

    <!-- ===== Filter ===== -->
    <div class="filters row mb-4">
      <div class="col-md-12">
        <h5>Jahr</h5>
        <select v-model="selectedYear" class="form-select">
          <option value="">Alle</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>

<br>

        <h5>Keywords</h5>
      <div class="keyword-filter">
  <div
    v-for="(group, groupKey) in keywordGroups"
    :key="groupKey"
    class="keyword-group"
  >
    <span
      v-for="kw in group"
      :key="kw.label"
      class="keyword-badge"
      :class="[kw.cssClass, { active: selectedKeywords.includes(kw.label) }]"
      @click="toggleKeyword(kw.label)"
    >
      {{ kw.label }}
    </span>
  </div>
</div>


      </div>
    </div>

    <!-- ===== LISTEN-WRAPPER ===== -->
    <div class="letters-list">

      <!-- ===== EINE ZEILE = EIN BRIEF ===== -->
      <div
        v-for="letter in filteredLetters"
        :key="letter.nr"
        class="row align-items-center letter-row mb-3"
      >

        <!-- Vorschaubild -->
        <div class="col-sm-1">
          <router-link
            :to="{ name: 'brief', params: { nr: letter.nr } }"
            class="letter-link"
          >
            <img
              :src="`/img/digitalisate/brief${letter.nr}_1.jpg`"
              class="thumb"
              alt=""
            />
          </router-link>
        </div>

        <!-- Datum, Absendeort, Empfangsort -->
        <div class="col-sm-3 meta">
            <div class="date">
              Datum: {{ letter.date }}
            </div>
          <div class="places">
            Absendeort: {{ letter.sender.place }}<br>
            Empfangsort: {{ letter.recipient.place || 'Nicht bekannt' }}
          </div>
        </div>

        <!-- Keywords -->
        <div class="col-sm-7">
          <div class="keywords">
<span
  v-for="kw in letter.keywords"
  :key="kw.label"
  class="keyword-badge"
  :class="'kw-' + keywordCategory(kw.label)"
>
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
      letters: [],
      selectedYear: "",
      selectedKeywords: [],
      selectedCategories: []
    };
  },

  async mounted() {
    const res = await fetch("/data/briefe_json/alle_briefe.json");
    this.letters = await res.json();
  },

  computed: {

    ALL_KEYWORDS() {
      return ALL_KEYWORDS;
    },
    KEYWORD_CATEGORIES() {
      return KEYWORD_CATEGORIES;
    },
 keywordGroups() {
    const groups = {};

    for (const [label, cls] of Object.entries(KEYWORD_CATEGORIES)) {
      // Basis-Gruppe bestimmen (literatur, politik, reisen, …)
      const groupKey = cls.replace('_oberkategorie', '');

      if (!groups[groupKey]) {
        groups[groupKey] = [];
      }

      groups[groupKey].push({
        label,
        cssClass: 'kw-' + cls,
        isTopLevel: cls.endsWith('_oberkategorie')
      });
    }

    // optional: Oberkategorie innerhalb der Gruppe nach vorne
    Object.values(groups).forEach(group => {
      group.sort((a, b) => b.isTopLevel - a.isTopLevel);
    });

    return groups;
  },
  filterKeywords() {
    return Object.keys(KEYWORD_CATEGORIES).map(label => ({
      label,
      cssClass: 'kw-' + KEYWORD_CATEGORIES[label],
      isTopLevel: KEYWORD_CATEGORIES[label].endsWith('_oberkategorie')
    }));
  },



    /* ===== verfügbare Jahre ===== */
    years() {
      return ["1795", "1796", "1797", "[1797]", "1798", "1799", "1800"];
    },

    /* ===== gefilterte Briefe ===== */
   filteredLetters() {
  return this.letters.filter(letter => {

    /* ===== Jahr ===== */
    if (this.selectedYear) {
      const year = this.extractYear(letter.date);
      if (year !== this.selectedYear) return false;
    }

    /* ===== Keywords (rekursiv!) ===== */
    if (this.selectedKeywords.length) {

      const letterKeywordLabels =
        letter.keywords?.map(k => k.label) || [];

      // für jedes aktive Filter-Keyword
      for (const filterLabel of this.selectedKeywords) {

        const node = this.findNodeByLabel(KEYWORD_TREE, filterLabel);

        // alle passenden Keywords unter diesem Knoten
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
    /* Sammelt alle Keywords unter einem Knoten in der Hierarchie (einer Oberkategorie) */
/* Sammelt alle Labels unter einem Knoten inklusive des Knotens selbst */
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

/* Mapped Oberkategorie auf Knoten im Baum */
findNodeByLabel(tree, label) {
  for (const node of Object.values(tree)) {
    if (node.label === label) return node;

    if (node.children) {
      const found = this.findNodeByLabel(node.children, label);
      if (found) return found;
    }
  }
  return null;
},


      toggleKeyword(kw) {
    const i = this.selectedKeywords.indexOf(kw);
    if (i === -1) this.selectedKeywords.push(kw);
    else this.selectedKeywords.splice(i, 1);
  },

  toggleCategory(cat) {
    const i = this.selectedCategories.indexOf(cat);
    if (i === -1) this.selectedCategories.push(cat);
    else this.selectedCategories.splice(i, 1);
  },
    extractYear(date) {
  if (!date) return null;

  // sucht entweder yyyy oder [yyyy] in Datumsangabe des Briefs
  const match = date.match(/\[?\d{4}\]?$/);
  return match ? match[0] : null;
},
/* Get keyword kategory from list */
keywordCategory(label) {
  return KEYWORD_CATEGORIES[label] || "default";
}
  }
};
</script>

<style>

.thumb {
  width: 80px;
  height: auto;
  border: 1px solid #ccc;
}

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

/* ===== Keyword Badges ===== */
.keyword-filter {
  display: flex;
  flex-direction: column; /* jede Gruppe untereinander */
  gap: 0.6rem; /* Abstand zwischen Oberkategorien */
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
  white-space: nowrap; /* verhindert, dass der Text umbricht */
}

.keyword-badge.oberkategorie {
  font-weight: bold;
  margin-right: 0.5rem; /* etwas Abstand zu Unterkeywords */
}




.keyword-badge.active {
  background: #333;
  color: white;
}



/* Filter */
.keyword-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}









/* ===== Keyword-Kategorien ===== */

.kw-literatur {
  background-color: #ca07076d;
}

.kw-literatur_oberkategorie {
  background-color: #ad2601;
  color: #ffffff;
}

.kw-beziehungen {
  background-color: #ff8c0081;
}

.kw-beziehungen_oberkategorie {
  background-color: #f98800;
  color: #ffffff;
}

.kw-persoenliches {
  background-color: #044c8b88;
}

.kw-persoenliches_oberkategorie {
  background-color: #044b8b;
  color: #ffffff;
}

.kw-politik {
  background-color: #6c0f7c82;
}

.kw-politik_oberkategorie {
  background-color: #6b0f7c;
  color: #ffffff;
}

.kw-reisen {
  background-color: #3ea06d86;
}

.kw-reisen_oberkategorie {
  background-color: #3ea06d;
  color: #ffffff;
}

.kw-emotion {
  background-color: #dbd4018d;
}

.kw-emotion_oberkategorie {
  background-color: #edca05df;
  color: #ffffff;
}

.kw-sprechakt {
  background-color: #f9bf0084;
}

.kw-sprechakt_oberkategorie {
  background-color: #F9C000;
  color: #ffffff;
}

.kw-warensendung {
  background-color: #e2037288;
}

.kw-warensendung_oberkategorie {
  background-color: #e20372;
  color: #ffffff;
}

.kw-zitat {
  background-color: #753b0896;
}

.kw-zitat_oberkategorie {
  background-color: #753b08;
  color: #ffffff;
}

.kw-andere {
  background-color: gray;
  color: #ffffff;
}

</style>
