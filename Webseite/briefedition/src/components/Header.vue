<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">

      <!-- Brand / Home (Router-Link statt <a>) -->
      <router-link class="navbar-brand d-flex align-items-center" to="/">
        <img src="@/assets/logo.png" alt="Logo" width="100" height="100" class="me-2" />
        Home
      </router-link>

      <!-- Mobile Toggler -->
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
                <router-link to="/register/personen" class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown">
                Register
                </router-link>
                <ul class="dropdown-menu">
                    <li><router-link class="dropdown-item" to="/register/personen">Personen</router-link></li>
                    <li><router-link class="dropdown-item" to="/register/orte">Orte</router-link></li>
                    <li><router-link class="dropdown-item" to="/register/werke">Werke</router-link></li>
                </ul>
            </li>
            <li class="nav-item">
                <router-link to="/about" class="nav-link">
                Über diese Edition
                </router-link>
            </li>
        </ul>

        <!-- Suche -->
        <form class="d-flex" @submit.prevent="search">
          <input class="form-control me-2" type="search" placeholder="Suche..." v-model="query">
          <button class="btn btn-outline-light" type="submit">Suchen</button>
        </form>

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



























