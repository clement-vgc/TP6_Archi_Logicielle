<script>
import QuestionAdminItem from './QuestionAdminItem.vue';

const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires';

export default {
  components: { QuestionAdminItem },
  data() {
    return {
      quiz: null,
      loading: true,
      error: '',
      quizNameDraft: '',
      newQuestionTitle: '',
      newQuestionType: 'ouverte',
      newOpenAnswers: [''],
      newQcmChoices: [{ text: '', is_correct: false }, { text: '', is_correct: false }]
    };
  },
  mounted() {
    this.fetchQuiz();
  },
  watch: {
    '$route.params.id'() {
      this.fetchQuiz();
    }
  },
  methods: {
    async fetchQuiz() {
      this.loading = true;
      this.error = '';

      const response = await fetch(`${API_URL}/${this.$route.params.id}`);
      if (!response.ok) {
        this.quiz = null;
        this.error = 'Quiz introuvable.';
        this.loading = false;
        return;
      }

      const data = await response.json();
      this.quiz = data.questionnaire;
      this.quizNameDraft = this.quiz.name;
      this.loading = false;
    },

    async updateQuizName() {
      const newName = this.quizNameDraft.trim();
      if (!newName || !this.quiz) return;

      const response = await fetch(`${API_URL}/${this.quiz.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName })
      });

      if (!response.ok) {
        alert('Impossible de modifier le nom du quiz, il existe déjà.');
        return;
      }

      this.quiz.name = newName;
      alert('Nom du quiz mis a jour.');
    },

    async addQuestion() {
      if (!this.quiz || !this.newQuestionTitle.trim()) return;

      const payload = {
        title: this.newQuestionTitle.trim(),
        type: this.newQuestionType
      };

      if (this.newQuestionType === 'ouverte') {
        payload.bonnes_reponses = this.newOpenAnswers
          .map((answer) => answer.trim())
          .filter((answer) => answer !== '');

        if (!payload.bonnes_reponses.length) {
          alert('Au moins une bonne reponse est requise.');
          return;
        }
      }

      if (this.newQuestionType === 'qcm') {
        payload.propositions = this.newQcmChoices
          .filter((choice) => choice.text.trim())
          .map((choice) => ({ text: choice.text.trim(), is_correct: !!choice.is_correct }));

        if (!payload.propositions.length) {
          alert('Au moins une proposition est requise.');
          return;
        }

        if (!payload.propositions.some((choice) => choice.is_correct)) {
          alert('Cochez au moins une bonne reponse.');
          return;
        }
      }

      const response = await fetch(`${API_URL}/${this.quiz.id}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        alert('Impossible d\'ajouter la question.');
        return;
      }

      this.newQuestionTitle = '';
      this.newQuestionType = 'ouverte';
      this.newOpenAnswers = [''];
      this.newQcmChoices = [{ text: '', is_correct: false }, { text: '', is_correct: false }];
      await this.fetchQuiz();
    },

    async removeQuestion(payload) {
      if (!this.quiz) return;

      const response = await fetch(`${API_URL}/${this.quiz.id}/questions/${payload.id || payload.number}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        alert('Impossible de supprimer la question.');
        return;
      }

      await this.fetchQuiz();
    },

    async updateQuestion(payload) {
      if (!this.quiz) return;

      const response = await fetch(`${API_URL}/${this.quiz.id}/questions/${payload.id || payload.number}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload.data)
      });

      if (!response.ok) {
        alert('Impossible de modifier la question.');
        return;
      }

      await this.fetchQuiz();
    },

    addOpenAnswerField() {
      this.newOpenAnswers.push('');
    },

    removeOpenAnswerField(index) {
      this.newOpenAnswers.splice(index, 1);
      if (!this.newOpenAnswers.length) this.newOpenAnswers.push('');
    },

    addQcmChoiceField() {
      this.newQcmChoices.push({ text: '', is_correct: false });
    },

    removeQcmChoiceField(index) {
      this.newQcmChoices.splice(index, 1);
      if (!this.newQcmChoices.length) this.newQcmChoices.push({ text: '', is_correct: false });
    },

    retourVersEdition() {
      this.$router.push({ path: '/edition', query: { fromModifier: '1' } });
    }
  }
};
</script>

<template>
  <div class="mt-4">
    <button class="btn btn-outline-secondary btn-sm mb-3" @click="retourVersEdition">Retour a la liste</button>

    <div v-if="loading" class="alert alert-info">Chargement du quiz...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else class="card shadow-sm">
      <div class="card-body">
        <h3 class="mb-3">Edition complete du quiz</h3>

        <div class="input-group mb-4">
          <span class="input-group-text">Nom du quiz</span>
          <input v-model="quizNameDraft" class="form-control" placeholder="Nom du quiz">
          <button class="btn btn-primary" @click="updateQuizName">Enregistrer le nom</button>
        </div>

        <h5>Questions existantes</h5>
        <ul class="list-group mb-4">
          <QuestionAdminItem
            v-for="question in quiz.questions"
            :key="question.id"
            :question="question"
            @remove="removeQuestion"
            @update="updateQuestion"
          />
        </ul>

        <h5 class="text-primary">Ajouter une nouvelle question</h5>
        <div class="mb-2">
          <select v-model="newQuestionType" class="form-select form-select-sm">
            <option value="ouverte">Question ouverte</option>
            <option value="qcm">QCM</option>
          </select>
        </div>

        <div class="input-group input-group-sm mb-3">
          <input
            v-model="newQuestionTitle"
            @keyup.enter="addQuestion"
            placeholder="Texte de la nouvelle question"
            class="form-control"
          >
        </div>

        <div v-if="newQuestionType === 'ouverte'" class="mb-3 p-3 border rounded bg-light">
          <p class="small fw-bold">Bonnes reponses acceptees :</p>
          <div v-for="(answer, index) in newOpenAnswers" :key="`new-open-${index}`" class="input-group input-group-sm mb-2">
            <input v-model="newOpenAnswers[index]" class="form-control" placeholder="Ex: Paris">
            <button class="btn btn-outline-danger" @click="removeOpenAnswerField(index)">-</button>
          </div>
          <button class="btn btn-outline-secondary btn-sm" @click="addOpenAnswerField">Ajouter une variante</button>
        </div>

        <div v-if="newQuestionType === 'qcm'" class="mb-3 p-3 border rounded bg-light">
          <p class="small fw-bold mb-2">Cochez les bonnes reponses :</p>
          <div v-for="(choice, index) in newQcmChoices" :key="`new-qcm-${index}`" class="input-group input-group-sm mb-2">
            <span class="input-group-text bg-white"><input type="checkbox" v-model="newQcmChoices[index].is_correct"></span>
            <input v-model="newQcmChoices[index].text" class="form-control" placeholder="Proposition">
            <button class="btn btn-outline-danger" @click="removeQcmChoiceField(index)">-</button>
          </div>
          <button class="btn btn-outline-secondary btn-sm" @click="addQcmChoiceField">Ajouter proposition</button>
        </div>

        <button class="btn btn-success" @click="addQuestion">Ajouter la question</button>
      </div>
    </div>
  </div>
</template>
