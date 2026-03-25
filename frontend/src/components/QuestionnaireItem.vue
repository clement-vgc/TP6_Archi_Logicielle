<script>
import QuestionItem from './QuestionItem.vue';

export default {
  components: { QuestionItem },
  props: { questionnaire: Object },
  emits: ['remove-quiz', 'update-quiz', 'add-question', 'remove-question', 'update-question'],
  data() {
    return {
      newQuestionTitle: '',
      newQuestionType: 'question',
      newQuestionReponse: '',
      newQuestionP1: '',
      newQuestionP2: '',
      newQuestionBonneReponse: 1
    }
  },
  methods: {
    supprQuiz() {
      this.$emit('remove-quiz', { id: this.questionnaire.id });
    },
    modifQuiz() {
      let nouveauNom = prompt("Modifier le nom du quiz :", this.questionnaire.name);
      if (nouveauNom !== null && nouveauNom.trim() !== '') {
        this.$emit('update-quiz', { id: this.questionnaire.id, name: nouveauNom.trim() });
      }
    },
    ajouterQuestion() {
      if (this.newQuestionTitle.trim() !== '') {
        const payload = {
          quizId: this.questionnaire.id,
          title: this.newQuestionTitle.trim(),
          type: this.newQuestionType,
          reponse: this.newQuestionReponse,
          p1: this.newQuestionP1,
          p2: this.newQuestionP2,
          bonne_reponse: Number(this.newQuestionBonneReponse)
        };

        this.$emit('add-question', { 
          ...payload
        });

        this.newQuestionTitle = '';
        this.newQuestionType = 'question';
        this.newQuestionReponse = '';
        this.newQuestionP1 = '';
        this.newQuestionP2 = '';
        this.newQuestionBonneReponse = 1;
      }
    },
    supprimerQuestion(payload) {
      this.$emit('remove-question', { 
        quizId: this.questionnaire.id, 
        id: payload.id 
      });
    },
    modifierQuestion(payload) {
      this.$emit('update-question', {
        quizId: this.questionnaire.id,
        id: payload.id,
        data: payload.data
      });
    }
  }
}
</script>

<template>
  <li class="alert alert-info mt-4 list-unstyled">
    <div class="d-flex justify-content-between align-items-center">
      <h4 class="m-0">{{ questionnaire.name }}</h4> 
      <div>
        <button class="btn btn-warning btn-sm me-2" @click="modifQuiz">Modifier le Quiz</button>
        <button class="btn btn-danger btn-sm" @click="supprQuiz">Supprimer le Quiz</button>
      </div>
    </div>

    <div class="mt-3 bg-white p-3 rounded text-dark">
      <h5>Questions :</h5>
      <ul class="list-group mb-3">
        <QuestionItem 
          v-for="q in questionnaire.questions" 
          :key="q.id" 
          :question="q" 
          @remove="supprimerQuestion"
          @update="modifierQuestion"
        />
      </ul>

      <div class="mb-2">
        <select v-model="newQuestionType" class="form-select form-select-sm">
          <option value="question">Question simple</option>
          <option value="ouverte">Question ouverte</option>
          <option value="qcm">QCM</option>
        </select>
      </div>

      <div class="input-group input-group-sm mb-2">
        <input v-model="newQuestionTitle" @keyup.enter="ajouterQuestion" placeholder="Texte de la nouvelle question" class="form-control">
      </div>

      <div v-if="newQuestionType === 'ouverte'" class="input-group input-group-sm mb-2">
        <input v-model="newQuestionReponse" placeholder="Réponse attendue" class="form-control">
      </div>

      <div v-if="newQuestionType === 'qcm'" class="row g-2 mb-2">
        <div class="col-md-4">
          <input v-model="newQuestionP1" placeholder="Proposition 1" class="form-control form-control-sm">
        </div>
        <div class="col-md-4">
          <input v-model="newQuestionP2" placeholder="Proposition 2" class="form-control form-control-sm">
        </div>
        <div class="col-md-4">
          <input
            v-model.number="newQuestionBonneReponse"
            type="number"
            min="1"
            max="2"
            placeholder="Bonne réponse (1 ou 2)"
            class="form-control form-control-sm"
          >
        </div>
      </div>

      <div>
        <button @click="ajouterQuestion" class="btn btn-success btn-sm">Ajouter question</button>
      </div>
    </div>
  </li>
</template>