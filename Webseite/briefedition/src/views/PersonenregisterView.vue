<template>
  <!-- Nutzt Komponente "Register" und übergibt als Daten die Personenregister-JSON.  -->
  <Register url="/data/register/personenregister.json" title="Personenregister" type="person" />
</template>

<script>
import Register from "@/components/Register.vue";

export default {
  components: { Register }
};
</script>