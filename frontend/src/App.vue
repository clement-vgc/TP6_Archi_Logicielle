<script>
export default {
  name: 'App'
}
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" crossorigin="anonymous">
  
  <div class="container mt-4">
    <div class="d-flex justify-content-center mb-5 pb-3 border-bottom">
      
      <router-link to="/edition" class="btn btn-outline-primary me-3" active-class="btn-primary text-white">
        Mode Édition
      </router-link>
      
      <router-link to="/joueur" class="btn btn-outline-success" active-class="btn-success text-white">
        Mode Joueur
      </router-link>
      
    </div>

    <router-view></router-view>

  </div>
</template>