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
body {
  margin: 0;
}

input {
  border: 0;
  border-radius: 8px;
  width: 100%;
}
</style>
