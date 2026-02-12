<template>
  <link href='https://fonts.googleapis.com/css?family=Open Sans' rel='stylesheet'>
<div class="single-letter-page">
<div class="row justify-content-center">
<div class="col-sm-10">
  <h3>Sophie von La Roche an Johann Isaak von Gerning am {{ metadata?.date || '' }}</h3>
  <p>
    <b>Bestandshaltende Institution:</b> {{ metadata?.identifier?.institution || '' }}
    <b style="margin-left: 10px;">Signatur:</b> {{ metadata?.identifier?.signature || '' }}
  </p>
  <p>
    <b>Absendeort:</b> {{ metadata?.sender.place || 'Keine Angabe' }}
    <b style="margin-left: 10px;">Empfangsort:</b> {{ metadata?.recipient.place || 'Keine Angabe' }}
  </p>
  <p>
    <a :href="`/data/briefe_tei/brief${nr}_tei.xml`" target="_blank">TEI-Download</a>
    <a style="margin-left: 10px;" :href="`/data/briefe_txt/brief${nr}.txt`" target="_blank">TXT-Download</a>
  </p>
</div>

  </div>

  <br>

      <div class="row justify-content-center">
        <!-- Faksimile (Carousel: Bilder können durchgeblättert werden)-->
        <div class="col-sm-4">

          <FacsimileViewer :images="images" />




          
        </div>

        <!-- Transkript -->
        <div class="col-sm-3">
<div v-if="loading">Lade Inhalt …</div>
<div
  v-else
  ref="letterContent"
  class="letter-content"
  v-html="content"
></div>

        </div>

        <!-- Registereinträge -->
        <div class="col-sm-3">
          <!-- Personen -->
          <h4>Personen</h4>
          <ul>
            <li v-for="person in persons" :key="person.id">
              <router-link :to="{ name: 'personenregister', hash: '#' + person.id }">
                {{ person.firstname }} {{ person.name }}
              </router-link>
            </li>
          </ul>
          <!-- Orte -->
          <h4>Orte</h4>
          <ul>
            <li v-for="place in places" :key="place.id">
              <router-link :to="{ name: 'ortsregister', hash: '#' + place.id }">
                {{ place.name }}
              </router-link>
            </li>
          </ul>
          <!-- Werke -->
          <h4>Werke</h4>
          <ul>
            <li v-for="work in works" :key="work.id">
              <router-link :to="{ name: 'werkregister', hash: '#' + work.id }">
                {{ work.name }}
              </router-link>
            </li>
          </ul>



        </div>

        </div>
</div>
</template>


<script>
import { nextTick } from 'vue';
import { Tooltip } from "bootstrap";

import FacsimileViewer from '@/components/FacsimileViewer.vue';

export default {
  components: {
    FacsimileViewer
  },

  props: ['nr'],

  data() {
    return {
      content: '',           // HTML-Inhalt (Transkription)
      loading: true,

      images: [],
      currentImageIndex: 0,
      currentImage: null,
      rotation: 0,
      scale: 1,

      briefPages: {
        1: 4, 2: 4, 3: 4, 4: 6, 5: 2,
        6: 4, 7: 4, 8: 4, 9: 4, 10: 4,
        11: 4, 12: 4, 13: 4, 14: 4, 15: 4,
        16: 7, 17: 6, 18: 4, 19: 2, 20: 2,
        21: 4, 22: 6, 23: 4, 24: 4, 25: 1
      },

      metadata: null, // die Meta-Daten aus brief{i}.json

      personenRegister: {},
      ortsRegister: {},
      werkRegister: {},

      // Gesammelte Entities aus dem Brief (kommen im Brieftext vor)
      mentionedEntities: {
        person: new Set(),
        place: new Set(),
        work: new Set()
      }
    };
  },

  async mounted() {
    const resPersonen = await fetch('/data/register/personenregister.json');
    this.personenRegister = await resPersonen.json();
    const resOrte = await fetch('/data/register/ortsregister.json');
    this.ortsRegister = await resOrte.json();
    const resWerke = await fetch('/data/register/werkregister.json');
    this.werkRegister = await resWerke.json();

    await this.loadLetter();
  },

  watch: {
    nr() {
      this.loadLetter();
    },

    async content() {
      await nextTick();
      this.linkEntitiesInHtml();
      this.initTooltips();
    }
  },

  computed: {
  persons() {
    return [...this.mentionedEntities.person]
      .map(id => {
        const obj = this.personenRegister[id];
        if (!obj) return null;        
        return { ...obj, id };          // ID direkt aus dem Set übernehmen
      })
      .filter(Boolean);
  },

  places() {
    return [...this.mentionedEntities.place]
      .map(id => {
        const obj = this.ortsRegister[id];
        if (!obj) return null;
        return { ...obj, id };          // ID aus dem Set übernehmen
      })
      .filter(Boolean);
  },

  works() {
    return [...this.mentionedEntities.work]
      .map(id => {
        const obj = this.werkRegister[id];
        if (!obj) return null;
        return { ...obj, id };          // ID aus dem Set übernehmen
      })
      .filter(Boolean);
  }
},


  methods: {

    async loadLetter() {
      await this.loadHtml();
      await this.loadMetadata();
      this.loadImages();
    },

    async loadHtml() {
      this.loading = true;
      const filename = `/data/briefe_html/brief${this.nr}.html`;

      try {
        const response = await fetch(filename);
        if (!response.ok) throw new Error("Datei nicht gefunden");
        this.content = await response.text();
      } catch (error) {
        this.content = `<h2>Die Datei brief${this.nr}.html existiert nicht.</h2>`;
        console.error(error);
      }

      this.loading = false;
    },

    /* Laden der Meta-Daten aus brief{i}.json */
    async loadMetadata() {
  try {
    const response = await fetch(`/data/briefe_json/brief${this.nr}.json`);
    if (!response.ok) throw new Error("JSON-Datei nicht gefunden");
    this.metadata = await response.json();
  } catch (error) {
    console.error(error);
    this.metadata = null;
  }
},

    loadImages() {
      const numImages = this.briefPages[this.nr] || 0;
      this.images = [];

      for (let i = 1; i <= numImages; i++) {
        this.images.push(`/img/digitalisate/brief${this.nr}_${i}.jpg`);
      }

      this.currentImageIndex = 0;
    },

   linkEntitiesInHtml() {
  // Sets zurücksetzen
  this.mentionedEntities.person.clear();
  this.mentionedEntities.place.clear();
  this.mentionedEntities.work.clear();

  const container = this.$refs.letterContent;
  if (!container) return;

  const spans = container.querySelectorAll("span.entity");

  spans.forEach(span => {
    let keys = [];

    if (span.classList.contains("person")) {
      // Personen haben data-keys als JSON-Array
      keys = JSON.parse(span.dataset.keys || "[]");
    } else if (span.classList.contains("place") || span.classList.contains("work")) {
      // Orte / Werke haben nur einen string in data-key
      if (span.dataset.key) keys = [span.dataset.key];
    }

    if (!keys.length) return;

    let type = null;
    let route = null;

    if (span.classList.contains("person")) {
      type = "person";
      route = "personenregister";
    } else if (span.classList.contains("place")) {
      type = "place";
      route = "ortsregister";
    } else if (span.classList.contains("work")) {
      type = "work";
      route = "werkregister";
    }

    if (!type) return;

    // IDs für Randspalte sammeln
    keys.forEach(id => this.mentionedEntities[type].add(id));

    // Link erzeugen (bei mehreren IDs: erste nehmen)
const a = document.createElement("a");
a.innerHTML = span.innerHTML;
a.href = `/${route}#${keys[0]}`;
a.classList.add("entity-link", type);

// Tooltip-Inhalt zusammenbauen
let tooltipLines = [];

keys.forEach(id => {
  if (type === "person") {
    const p = this.personenRegister[id];
    if (p) tooltipLines.push(`${p.firstname} ${p.name}`);
  }
  if (type === "place") {
    const o = this.ortsRegister[id];
    if (o) tooltipLines.push(o.name);
  }
  if (type === "work") {
    const w = this.werkRegister[id];
    if (w) tooltipLines.push(w.name);
  }
});

// Tooltip-Attribute setzen
if (tooltipLines.length) {
  a.setAttribute("data-bs-title", tooltipLines.join("<br>"));
  a.setAttribute("data-bs-toggle", "tooltip");
  a.setAttribute("data-bs-html", "true");
}

span.replaceWith(a);

  });
},
async initTooltips() {
  await nextTick();

  // Alte Tooltips entfernen
  document.querySelectorAll(
    ".recipient-note, .unclear, .entity-link"
  ).forEach(el => {
    if (el._tooltipInstance) {
      el._tooltipInstance.dispose();
      el._tooltipInstance = null;
    }
  });

  const elements = document.querySelectorAll(
    ".recipient-note, .unclear, .entity-link"
  );

  elements.forEach(el => {
    let title = el.getAttribute("data-bs-title");

    // feste Tooltip-Texte
    if (el.classList.contains("recipient-note")) {
      title = "Notiz des Empfängers";
    }

    if (el.classList.contains("unclear")) {
      title = "Nicht entziffert";
    }

    if (!title) return;

    el.setAttribute("data-bs-title", title);
    el.setAttribute("data-bs-toggle", "tooltip");
    el.removeAttribute("title");

    const instance = new Tooltip(el, {
      html: true,
      trigger: "hover focus"
    });

    el._tooltipInstance = instance;

    // 🔑 Zentrale Logik:
    // Innerer Tooltip deaktiviert äußeren recipient-note Tooltip
    if (
      el.classList.contains("unclear") ||
      el.classList.contains("entity-link")
    ) {
      const outer = el.closest(".recipient-note");

      if (outer && outer._tooltipInstance) {
        el.addEventListener("mouseenter", () => {
          outer._tooltipInstance.disable();
        });

        el.addEventListener("mouseleave", () => {
          outer._tooltipInstance.enable();
        });
      }
    }
  });
}

  }
};
</script>



<style>

/* Styles für die HTML-Dokumente der Transkriptionen */

/* Schriftart für Kurrentschrift*/
.tei-div {
  font-family: Garamond;
}

.underline {
  text-decoration: underline;
}

.double-underline {
  text-decoration-line: underline;
  text-decoration-style: double;
}

/* Schriftart für lateinische Schreibschrift*/
.latintype {
  font-family: 'Open Sans'
}

/* Farben für Notizen Gernings und nicht entzifferte Stellen */
.recipient-note {
  color: gray
}
.unclear {
  color: darkred
}

/* Abstand am unteren Rand der Seite */
.single-letter-page {
  margin-bottom: 4rem;
}

/* Metadaten (Kopf der Seite) */
.single-letter-page .col-sm-10 p {
  margin: 0;
}
.single-letter-page .col-sm-10 h3 {
  margin-bottom: 0.5rem;
  margin-top: 1rem;
}










</style>