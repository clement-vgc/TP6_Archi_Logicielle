<script>
import RepondreQuizItem from './RepondreQuizItem.vue';

const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires';

export default {
  components: { RepondreQuizItem },
  data() {
    return {
      questionnaires: [],
      quizActuel: null,
      reponsesUtilisateur: {},
      score: null,
      quizTermine: false
    };
  },
  mounted() {
    this.chargerQuestionnaires();
  },
  methods: {
    async chargerQuestionnaires() {
      let response = await fetch(API_URL);
      let data = await response.json();
      this.questionnaires = data.questionnaires;
    },
    
    demarrerQuiz(quiz) {
      this.quizActuel = quiz;
      this.reponsesUtilisateur = {};
      this.score = null;
      this.quizTermine = false;
    },

    noterReponse(payload) {
      this.reponsesUtilisateur[payload.questionId] = payload.answer;
    },

    terminerQuiz() {
      let points = 0;
      
      this.quizActuel.questions.forEach(q => {
        let reponseDonnee = this.reponsesUtilisateur[q.id];
        
        if (!reponseDonnee) return; 

        if (q.type === 'qcm') {
          let bonneReponse = q.propositions.find(p => p.is_correct);
          if (bonneReponse && reponseDonnee === bonneReponse.text) {
            points++;
          }
        } else if (q.type === 'ouverte') {
          let repUserLower = reponseDonnee.toLowerCase().trim();
          
          let estCorrect = q.bonnes_reponses.some(bonneRep => 
            bonneRep.toLowerCase().trim() === repUserLower
          );
          
          if (estCorrect) {
            points++;
          }
        } else {
            if (q.answer && q.answer.toLowerCase().trim() === reponseDonnee.toLowerCase().trim()) {
                points++;
            }
        }
      });

      this.score = points;
      this.quizTermine = true;
    },
    
    retourMenu() {
        this.quizActuel = null;
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-primary">Mode Joueur - Répondre au Quiz</h2>

    <div v-if="!quizActuel">
      <h4>Choisissez un quiz pour commencer :</h4>
      <div class="list-group mt-3">
        <button 
          v-for="q in questionnaires" 
          :key="q.id" 
          class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
          @click="demarrerQuiz(q)"
        >
          {{ q.name }}
          <span class="badge bg-primary rounded-pill">{{ q.questions ? q.questions.length : 0 }} questions</span>
        </button>
      </div>
    </div>

    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>Quiz : {{ quizActuel.name }}</h3>
        <button class="btn btn-outline-secondary btn-sm" @click="retourMenu">Changer de quiz</button>
      </div>

      <div v-if="!quizTermine">
        <RepondreQuizItem 
          v-for="(question, index) in quizActuel.questions" 
          :key="question.id" 
          :question="question"
          :index="index"
          @reponse="noterReponse"
        />
        <button class="btn btn-success mt-3" @click="terminerQuiz">Valider mes réponses</button>
      </div>

      <div v-else class="alert alert-success mt-4">
        <h4 class="alert-heading">Quiz terminé !</h4>
        <p class="mb-0">Votre score est de <strong>{{ score }} / {{ quizActuel.questions.length }}</strong>.</p>
        <button class="btn btn-primary mt-3" @click="retourMenu">Retour à la liste</button>
      </div>
    </div>
  </div>
</template>