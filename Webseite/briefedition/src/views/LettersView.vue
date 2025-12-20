<template>
  <div class="letters-overview container">

    <h1>Briefübersicht</h1>

    <!-- ===== Filter ===== -->
    <div class="filters row mb-4">
      <div class="col-md-4">
        <label>Jahr</label>
        <select v-model="selectedYear" class="form-select">
          <option value="">Alle</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>

      <div class="col-md-8">
        <label>Keywords</label>
        <div class="keyword-filter">
          <span
            v-for="kw in allKeywords"
            :key="kw"
            class="keyword-badge"
            :class="{ active: selectedKeywords.includes(kw) }"
            @click="toggleKeyword(kw)"
          >
            {{ kw }}
          </span>
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
        <div class="col-sm-4 meta">
            <div class="date">
              Datum: {{ letter.date }}
            </div>
          <div class="places">
            Absendeort: {{ letter.sender.place }}<br>
            Empfangsort: {{ letter.recipient.place || 'Nicht bekannt' }}
          </div>
        </div>

        <!-- Keywords -->
        <div class="col-sm-5">
          <div class="keywords">
            <span
              v-for="kw in letter.keywords"
              :key="kw.label"
              class="keyword-badge"
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
export default {
  data() {
    return {
      letters: [],
      selectedYear: "",
      selectedKeywords: []
    };
  },

  async mounted() {
    const res = await fetch("/data/briefe_json/alle_briefe.json");
    this.letters = await res.json();
  },

  computed: {
    /* ===== verfügbare Jahre ===== */
    years() {
      return ["1795", "1796", "1797", "[1797]", "1798", "1799", "1800"];
    },

    /* ===== alle Keywords ===== */
    allKeywords() {
      const kws = this.letters.flatMap(l =>
        l.keywords?.map(k => k.label) || []
      );
      return [...new Set(kws)].sort();
    },

    /* ===== gefilterte Briefe ===== */
    filteredLetters() {
      return this.letters.filter(letter => {

        /* Jahr */
if (this.selectedYear) {
  const year = this.extractYear(letter.date);
  if (year !== this.selectedYear) return false;
}

        /* Keywords */
        if (this.selectedKeywords.length) {
          const letterKeywords = letter.keywords?.map(k => k.label) || [];
          if (!this.selectedKeywords.every(k => letterKeywords.includes(k))) {
            return false;
          }
        }

        return true;
      });
    }
  },

  methods: {
    toggleKeyword(kw) {
      const i = this.selectedKeywords.indexOf(kw);
      if (i === -1) this.selectedKeywords.push(kw);
      else this.selectedKeywords.splice(i, 1);
    },
    extractYear(date) {
  if (!date) return null;

  // sucht entweder yyyy oder [yyyy] in Datumsangabe des Briefs
  const match = date.match(/\[?\d{4}\]?$/);
  return match ? match[0] : null;
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

/* ===== Keyword Badges ===== */
.keyword-badge {
  background: #eee;
  padding: 0.2rem 0.5rem;
  border-radius: 0.4rem;
  font-size: 0.8rem;
  cursor: pointer;
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
</style>
