import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Z.B. für Carousel, Popper
import 'bootstrap-icons/font/bootstrap-icons.css'; // Bootstrap Icons (z.B. Lupensymbol für Suche)

createApp(App).use(router).mount('#app')
