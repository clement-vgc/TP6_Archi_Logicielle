<script>
import QuestionItem from './QuestionItem.vue';

export default {
  components: { QuestionItem },
  props: { questionnaire: Object },
  emits: ['remove-quiz', 'add-question', 'remove-question'],
  data() {
    return {
      newQuestionTitle: ''
    }
  },
  methods: {
    supprQuiz() {
      this.$emit('remove-quiz', { id: this.questionnaire.id });
    },
    ajouterQuestion() {
      if (this.newQuestionTitle.trim() !== '') {
        this.$emit('add-question', { 
          quizId: this.questionnaire.id, 
          title: this.newQuestionTitle.trim() 
        });
        this.newQuestionTitle = '';
      }
    },
    supprimerQuestion(payload) {
      this.$emit('remove-question', { 
        quizId: this.questionnaire.id, 
        number: payload.number 
      });
    }
  }
}
</script>

<template>
  <li class="alert alert-info mt-4 list-unstyled">
    <div class="d-flex justify-content-between align-items-center">
      <h4 class="m-0">{{ questionnaire.name }}</h4> 
      <button class="btn btn-danger btn-sm" @click="supprQuiz">Supprimer le Quiz</button>
    </div>

    <div class="mt-3 bg-white p-3 rounded text-dark">
      <h5>Questions :</h5>
      <ul class="list-group mb-3">
        <QuestionItem 
          v-for="q in questionnaire.questions" 
          :key="q.number" 
          :question="q" 
          @remove="supprimerQuestion"
        />
      </ul>

      <div class="input-group input-group-sm">
        <input v-model="newQuestionTitle" @keyup.enter="ajouterQuestion" placeholder="Texte de la nouvelle question" class="form-control">
        <button @click="ajouterQuestion" class="btn btn-success">Ajouter question</button>
      </div>
    </div>
  </li>
</template>