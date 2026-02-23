<template>
  <!-- HINWEIS: Der Inhalt von compareEntries(a, b){...}, countLettersForEntry(entryId){...}, sowie async mounted(){...} wurde mithilfe von GPT-5 generiert und anschließend überarbeitet. -->
  
  <!--  Dieses Template generiert alle drei Registerseiten (Personen, Orte, Werke). Es ändert sich je nach übergebenen Daten.  -->
  <div>
    <div class="row justify-content-center">
      <div class="col-sm-10">
        <h2>{{ title }}</h2>

        <ul>
          <li v-for="entry in entries" :key="entry.id" :id="entry.id">
            <!--  Name existiert für alle drei Arten von Registereinträgen  -->
            <!-- Wenn Person: Namen aus Vor- und Nachnamen zusammensetzen -->
            <template v-if="type === 'person'">
              <b>
                {{ entry.firstname ? entry.firstname + ' ' : '' }}{{ entry.name }}
              </b>
            </template>
            <template v-else>
              <b>{{ entry.name }}</b>
            </template>

            <!-- Person oder Ort: GND- und Wikidata-Link -->
            <div v-if="type === 'person' || type === 'place'" class="meta">
              <span>
                <a v-if="entry.gnd" :href="entry.gnd" target="_blank">GND</a>
                <span v-else class="placeholder">GND</span>
              </span>
              |
              <span>
                <a v-if="entry.wikidata" :href="entry.wikidata" target="_blank">Wikidata</a>
                <span v-else class="placeholder">Wikidata</span>
              </span>
              <span>
                <router-link :to="{name: 'briefe', query: {entityType: type, entityId: entry.id}}" class="btn btn-dark btn-sm button"> <!-- Link zur Briefübersichtsseite mit Filter -->
                  <i class="bi bi-search"></i>
                  Briefe ({{ countLettersForEntry(entry.id) }})
                </router-link>
              </span>
            </div>

            <!-- Werk: GND- und Wikidata-Link, Link zu Digitalisat, Link zu Volltext -->
            <div v-if="type === 'work'" class="meta">
              <span>
                <a v-if="entry.gnd" :href="entry.gnd" target="_blank">GND</a>
                <span v-else class="placeholder">GND</span>
              </span>
              |
              <span>
                <a v-if="entry.wikidata" :href="entry.wikidata" target="_blank">Wikidata</a>
                <span v-else class="placeholder">Wikidata</span>
              </span>
              |
              <span>
                <a v-if="entry.digitalisat" :href="entry.digitalisat" target="_blank">Digitalisat</a>
                <span v-else class="placeholder">Digitalisat</span>
              </span>
              |
              <span>
                <a v-if="entry.volltext" :href="entry.volltext" target="_blank">Volltext</a>
                <span v-else class="placeholder">Volltext</span>
              </span>
              <span>
              <router-link :to="{name: 'briefe', query: {entityType: type, entityId: entry.id}}" class="btn btn-dark btn-sm button"> <!-- Link zur Briefübersichtsseite mit Filter -->
                <i class="bi bi-search"></i>
                Briefe ({{ countLettersForEntry(entry.id) }})
              </router-link>
            </span>
            </div>

          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  props: {
    url: { type: String, required: true },
    title: { type: String, required: true },
    type: { type: String, required: true } // Möglichkeiten: 'person', 'place', 'work'
  },
  data() {
    return {
      entries: [],
      letters: []   // Alle Briefe: Wird für Filter nach Entitäten gebraucht
    };
  },
async mounted() {
  try {
    // Laden der Registerdaten
    const response = await fetch(this.url);
    const data = await response.json();

    // Laden der Briefe (für Filter nach Entitäten)
    const lettersRes = await fetch("/data/briefe_json/alle_briefe.json");
    this.letters = await lettersRes.json();

    this.entries = Object.entries(data)
      // Umstrukturierung des JSON-Objekts
      .map(([id, entry]) => ({ id, ...entry }))
      .sort((a, b) => this.compareEntries(a, b));

    // Scroll zu Hash, falls vorhanden (Benötigt für Weiterleitung, wenn User auf einen Link zu einem Registereintrag klickt)
    if (this.$route.hash) {
      this.$nextTick(() => {
        const el = document.querySelector(this.$route.hash);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      });
    }
  } catch (err) {
    console.error("Fehler beim Laden des Registers:", err);
  }
},

methods: {

  // Zum Sortieren der Register-Einträge nach Alphabet
  compareEntries(a, b) {
    const collator = new Intl.Collator("de", {
      sensitivity: "base",
      numeric: true
    });

    // Personen: "Nachname Vorname", funktioniert auch, wenn nur eins davon existiert
    if (this.type === "person") {
      const nameA = `${a.name.replace(/^(von|der|den|de|zu)\s+/i, "").trim() || ""} ${a.firstname || ""}`.trim();
      const nameB = `${b.name.replace(/^(von|der|den|de|zu)\s+/i, "").trim() || ""} ${b.firstname || ""}`.trim();
      return collator.compare(nameA, nameB);
    }

    // Orte & Werke: Name
    return collator.compare(a.name, b.name);
  },

  // Zum Zählen der Briefe, die die jeweilige Person, den Ort oder das Werk enthalten
  countLettersForEntry(entryId) {
    return this.letters.filter(letter => {

      if (this.type === "person") {
        return letter.register_entities?.persons?.includes(entryId);
      }

      if (this.type === "place") {
        return letter.register_entities?.places?.includes(entryId);
      }

      if (this.type === "work") {
        return letter.register_entities?.works?.includes(entryId);
      }

      return false;
    }).length;
  }
  }
};
</script>

<style scoped>

/* Abstand zum oberen Rand */
.row {
  margin-top: 20px;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 8px;
}

/* Links in einer Zeile, getrennt durch | */
li div a {
  margin-right: 4px;
}

/* Metadaten der Registereinträge */
.meta {
  font-size: 0.9em;
  margin-top: 2px;
}

/* Ausgegraute Links/Placeholder wenn kein Link vorhanden (für GND, Wikidata etc.) */
.placeholder {
  color: rgb(50, 46, 46);
  background: none;
}

/* Button mit Link zu Briefübersicht */
.button {
  background-color: var(--primary-blue) !important;
  margin-left: 1em;
}
</style>
