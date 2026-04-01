<script>
import { isAuthenticated, login } from '../auth.js';

export default {
  data() {
    return {
      isLoggedIn: false,
      password: '',
      error: ''
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
      if (this.isLoggedIn) {
        this.password = '';
        this.error = '';
      }
    },
    seConnecter() {
      if (this.password !== 'admin') {
        this.error = 'Mot de passe incorrect.';
        return;
      }

      login();
      this.$router.push('/edition');
    }
  }
};
</script>

<template>
  <div class="mt-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h3 class="mb-3">Connexion</h3>

        <div v-if="!isLoggedIn">
          <p class="text-muted mb-3">
            Connectez-vous pour accéder au mode édition.
          </p>
          <div class="input-group mb-2">
            <span class="input-group-text">Mot de passe</span>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="admin"
              @keyup.enter="seConnecter"
            >
            <button class="btn btn-primary" @click="seConnecter">Se connecter</button>
          </div>
          <small v-if="error" class="text-danger">{{ error }}</small>
        </div>

        <div v-else class="alert alert-success mb-0 d-flex justify-content-between align-items-center">
          <span>Vous êtes déjà connecté.</span>
          <button class="btn btn-success btn-sm" @click="$router.push('/edition')">Aller au mode édition</button>
        </div>
      </div>
    </div>
  </div>
</template>
