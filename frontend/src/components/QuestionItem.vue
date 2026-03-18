<script>
export default {
  props: { question: Object },
  emits: ['remove'],
  methods: {
    suppr() {
      this.$emit('remove', { number: this.question.number });
    }
  }
}
</script>

<template>
  <li class="list-group-item d-flex justify-content-between align-items-center">
    <span><strong>Q{{ question.number }} :</strong> {{ question.title }}</span>
    <button class="btn btn-danger btn-sm" @click="suppr">Supprimer</button>
  </li>
</template>