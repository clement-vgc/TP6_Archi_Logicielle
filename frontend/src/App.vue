<script>
import QuestionnaireItem from './components/QuestionnaireItem.vue';

const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires';

export default {
  components: { QuestionnaireItem },
  data() {
    return {
      questionnaires: [],
      newQuizName: ''
    };
  },
  mounted() {
    this.fetchQuestionnaires();
  },
  methods: {
    // ---- GESTION DES QUESTIONNAIRES ----
    async fetchQuestionnaires() {
      let response = await fetch(API_URL);
      let data = await response.json();
      this.questionnaires = data.questionnaires || data;
    },
    
    async addQuiz() {
      let name = this.newQuizName.trim();
      if (name) {
        await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: name }) 
        });
        this.newQuizName = '';
        this.fetchQuestionnaires(); 
      }
    },
    
    async removeQuiz(payload) {
      await fetch(`${API_URL}/${payload.id}`, { method: 'DELETE' });
      this.fetchQuestionnaires();
    },

    async updateQuiz(payload) {
      await fetch(`${API_URL}/${payload.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: payload.name })
      });
      this.fetchQuestionnaires();
    },

    // ---- GESTION DES QUESTIONS ----
    async addQuestionToQuiz(payload) {
      await fetch(`${API_URL}/${payload.quizId}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: payload.title }) 
      });
      this.fetchQuestionnaires();
    },

    async removeQuestionFromQuiz(payload) {
      await fetch(`${API_URL}/${payload.quizId}/questions/${payload.number}`, { 
        method: 'DELETE' 
      });
      this.fetchQuestionnaires();
    }
  }
}
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" crossorigin="anonymous">
  
  <div class="container mt-4">
    <h2>Édition des Quiz</h2>
    
    <div class="input-group mb-4">
      <input v-model="newQuizName" @keyup.enter="addQuiz" placeholder="Nom du nouveau quiz" class="form-control">
      <button @click="addQuiz" class="btn btn-primary">Créer le quiz</button>
    </div>

    <ul class="p-0">
      <QuestionnaireItem 
        v-for="q in questionnaires" 
        :key="q.id"
        :questionnaire="q"
        @remove-quiz="removeQuiz"
        @update-quiz="updateQuiz"  @add-question="addQuestionToQuiz"
        @remove-question="removeQuestionFromQuiz"
      />
    </ul>
  </div>
</template>