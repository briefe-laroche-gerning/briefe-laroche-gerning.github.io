<template>
  <!-- Nutzt Komponente "Register" und übergibt als Daten die Werkregister-JSON.  -->
  <Register url="/data/register/werkregister.json" title="Werkregister" type="work" />
</template>

<script>
import Register from "@/components/Register.vue";

export default {
  components: { Register }
};
</script>