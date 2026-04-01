import { createRouter, createWebHistory } from 'vue-router'
import JouerQuiz from './components/JouerQuiz.vue'
import EditerQuiz from './components/EditerQuiz.vue'
import ModifierQuiz from './components/ModifierQuiz.vue'
import ConsulterQuiz from './components/ConsulterQuiz.vue'
import CreerQuiz from './components/CreerQuiz.vue'

const routes = [
  { path: '/', redirect: '/joueur' },
  { path: '/joueur', component: JouerQuiz },
  { 
    path: '/edition', 
    component: EditerQuiz,
    beforeEnter: (to, from, next) => {
      if (to.query.fromModifier === '1') {
        next();
        return;
      }
      let mdp = prompt("Mot de passe requis ('admin') :");
      if (mdp === 'admin') {
        next();
      } else {
        alert("Mot de passe incorrect.");
        next(false);
      }
    }
  },
  {
    path: '/edition/creer',
    component: CreerQuiz
  },
  {
    path: '/edition/:id/modifier',
    component: ModifierQuiz
  },
  {
    path: '/edition/:id/consulter',
    component: ConsulterQuiz
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router