<script>
import TodoItem from './components/TodoItem.vue';

export default {
  components: { TodoItem },
  data() {
    return {
      todos: [],
      title: 'Mes questionnaires',
      newItem: ''
    };
  },
  mounted() {
    this.getAllTodos();
  },
  methods: {
    getAllTodos() {
      fetch('http://127.0.0.1:5000/quiz/api/v1.0/questionnaires')
        .then(response => response.json())
        .then(data => {
          this.todos = data.questionnaires || [];
        })
        .catch(err => console.error("Erreur de récupération:", err));
    },

    addItem() {
      let text = this.newItem.trim();
      if (text) {
        fetch('http://127.0.0.1:5000/quiz/api/v1.0/questionnaires', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: text })
        })
        .then(response => response.json())
        .then(data => {
          if (data.questionnaire) {
            this.todos.push(data.questionnaire);
            this.newItem = '';
          }
        })
        .catch(err => console.error("Erreur d'ajout:", err));
      }
    },

    removeItem(id) {
      if (id == null) {
        console.error("Suppression impossible: id manquant");
        return;
      }
      fetch(`http://127.0.0.1:5000/quiz/api/v1.0/questionnaires/${id}`, {
        method: 'DELETE'
      })
      .then(response => response.json())
      .then(() => {
        this.todos = this.todos.filter(t => t.id !== id);
      })
      .catch(err => console.error("Erreur suppression:", err));
    }
  }
}
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
  
  <div class="container mt-4">
    <h2 class="mb-4">{{ title }}</h2>
    
    <ol class="list-group mb-4">
      <TodoItem 
        v-for="todo in todos" 
        :key="todo.id" 
        :todo="todo"
        @remove="removeItem"
      />
    </ol>

    <div class="input-group">
      <input v-model="newItem" 
             @keyup.enter="addItem" 
              placeholder="Ajouter un questionnaire" 
             type="text"
             class="form-control">
      <button @click="addItem" class="btn btn-primary" type="button">Ajouter</button>
    </div>
  </div>
</template>