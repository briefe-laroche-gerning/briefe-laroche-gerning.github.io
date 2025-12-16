<template>
  <div>
    <div class="row justify-content-center">
      <div class="col-sm-10">
        <h2>{{ title }}</h2>

        <ul>
          <li v-for="entry in entries" :key="entry.id" :id="entry.id">
            <!-- NAME -->
            <template v-if="type === 'person'">
              <b>
                {{ entry.firstname ? entry.firstname + ' ' : '' }}{{ entry.name }}
              </b>
            </template>
            <template v-else>
              <b>{{ entry.name }}</b>
            </template>

            <!-- PERSON -->
            <div v-if="type === 'person'" class="meta">
              <span>
                <a v-if="entry.gnd" :href="entry.gnd" target="_blank">GND</a>
                <span v-else class="placeholder">GND</span>
              </span>
              |
              <span>
                <a v-if="entry.wikidata" :href="entry.wikidata" target="_blank">Wikidata</a>
                <span v-else class="placeholder">Wikidata</span>
              </span>
            </div>

            <!-- ORT -->
            <div v-if="type === 'place'" class="meta">
              <a v-if="entry.geolink" :href="entry.geolink" target="_blank">Geolink</a>
              <span v-else class="placeholder">Geolink</span>
            </div>

            <!-- WERK -->
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
    type: { type: String, default: "person" } // 'person', 'place', 'work'
  },
  data() {
    return {
      entries: []
    };
  },
  async mounted() {
    try {
      const res = await fetch(this.url);
      const data = await res.json();
      this.entries = Object.entries(data).map(([id, entry]) => ({ id, ...entry }));

      // Scroll zu Hash, falls vorhanden
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
    entryKey(entry) {
      return entry.gnd || entry.name;
    }
  }
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 8px;
}

/* Links in einer Zeile, Abstand durch | */
li div a {
  margin-right: 4px;
}

/* Metadaten der Registereinträge */
.meta {
  font-size: 0.9em;
  margin-top: 2px;
}

/* Ausgegraute Links/Placeholder wenn kein Link vorhanden */
.placeholder {
  color: rgb(50, 46, 46);
  background: none;
}
</style>
