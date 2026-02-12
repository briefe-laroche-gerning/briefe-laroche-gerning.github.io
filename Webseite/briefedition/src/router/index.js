import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/briefe',
    name: 'briefe',
    component: () => import('../views/LettersView.vue')
  },
  {
  path: '/personenregister',
  name: 'personenregister',
  component: () => import('../components/Register.vue'),
  props: {
    url: '/data/register/personenregister.json',
    title: 'Personenregister',
    type: 'person'
  }
},
{
  path: '/ortsregister',
  name: 'ortsregister',
  component: () => import('../views/OrtsregisterView.vue'),
  props: {
    url: '/data/register/ortsregister.json',
    title: 'Ortsregister',
    type: 'place'
  }
},
{
  path: '/werkregister',
  name: 'werkregister',
  component: () => import('../views/WerkregisterView.vue'),
  props: {
    url: '/data/register/werkregister.json',
    title: 'Werkregister',
    type: 'work'
  }
},
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/brief:nr',
    name: 'brief',
    component: () => import('@/views/SingleLetterView.vue'),
    props: true
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' };
    }
    return { top: 0 };
  }
});


export default router
