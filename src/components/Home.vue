<template>
  <div>
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row justify-content-center text-center">
          <div class="col-lg-8">
            <h1 class="display-4 fw-bold text-white mb-4">
              Welcome To ForestEye
            </h1>
            <p class="lead text-white mb-5">
              This is a simple project to manage and visualize forest data.
            </p>
            <router-link to="/data-visualization" class="btn btn-create-forest btn-lg">
              CREATE FOREST
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Information Section -->
    <section class="info-section">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Forestry Information & Benefits</h2>
          <p class="text-muted">Learn about sustainable forestry and environmental conservation</p>
        </div>
        
        <div class="row g-4">
          <!-- Row 1 -->
          <div class="col-md-4">
            <div class="info-card">
              <img src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=200&fit=crop" alt="Biodiversity" class="img-fluid">
              <h5>Biodiversity</h5>
              <p>Forests are home to a staggering 80% of the world's terrestrial biodiversity, including countless species of plants, animals, and microorganisms, contributing to biodiversity and ecosystem health.</p>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="info-card">
              <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=200&fit=crop" alt="Climate Regulation" class="img-fluid">
              <h5>Climate Regulation</h5>
              <p>Forests play a crucial role in regulating the earth's climate by absorbing carbon dioxide from the atmosphere and releasing oxygen through photosynthesis.</p>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="info-card">
              <img src="/images/water.jpg" alt="Water Cycle" class="img-fluid">
              <h5>Water Cycle</h5>
              <p>Forests help regulate the water cycle by absorbing groundwater and releasing it into the atmosphere, contributing to precipitation patterns.</p>
            </div>
          </div>
          
          <!-- Row 2 -->
          <div class="col-md-4">
            <div class="info-card">
              <img src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=200&fit=crop&crop=center" alt="Soil Conservation" class="img-fluid">
              <h5>Soil Conservation</h5>
              <p>Forest canopy and root systems help by stabilizing the soil and prevent erosion and providing ground cover that retains moisture and nutrients.</p>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="info-card">
              <img src="/images/timber.jpg" alt="Economic Benefits" class="img-fluid">
              <h5>Economic Benefits</h5>
              <p>Forests provide resources such as timber, non-timber products, and recreational opportunities, contributing to local and global economies.</p>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="info-card">
              <img src="/images/culture.jpg" alt="Cultural Significance" class="img-fluid">
              <h5>Cultural Significance</h5>
              <p>Forests hold cultural and spiritual significance for many indigenous communities, serving as sacred spaces and sources of traditional knowledge and heritage.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>