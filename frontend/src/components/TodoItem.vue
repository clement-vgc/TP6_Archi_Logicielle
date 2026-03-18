<script>
export default {
  props: {
    todo: Object 
  },
  data() {
    return {
      editingText: this.todo.name
    }
  },
  emits: ['remove'], 
  methods: {
    suppr: function() {
      this.$emit('remove', this.todo.id);
    },
    modifier: function(){
      if (this.todo.id == null) {
        console.error("Modification impossible: id manquant");
        return;
      }

      fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${this.todo.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: this.editingText
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.questionnaire) {
          this.todo.name = data.questionnaire.name;
        }
      })
      .catch(err => console.error("Erreur modification:", err));
    }
  }
}
</script>

<template>
  <li class="mb-3 p-2 border rounded">
    <div class="d-flex align-items-center justify-content-between">
      <div>
        {{ todo.name }}
      </div>
      
      <input type="button" class="btn btn-danger btn-sm" value="Supprimer" @click="suppr">
    </div>

    <div class="input-group mt-2">
      <input v-model="editingText" class="form-control form-control-sm" type="text">
      <button @click="modifier" class="btn btn-warning btn-sm">Modifier</button>
    </div>
  </li>
</template>