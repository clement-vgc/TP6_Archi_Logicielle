import { createRouter, createWebHistory } from 'vue-router'
import JouerQuiz from './components/JouerQuiz.vue'
import EditerQuiz from './components/EditerQuiz.vue'

const routes = [
  { path: '/', redirect: '/joueur' },
  { path: '/joueur', component: JouerQuiz },
  { 
    path: '/edition', 
    component: EditerQuiz,
    beforeEnter: (to, from, next) => {
      let mdp = prompt("Mot de passe requis ('admin') :");
      if (mdp === 'admin') {
        next();
      } else {
        alert("Mot de passe incorrect.");
        next(false);
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router