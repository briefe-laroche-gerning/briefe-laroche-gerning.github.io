<template>
  <div>
    <div class="row justify-content-center">
      <div class="col-sm-10">
        <h2>{{ title }}</h2>
        <ul>
          <li v-for="entry in entries" :key="entryKey(entry)">
            <!-- Name -->
            <template v-if="type === 'person'">
              <b><span v-if="entry.firstname">{{ entry.firstname }}</span> {{ entry.name }}</b>
            </template>
            <template v-else>
              <b>{{ entry.name }}</b>
            </template>

            <!-- Links unter dem Namen -->
            <div v-if="type === 'person' || type === 'work'">
              <!-- Personen und Werke: GND / Wikidata -->
              <span v-if="entry.gnd"><a :href="entry.gnd" target="_blank">GND</a></span>
              <span v-if="entry.wikidata">
                <span v-if="entry.gnd"> </span>
                <a :href="entry.wikidata" target="_blank">Wikidata</a>
              </span>

              <!-- Werke: Digitalisat / Volltext -->
              <template v-if="type === 'work' && (entry.digitalisat || entry.volltext)">
                <span v-if="entry.digitalisat"> <a :href="entry.digitalisat" target="_blank">Digitalisat</a></span>
                <span v-if="entry.volltext"> <a :href="entry.volltext" target="_blank">Volltext</a></span>
              </template>
            </div>

            <!-- Orte: Geolink unter dem Namen -->
            <div v-if="type === 'place' && entry.geolink">
              <a :href="entry.geolink" target="_blank">Geolink</a>
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
      this.entries = Object.values(data);
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
</style>
