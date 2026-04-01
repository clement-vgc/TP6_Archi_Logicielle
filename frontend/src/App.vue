<script>
import QuestionItem from './components/QuestionItem.vue';
import JouerQuiz from './components/JouerQuiz.vue';

const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires';

export default {
  components: { QuestionItem, JouerQuiz },
  data() {
    return {
      modeActuel: 'edition',
      questionnaires: [],
      selectedQuiz: null,
      newQuizName: '',
      newQuestionTitle: '',
      newQuestionType: 'question',
      newOpenAnswers: [''],
      newQcmChoices: [
        { text: '', is_correct: false },
        { text: '', is_correct: false }
      ]
    };
  },
  mounted() {
    this.fetchQuestionnaires();
  },
  methods: {
    async fetchQuestionnaires() {
      let response = await fetch(API_URL);
      let data = await response.json();
      this.questionnaires = data.questionnaires || data;

      if (this.selectedQuiz) {
        const stillExists = this.questionnaires.some((q) => q.id === this.selectedQuiz.id);
        if (!stillExists) {
          this.selectedQuiz = null;
        }
      }
    },

    async fetchOneQuiz(qid) {
      const response = await fetch(`${API_URL}/${qid}`);
      if (!response.ok) {
        this.selectedQuiz = null;
        return;
      }
      const data = await response.json();
      this.selectedQuiz = data.questionnaire;
    },

    async consulterQuiz(qid) {
      await this.fetchOneQuiz(qid);
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
        await this.fetchQuestionnaires();
      }
    },
    
    async removeQuiz(id) {
      await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      await this.fetchQuestionnaires();
      if (this.selectedQuiz && this.selectedQuiz.id === id) {
        this.selectedQuiz = null;
      }
    },

    async updateQuiz(id) {
      const q = this.questionnaires.find((item) => item.id === id);
      if (!q) return;

      const newName = prompt('Modifier le nom du quiz :', q.name);
      if (newName === null || newName.trim() === '') return;

      await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName.trim() })
      });

      await this.fetchQuestionnaires();
      if (this.selectedQuiz && this.selectedQuiz.id === id) {
        await this.fetchOneQuiz(id);
      }
    },

    async addQuestionToSelectedQuiz() {
      if (!this.selectedQuiz || this.newQuestionTitle.trim() === '') return;

      let payload = {
        title: this.newQuestionTitle.trim(),
        type: this.newQuestionType
      };

      if (this.newQuestionType === 'ouverte') {
        payload.bonnes_reponses = this.newOpenAnswers.map(a => a.trim()).filter(a => a !== '');
        if (payload.bonnes_reponses.length === 0) {
          alert('Ajout impossible: vous devez renseigner au moins une bonne réponse pour une question ouverte.');
          return;
        }
      } else if (this.newQuestionType === 'qcm') {
        payload.propositions = this.newQcmChoices
          .filter(choice => choice.text.trim() !== '')
          .map(choice => ({
            text: choice.text.trim(),
            is_correct: !!choice.is_correct
          }));

        if (payload.propositions.length === 0) {
          alert('Ajout impossible: vous devez renseigner au moins une proposition pour un QCM.');
          return;
        }
        if (!payload.propositions.some(choice => choice.is_correct)) {
          alert('Ajout impossible: cochez au moins une bonne réponse pour le QCM.');
          return;
        }
      }

      await fetch(`${API_URL}/${this.selectedQuiz.id}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      this.newQuestionTitle = '';
      this.newQuestionType = 'question';
      this.newOpenAnswers = [''];
      this.newQcmChoices = [
        { text: '', is_correct: false },
        { text: '', is_correct: false }
      ];

      await this.fetchOneQuiz(this.selectedQuiz.id);
      await this.fetchQuestionnaires();
    },

    async removeQuestionFromSelectedQuiz(payload) {
      if (!this.selectedQuiz) return;

      await fetch(`${API_URL}/${this.selectedQuiz.id}/questions/${payload.id || payload.number}`, {
        method: 'DELETE' 
      });

      await this.fetchOneQuiz(this.selectedQuiz.id);
      await this.fetchQuestionnaires();
    },

    async updateQuestionInSelectedQuiz(payload) {
      if (!this.selectedQuiz) return;

      await fetch(`${API_URL}/${this.selectedQuiz.id}/questions/${payload.id || payload.number}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload.data)
      });

      await this.fetchOneQuiz(this.selectedQuiz.id);
      await this.fetchQuestionnaires();
    },

    addOpenAnswerField() {
      this.newOpenAnswers.push('');
    },

    removeOpenAnswerField(index) {
      this.newOpenAnswers.splice(index, 1);
      if (this.newOpenAnswers.length === 0) this.newOpenAnswers.push('');
    },

    addQcmChoiceField() {
      this.newQcmChoices.push({ text: '', is_correct: false });
    },

    removeQcmChoiceField(index) {
      this.newQcmChoices.splice(index, 1);
      if (this.newQcmChoices.length === 0) this.newQcmChoices.push({ text: '', is_correct: false });
    }
  }
}
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" crossorigin="anonymous">
  
  <div class="container mt-4">
    
    <div class="d-flex justify-content-center mb-5 pb-3 border-bottom">
      <button 
        class="btn me-3" 
        :class="modeActuel === 'edition' ? 'btn-primary' : 'btn-outline-primary'" 
        @click="modeActuel = 'edition'"
      >
        Mode Édition
      </button>
      <button 
        class="btn" 
        :class="modeActuel === 'joueur' ? 'btn-success' : 'btn-outline-success'" 
        @click="modeActuel = 'joueur'"
      >
        Mode Joueur
      </button>
    </div>

    <div v-if="modeActuel === 'edition'">
      <h2 class="mb-4">Gestion des quiz</h2>
      
      <div class="input-group mb-4">
        <input v-model="newQuizName" @keyup.enter="addQuiz" placeholder="Nom du nouveau quiz" class="form-control">
        <button @click="addQuiz" class="btn btn-primary">Créer le quiz</button>
      </div>

      <div class="row g-4">
        <div class="col-lg-5">
          <h4 class="mb-3">Liste des quiz</h4>
          <ul class="list-group">
            <li
              v-for="q in questionnaires"
              :key="q.id"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <div class="fw-semibold">{{ q.name }}</div>
                <small class="text-muted">ID: {{ q.id }}</small>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-primary btn-sm" @click="consulterQuiz(q.id)">Consulter</button>
                <button class="btn btn-warning btn-sm" @click="updateQuiz(q.id)">Modifier</button>
                <button class="btn btn-danger btn-sm" @click="removeQuiz(q.id)">Supprimer</button>
              </div>
            </li>
          </ul>
        </div>

        <div class="col-lg-7">
          <div v-if="selectedQuiz" class="card shadow-sm">
            <div class="card-body">
              <h4 class="card-title mb-3">Quiz consulté: {{ selectedQuiz.name }}</h4>

              <h5>Questions</h5>
              <ul class="list-group mb-3">
                <QuestionItem
                  v-for="question in selectedQuiz.questions"
                  :key="question.id"
                  :question="question"
                  @remove="removeQuestionFromSelectedQuiz"
                  @update="updateQuestionInSelectedQuiz"
                />
              </ul>

              <h6 class="mb-2 mt-4 text-primary">Ajouter une question</h6>
              <div class="mb-2">
                <select v-model="newQuestionType" class="form-select form-select-sm">
                  <option value="question">Question simple</option>
                  <option value="ouverte">Question ouverte</option>
                  <option value="qcm">QCM</option>
                </select>
              </div>

              <div class="input-group input-group-sm mb-3">
                <input
                  v-model="newQuestionTitle"
                  @keyup.enter="addQuestionToSelectedQuiz"
                  placeholder="Texte de la nouvelle question"
                  class="form-control"
                >
              </div>

              <div v-if="newQuestionType === 'ouverte'" class="mb-3 p-3 border rounded bg-light">
                <p class="small fw-bold">Bonnes réponses acceptées :</p>
                <div
                  v-for="(answer, index) in newOpenAnswers"
                  :key="`open-answer-${index}`"
                  class="input-group input-group-sm mb-2"
                >
                  <input v-model="newOpenAnswers[index]" placeholder="Ex: Paris" class="form-control">
                  <button class="btn btn-outline-danger" @click="removeOpenAnswerField(index)">-</button>
                </div>
                <button class="btn btn-outline-secondary btn-sm" @click="addOpenAnswerField">Ajouter une variante</button>
              </div>

              <div v-if="newQuestionType === 'qcm'" class="mb-3 p-3 border rounded bg-light">
                <p class="small fw-bold mb-2">
                  Cochez la case devant une proposition pour indiquer que c'est une bonne réponse.
                </p>
                <div
                  v-for="(choice, index) in newQcmChoices"
                  :key="`qcm-choice-${index}`"
                  class="input-group input-group-sm mb-2"
                >
                  <span class="input-group-text bg-white">
                    <input type="checkbox" v-model="newQcmChoices[index].is_correct">
                  </span>
                  <input v-model="newQcmChoices[index].text" placeholder="Proposition" class="form-control">
                  <button class="btn btn-outline-danger" @click="removeQcmChoiceField(index)">-</button>
                </div>
                <button class="btn btn-outline-secondary btn-sm" @click="addQcmChoiceField">Ajouter une proposition</button>
              </div>

              <button @click="addQuestionToSelectedQuiz" class="btn btn-success">Enregistrer la question</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <JouerQuiz v-else />

  </div>
</template>