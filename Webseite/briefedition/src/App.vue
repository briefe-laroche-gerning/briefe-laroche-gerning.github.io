<template>
  <Header></Header>
  <router-view/>
</template>

<script>
import Header from '@/components/Header.vue'
  export default {
    components: {
      Header
    }
  }
</script>

<style>
/* Import der Main-Style-Datei (für Farben etc.) */
@import './assets/css/main.css';

body {
  margin: 0;
}

input {
  border: 0;
  border-radius: 8px;
  width: 100%;
}
</style>
