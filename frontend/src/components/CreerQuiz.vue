<script>
const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires';

export default {
  data() {
    return {
      newQuizName: ''
    };
  },
  methods: {
    async createQuiz() {
      let name = this.newQuizName.trim();
      if (!name) return;

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name })
      });

      if (!response.ok) {
        alert("Erreur lors de la création du quiz. Le nom existe déjà.");
        return;
      }
      
      const data = await response.json();
      
      if (data.questionnaire && data.questionnaire.id) {
          this.$router.push(`/edition/${data.questionnaire.id}/modifier`);
      } else {
          this.retourVersEdition();
      }
    },
    retourVersEdition() {
      this.$router.push({ path: '/edition', query: { fromModifier: '1' } });
    }
  }
};
</script>

<template>
  <div class="mt-4">
    <button class="btn btn-outline-secondary btn-sm mb-3" @click="retourVersEdition">Retour à la liste</button>

    <div class="card shadow-sm">
      <div class="card-body">
        <h3 class="mb-3">Créer un nouveau quiz</h3>

        <div class="input-group mb-4">
          <span class="input-group-text">Nom du quiz</span>
          <input 
            v-model="newQuizName" 
            @keyup.enter="createQuiz" 
            class="form-control" 
            placeholder="Ex: Culture Générale"
          >
          <button class="btn btn-success" @click="createQuiz">Créer et ajouter des questions</button>
        </div>
      </div>
    </div>
  </div>
</template>