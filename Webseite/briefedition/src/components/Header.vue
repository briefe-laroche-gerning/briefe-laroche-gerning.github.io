<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">

      <!-- Brand / Home (Router-Link statt <a>) -->
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/logo.png" alt="Logo" width="100" height="100" class="me-2" />
        Startseite
      </router-link>

      <!-- Mobile Toggler/Hamburgermenü in mobilder Ansicht -->
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarSupportedContent"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        
        <!-- Links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">

            <li class="nav-item">
                <router-link to="/briefe" class="nav-link">
                  Briefe
                </router-link>
            </li>
 <li class="nav-item dropdown">
  <a
    class="nav-link dropdown-toggle"
    role="button"
    data-bs-toggle="dropdown"
    aria-expanded="false"
  >
    Register
  </a>

  <ul class="dropdown-menu">
    <li>
      <router-link class="dropdown-item" to="/personenregister">Personen</router-link>
    </li>
    <li>
      <router-link class="dropdown-item" to="/ortsregister">Orte</router-link>
    </li>
    <li>
      <router-link class="dropdown-item" to="/werkregister">Werke</router-link>
    </li>
  </ul>
</li>

  <li class="nav-item">
    <router-link to="/about" class="nav-link">
      Über diese Edition
    </router-link>
  </li>

  <li class="nav-item">
    <router-link to="/impressum" class="nav-link">
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
};
</script>

<style scoped>
.navbar-brand img {
  object-fit: contain;
}

.navbar {
    background-color: #020664 !important;
}


</style>



























