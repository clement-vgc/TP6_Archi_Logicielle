import { createRouter, createWebHistory } from 'vue-router'
import JouerQuiz from './components/JouerQuiz.vue'
import EditerQuiz from './components/EditerQuiz.vue'
import ModifierQuiz from './components/ModifierQuiz.vue'
import ConsulterQuiz from './components/ConsulterQuiz.vue'
import CreerQuiz from './components/CreerQuiz.vue'
import Connexion from './components/Connexion.vue'
import { isAuthenticated } from './auth.js'

const routes = [
  { path: '/', redirect: '/joueur' },
  { path: '/joueur', component: JouerQuiz },
  { path: '/connexion', component: Connexion },
  { path: '/edition', component: EditerQuiz, meta: { requiresAuth: true } },
  {
    path: '/edition/creer',
    component: CreerQuiz,
    meta: { requiresAuth: true }
  },
  {
    path: '/edition/:id/modifier',
    component: ModifierQuiz,
    meta: { requiresAuth: true }
  },
  {
    path: '/edition/:id/consulter',
    component: ConsulterQuiz,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    alert('Connexion requise pour accéder au mode édition.');
    next('/connexion');
    return;
  }

  next();
})

export default router