<script>
import QuestionAdminItem from './QuestionAdminItem.vue';

const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires';

export default {
  components: { QuestionAdminItem },
  data() {
    return {
      quiz: null,
      loading: true,
      error: ''
    };
  },
  mounted() {
    this.fetchQuiz();
  },
  methods: {
    async fetchQuiz() {
      this.loading = true;
      const response = await fetch(`${API_URL}/${this.$route.params.id}`);
      if (!response.ok) {
        this.error = 'Quiz introuvable.';
        this.quiz = null;
      } else {
        const data = await response.json();
        this.quiz = data.questionnaire;
      }
      this.loading = false;
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

    <div v-if="loading" class="alert alert-info">Chargement du quiz...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else class="card shadow-sm">
      <div class="card-body">
        <h3 class="mb-3">Consultation : {{ quiz.name }}</h3>
        <p class="text-muted">ID du quiz : {{ quiz.id }}</p>

        <h5 class="mt-4">Questions ({{ quiz.questions.length }})</h5>
        
        <ul class="list-group mb-4" v-if="quiz.questions.length > 0">
          <QuestionAdminItem
            v-for="question in quiz.questions"
            :key="question.id"
            :question="question"
            :canEdit="false"
          />
        </ul>
        
        <div v-else class="alert alert-warning">
          Aucune question dans ce quiz pour le moment.
        </div>
      </div>
    </div>
  </div>
</template>