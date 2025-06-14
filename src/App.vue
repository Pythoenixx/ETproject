<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-forest">
      <div class="container">
        <router-link to="/" class="navbar-brand">
          <i class="bi bi-tree-fill me-2"></i>FORESTEYE
        </router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                List of Trees
              </a>
              <ul class="dropdown-menu">
                <li><router-link to="/list-of-trees" class="dropdown-item">View All Trees</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Production Data
              </a>
              <ul class="dropdown-menu">
                <li><router-link to="/final-output" class="dropdown-item">Final Output</router-link></li>
                <li><router-link to="/stand-table" class="dropdown-item">Stand Table</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Cutting Regime
              </a>
              <ul class="dropdown-menu">
                <li><router-link to="/cutting-regime" class="dropdown-item">Regime</router-link></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Data Visualization
              </a>
              <ul class="dropdown-menu">
                <li><router-link to="/tree-map" class="dropdown-item">Tree Map</router-link></li>
                <li><router-link to="/analysis" class="dropdown-item">Analysis</router-link></li>

              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <router-view />

    <!-- Footer -->
    <footer class="footer-forest text-center">
      <div class="container">
        <p class="mb-2">Copyright: ForestEye All Right Reserved</p>
        <p class="mb-0">
          <!-- <small>Powered By: Green Information System International Sdn Bhd</small> -->
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>