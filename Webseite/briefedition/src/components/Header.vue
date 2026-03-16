<template>
  <!-- HINWEIS: Der Inhalt dieser Datei wurde mithilfe von GPT-5 überarbeitet. -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">

      <!-- Brand / Home -->
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/logo.png" alt="Logo" width="100" height="100" class="me-2" />
        Startseite
      </router-link>

      <!-- Hamburger für mobile Ansicht -->
      <button class="navbar-toggler" type="button" @click="menuOpen = !menuOpen">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation -->
      <div class="collapse navbar-collapse" :class="{ show: menuOpen }">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">

          <!-- Einfache Links -->
          <li class="nav-item">
            <router-link 
              to="/briefe" 
              class="nav-link" 
              :class="{ active: $route.path === '/briefe' }"
            >
              Briefe
            </router-link>
          </li>

          <!-- Dropdown: Register -->
          <li class="nav-item dropdown" 
              @mouseenter="registerOpen = true" 
              @mouseleave="registerOpen = false">
            <a class="nav-link dropdown-toggle" href="#">Register</a>
            <ul class="dropdown-menu" v-show="registerOpen">
              <li><router-link class="dropdown-item" to="/personenregister">Personen</router-link></li>
              <li><router-link class="dropdown-item" to="/ortsregister">Orte</router-link></li>
              <li><router-link class="dropdown-item" to="/werkregister">Werke</router-link></li>
            </ul>
          </li>

          <!-- Dropdown: Über diese Edition -->
          <li class="nav-item dropdown"
              @mouseenter="aboutOpen = true"
              @mouseleave="aboutOpen = false">
            <a class="nav-link dropdown-toggle" href="#">Über diese Edition</a>
            <ul class="dropdown-menu" v-show="aboutOpen">
              <li><router-link class="dropdown-item" to="/transkriptionsrichtlinien">Transkriptionsrichtlinien</router-link></li>
              <li><router-link class="dropdown-item" to="/about">Über die Briefe</router-link></li>
            </ul>
          </li>

          <!-- Impressum -->
          <li class="nav-item">
            <router-link to="/impressum" class="nav-link" :class="{ active: $route.path === '/impressum' }">
              Impressum
            </router-link>
          </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      menuOpen: false,       // Hamburger-Menü (mobile Ansicht) geöffnet / geschlossen
      registerOpen: false,   // Dropdown Register
      aboutOpen: false       // Dropdown Über diese Edition
    };
  }
};
</script>

<style scoped>
.navbar-brand img {
  object-fit: contain;
}

.navbar {
  background-color: var(--primary-blue) !important;
}

/* Dropdown sichtbar bei Hovern */
.dropdown-menu {
  display: block;
  position: absolute;
  visibility: hidden;
}
.nav-item.dropdown:hover .dropdown-menu {
  visibility: visible;
}

</style>