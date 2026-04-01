<script>
export default {
  props: {
    question: Object,
    index: Number,
    valeurPrecedente: String
  },
  emits: ['reponse'],
  data() {
    return {
      userAnswer: this.valeurPrecedente || ''
    }
  },
  methods: {
    enregistrerReponse() {
      this.$emit('reponse', {
        questionId: this.question.id,
        answer: this.userAnswer
      });
    }
  }
}
</script>

<template>
  <div class="card mb-3">
    <div class="card-body">
      <h5 class="card-title">Question {{ index + 1 }}</h5>
      <p class="card-text">{{ question.title }}</p>

      <div v-if="question.type === 'qcm'">
        <div v-for="(choix, i) in question.propositions" :key="i" class="form-check">
          <input 
            class="form-check-input" 
            type="radio" 
            :name="'qcm-' + question.id" 
            :value="choix.text" 
            v-model="userAnswer"
            @change="enregistrerReponse"
          >
          <label class="form-check-label">{{ choix.text }}</label>
        </div>
      </div>

      <div v-else class="form-group mt-2">
        <input 
          type="text" 
          class="form-control" 
          placeholder="Votre réponse..." 
          v-model="userAnswer"
          @input="enregistrerReponse"
        >
      </div>
    </div>
  </div>
</template>