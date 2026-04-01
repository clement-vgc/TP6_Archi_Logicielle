<script>
export default {
  props: {
    question: Object,
    canEdit: {
      type: Boolean,
      default: true
    }
  },
  emits: ['remove', 'update'],
  data() {
    return {
      editing: false,
      editTitle: '',
      editOpenAnswers: [''],
      editQcmChoices: [{ text: '', is_correct: false }]
    };
  },
  methods: {
    suppr() {
      this.$emit('remove', { id: this.question.id });
    },

    startEdit() {
      this.editing = true;
      this.editTitle = this.question.title || '';

      if (this.question.type === 'ouverte') {
        const answers = Array.isArray(this.question.bonnes_reponses) ? this.question.bonnes_reponses : [];
        this.editOpenAnswers = answers.length > 0 ? [...answers] : [''];
      }

      if (this.question.type === 'qcm') {
        const choices = Array.isArray(this.question.propositions) ? this.question.propositions : [];
        this.editQcmChoices = choices.length > 0
          ? choices.map((c) => ({ text: c.text || '', is_correct: !!c.is_correct }))
          : [{ text: '', is_correct: false }];
      }
    },

    cancelEdit() {
      this.editing = false;
    },

    addOpenAnswerField() {
      this.editOpenAnswers.push('');
    },

    removeOpenAnswerField(index) {
      this.editOpenAnswers.splice(index, 1);
      if (this.editOpenAnswers.length === 0) {
        this.editOpenAnswers.push('');
      }
    },

    addQcmChoiceField() {
      this.editQcmChoices.push({ text: '', is_correct: false });
    },

    removeQcmChoiceField(index) {
      this.editQcmChoices.splice(index, 1);
      if (this.editQcmChoices.length === 0) {
        this.editQcmChoices.push({ text: '', is_correct: false });
      }
    },

    saveEdit() {
      const title = this.editTitle.trim();
      if (!title) {
        return;
      }

      const data = { title };

      if (this.question.type === 'ouverte') {
        data.bonnes_reponses = this.editOpenAnswers
          .map((answer) => answer.trim())
          .filter((answer) => answer !== '');
      }

      if (this.question.type === 'qcm') {
        data.propositions = this.editQcmChoices
          .map((choice) => ({ text: choice.text.trim(), is_correct: !!choice.is_correct }))
          .filter((choice) => choice.text !== '');
      }

      this.$emit('update', {
        id: this.question.id,
        data
      });

      this.editing = false;
    }
  }
}
</script>

<template>
  <li class="list-group-item">
    <div v-if="!editing" class="d-flex justify-content-between align-items-start gap-2">
      <div>
        <strong>Q{{ question.number }} :</strong> {{ question.title }}
        <small class="text-muted ms-2">({{ question.type }})</small>
        <div v-if="question.type === 'ouverte'" class="small text-muted mt-1">
          Bonnes réponses: {{ (question.bonnes_reponses || []).join(', ') || 'Aucune' }}
        </div>
        <div v-if="question.type === 'qcm'" class="small text-muted mt-1">
          <div v-for="(choice, idx) in (question.propositions || [])" :key="`view-choice-${question.id}-${idx}`">
            <span>{{ idx + 1 }}) {{ choice.text }}</span>
            <span v-if="choice.is_correct"> - Bonne réponse</span>
          </div>
        </div>
      </div>

      <div class="d-flex gap-2">
        <button v-if="canEdit" class="btn btn-warning btn-sm" @click="startEdit">Modifier</button>
        <button class="btn btn-danger btn-sm" @click="suppr">Supprimer</button>
      </div>
    </div>

    <div v-else>
      <div class="input-group input-group-sm mb-2">
        <span class="input-group-text">Titre</span>
        <input v-model="editTitle" class="form-control">
      </div>

      <div v-if="question.type === 'ouverte'" class="mb-2">
        <div
          v-for="(answer, idx) in editOpenAnswers"
          :key="`edit-open-${question.id}-${idx}`"
          class="input-group input-group-sm mb-2"
        >
          <input v-model="editOpenAnswers[idx]" class="form-control" placeholder="Bonne réponse possible">
          <button class="btn btn-outline-danger" @click="removeOpenAnswerField(idx)">-</button>
        </div>
        <button class="btn btn-outline-secondary btn-sm" @click="addOpenAnswerField">Ajouter une bonne réponse</button>
      </div>

      <div v-if="question.type === 'qcm'" class="mb-2">
        <p class="small text-muted mb-2">
          Cochez une proposition si elle est correcte.
        </p>
        <div
          v-for="(choice, idx) in editQcmChoices"
          :key="`edit-qcm-${question.id}-${idx}`"
          class="input-group input-group-sm mb-2"
        >
          <span class="input-group-text">
            <input type="checkbox" v-model="editQcmChoices[idx].is_correct" title="Bonne réponse">
          </span>
          <input v-model="editQcmChoices[idx].text" class="form-control" placeholder="Proposition">
          <button class="btn btn-outline-danger" @click="removeQcmChoiceField(idx)">-</button>
        </div>
        <button class="btn btn-outline-secondary btn-sm" @click="addQcmChoiceField">Ajouter une proposition</button>
      </div>

      <div class="d-flex gap-2">
        <button class="btn btn-success btn-sm" @click="saveEdit">Enregistrer</button>
        <button class="btn btn-secondary btn-sm" @click="cancelEdit">Annuler</button>
      </div>
    </div>
  </li>
</template>