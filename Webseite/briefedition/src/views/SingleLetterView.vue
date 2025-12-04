<template>
  <link href='https://fonts.googleapis.com/css?family=Open Sans' rel='stylesheet'>

<div class="row justify-content-center">
  <div class="col-sm-10">
      <h1>Brief vom xx.xx.xxxx</h1>
      <p>Bestandshaltende Institution:</p>
      <p>Signatur:</p>
      <p>TEI-Download</p>
      <p>TXT Download</p>
</div>
  </div>


      <div class="row justify-content-center">
        <!-- Faksimile (Carousel: Bilder können durchgeblättert werden)-->
        <div class="col-sm-4">

          <FacsimileViewer :images="images" />




          
        </div>

        <!-- Transkript -->
        <div class="col-sm-4">
            <div v-if="loading">Lade Inhalt...</div>
            <div v-else v-html="content"></div>
        </div>

        <!-- Registereinträge -->
        <div class="col-sm-2">
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer
        </div>
        </div>

</template>



<script>
import FacsimileViewer from '@/components/FacsimileViewer.vue';

export default {
  components: {
    FacsimileViewer
  },
  props: ['nr'],

  data() {
  return {
    content: '',           // HTML-Inhalt (Transkription des Briefs)
    loading: true,         // Ladezustand für HTML
    images: [],            // Array der Faksimile-Bilder
    currentImageIndex: 0,  // Index für Carousel
    currentImage: null,    // für das Modal / Vollansicht des Bildes
    rotation: 0,           // für Rotation des Digitalisats
    scale: 1,              // für Zoom des Digitalisats
    briefPages: {          // Anzahl der Seiten pro Brief
      1: 4,
      2: 4,
      3: 4,
      4: 6,
      5: 2,
      6: 4,
      7: 4,
      8: 4,
      9: 4,
      10: 4,
      11: 4,
      12: 4,
      13: 4,
      14: 4,
      15: 4,
      16: 7,
      17: 6,
      18: 4,
      19: 2,
      20: 2,
      21: 4,
      22: 6,
      23: 4,
      24: 4,
      25: 1
    },
  };
  },

  mounted() {
    this.loadLetter();
  },

  watch: {
    nummer() {
      this.loadLetter(); // neu laden, falls Route sich ändert
    }
  },

  methods: {
  

    async loadLetter() {
      await this.loadHtml();
      this.loadImages();
    },

    // Für HTML-Dateien (Transkriptionen)
    async loadHtml() {
      this.loading = true;

      // URL zu den HTML-Dateien im public-Ordner
      const filename = `/briefe_html/brief${this.nr}.html`;

      try {
        const response = await fetch(filename);

        if (!response.ok) {
          throw new Error('Datei nicht gefunden');
        }

        this.content = await response.text();
      } catch (error) {
        this.content = `<h2>Die Datei brief${this.nr}.html existiert nicht.</h2>`;
        console.error(error);
      }

      this.loading = false;
    },
    // Bilder für das Carousel laden (den jeweiligen Brief)
  loadImages() {
    const numImages = this.briefPages[this.nr] || 0; // fallback 0
    this.images = [];

    for (let i = 1; i <= numImages; i++) {
      const url = `/img/digitalisate/brief${this.nr}_${i}.jpg`;
      this.images.push(url);
    }

    this.currentImageIndex = 0; // reset auf erstes Bild
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

</style>