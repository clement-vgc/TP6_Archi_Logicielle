<script>
import { isAuthenticated, logout } from './auth.js';

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false
    };
  },
  mounted() {
    this.refreshAuthState();
    window.addEventListener('auth-changed', this.refreshAuthState);
    window.addEventListener('storage', this.refreshAuthState);
  },
  beforeUnmount() {
    window.removeEventListener('auth-changed', this.refreshAuthState);
    window.removeEventListener('storage', this.refreshAuthState);
  },
  methods: {
    refreshAuthState() {
      this.isLoggedIn = isAuthenticated();
    },
    seDeconnecter() {
      logout();
      this.refreshAuthState();
      this.$router.push('/joueur');
    }
  }
}
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" crossorigin="anonymous">
  
  <div class="container mt-4">
    <div class="d-flex justify-content-center align-items-center gap-3 mb-4 pb-3 border-bottom flex-wrap">
      
      <router-link to="/joueur" class="btn btn-outline-success" active-class="btn-success text-white">
        Mode Joueur
      </router-link>

      <router-link :to="isLoggedIn ? '/edition' : '/connexion'" class="btn btn-outline-primary" active-class="btn-primary text-white">
        Mode Édition
      </router-link>
      
      <router-link v-if="!isLoggedIn" to="/connexion" class="btn btn-outline-secondary" active-class="btn-secondary text-white">
        Se connecter
      </router-link>

      <button v-else class="btn btn-outline-danger btn-sm" @click="seDeconnecter">
        Se déconnecter
      </button>
      
    </div>

    <p class="text-muted text-center mb-4" v-if="!isLoggedIn">
      Vous n'êtes pas connecté: le mode édition est verrouillé.
    </p>

    <router-view></router-view>

  </div>
</template>