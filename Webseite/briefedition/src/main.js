import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Z.B. für Carousel, Popper


import "@fancyapps/ui/dist/fancybox/fancybox.css";   // Für Galerieoptionen (Rotieren etc. bei den Faksimiles)
import { Fancybox } from "@fancyapps/ui";

// Fancybox global aktivieren
Fancybox.bind("[data-fancybox]", {
  Toolbar: {
    display: [
      "zoom",
      "rotate_ccw",
      "rotate_cw",
      "fullscreen",
      "close",
    ],
    // Zusätzliche Buttons
    items: {
      rotate_ccw: {
        type: "button",
        label: "Nach links drehen",
        icon: "rotate_ccw",
        click: (event, fancybox, slide) => {
          slide.rotate(-90);
        }
      },
      rotate_cw: {
        type: "button",
        label: "Nach rechts drehen",
        icon: "rotate_cw",
        click: (event, fancybox, slide) => {
          slide.rotate(90);
        }
      }
    }
  },
  l10n: {
    CLOSE: "Schließen",
    NEXT: "Nächste",
    PREV: "Vorherige",
    FULLSCREEN: "Vollbild",
    ZOOM: "Zoom",
    ERROR: "Inhalt konnte nicht geladen werden",
  }
});


createApp(App).use(router).mount('#app')
