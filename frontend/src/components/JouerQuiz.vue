<script>
import RepondreQuizItem from './RepondreQuizItem.vue';

const API_URL = 'http://127.0.0.1:5000/quiz/api/v1.0/questionnaires'

export default {
  components: { RepondreQuizItem },
  data() {
    return {
      questionnaires: [],
      quizActuel: null,
      reponsesUtilisateur: {},
      score: null,
      quizTermine: false,
      currentQuestionIndex: 0,
      resultatsDetailles: [] 
    };
  },
  computed: {
    questionCourante() {
      if (!this.quizActuel || !this.quizActuel.questions) return null;
      return this.quizActuel.questions[this.currentQuestionIndex];
    },
    estDerniereQuestion() {
      if (!this.quizActuel || !this.quizActuel.questions) return false;
      return this.currentQuestionIndex === this.quizActuel.questions.length - 1;
    }
  },
  mounted() {
    this.chargerQuestionnaires();
  },
  methods: {
    async chargerQuestionnaires() {
      let response = await fetch(API_URL);
      let data = await response.json();
      this.questionnaires = data.questionnaires || data;
    },
    
    async demarrerQuiz(quizBase) {
      try {
        let response = await fetch(`${API_URL}/${quizBase.id}`);
        let data = await response.json();
        
        this.quizActuel = data.questionnaire || data;
        
        if (!this.quizActuel.questions) {
          this.quizActuel.questions = [];
        }

        this.reponsesUtilisateur = {};
        this.score = null;
        this.quizTermine = false;
        this.currentQuestionIndex = 0;
        this.resultatsDetailles = [];
      } catch (error) {
        console.error("Erreur lors de la récupération du quiz :", error);
        alert("Impossible de charger les questions de ce quiz.");
      }
    },

    noterReponse(payload) {
      this.reponsesUtilisateur[payload.questionId] = payload.answer;
    },

    questionSuivante() {
      if (!this.estDerniereQuestion) this.currentQuestionIndex++;
    },

    questionPrecedente() {
      if (this.currentQuestionIndex > 0) this.currentQuestionIndex--;
    },

    terminerQuiz() {
      let points = 0;
      this.resultatsDetailles = [];
      
      this.quizActuel.questions.forEach(q => {
        let reponseDonnee = this.reponsesUtilisateur[q.id] || "Aucune réponse";
        let estCorrect = false;
        let bonneReponseAttendue = "";

        if (q.type === 'qcm') {
          let bonneProp = q.propositions.find(p => p.is_correct);
          if (bonneProp) {
            bonneReponseAttendue = bonneProp.text;
            if (reponseDonnee === bonneProp.text) {
              estCorrect = true;
            }
          }
        } else if (q.type === 'ouverte') {
          bonneReponseAttendue = q.bonnes_reponses.join(" ou ");
          if (reponseDonnee !== "Aucune réponse") {
            let repUserLower = reponseDonnee.toLowerCase().trim();
            estCorrect = q.bonnes_reponses.some(bonneRep => 
              bonneRep.toLowerCase().trim() === repUserLower
            );
          }
        }

        if (estCorrect) points++;

        this.resultatsDetailles.push({
          titre: q.title,
          reponseUser: reponseDonnee,
          correct: estCorrect,
          reponseAttendue: bonneReponseAttendue
        });
      });

      this.score = points;
      this.quizTermine = true;
    },

    recommencerQuiz() {
      this.reponsesUtilisateur = {};
      this.score = null;
      this.quizTermine = false;
      this.currentQuestionIndex = 0;
      this.resultatsDetailles = [];
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
        
        <div class="mb-3 text-muted">
          Question {{ currentQuestionIndex + 1 }} sur {{ quizActuel.questions.length }}
        </div>

        <RepondreQuizItem 
          v-if="questionCourante"
          :key="questionCourante.id"
          :question="questionCourante"
          :index="currentQuestionIndex"
          :valeurPrecedente="reponsesUtilisateur[questionCourante.id]" 
          @reponse="noterReponse"
        />
        
        <div class="d-flex justify-content-between mt-3">
          <button class="btn btn-secondary" :disabled="currentQuestionIndex === 0" @click="questionPrecedente">Précédent</button>
          
          <button v-if="!estDerniereQuestion" class="btn btn-primary" @click="questionSuivante">Suivant</button>
          <button v-else class="btn btn-success" @click="terminerQuiz">Terminer le quiz</button>
        </div>
      </div>

      <div v-else class="mt-4">
        <div class="alert alert-success">
          <h4 class="alert-heading">Quiz terminé !</h4>
          <p class="mb-0">Votre score est de <strong>{{ score }} / {{ quizActuel.questions.length }}</strong>.</p>
        </div>

        <h4 class="mt-4 mb-3">Résumé de vos réponses</h4>
        <ul class="list-group mb-4">
          <li 
            v-for="(res, idx) in resultatsDetailles" 
            :key="idx" 
            class="list-group-item"
            :class="res.correct ? 'list-group-item-success' : 'list-group-item-danger'"
          >
            <h6 class="mb-1 fw-bold">Q{{ idx + 1 }} : {{ res.titre }}</h6>
            <div class="mb-1">
              <span>Votre réponse : </span> 
              <strong>{{ res.reponseUser }}</strong>
            </div>
            
            <div v-if="!res.correct" class="text-danger mt-2">
              <span class="fw-bold">Réponse attendue : </span> 
              <u>{{ res.reponseAttendue }}</u>
            </div>
          </li>
        </ul>

        <div class="d-flex gap-2">
          <button class="btn btn-warning" @click="recommencerQuiz">Recommencer ce quiz</button>
          <button class="btn btn-primary" @click="retourMenu">Retour à la liste</button>
        </div>
      </div>
    </div>
  </div>
</template>