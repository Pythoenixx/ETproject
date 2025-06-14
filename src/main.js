import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import CreateForest from './components/CreateForest.vue'
import TreeList from './components/TreeList.vue'
import FinalOuput from './components/FinalOutput.vue'
import StandTable from './components/StandTable.vue'
import TreeMap from './components/TreeMap.vue'
import CuttingRegime from './components/CuttingRegime.vue'
import './style.css'

const routes = [
  { path: '/', component: Home },
  { path: '/create-forest', component: CreateForest },
  { path: '/list-of-trees', component: TreeList },
  { path: '/tree-map', component: TreeMap },
  { path: '/final-output', component: FinalOuput },
    { path: '/stand-table', component: StandTable },
  { path: '/production-data', component: { template: '<div class="container py-5"><h2>Production Data - Coming Soon</h2></div>' } },
    { path: '/cutting-regime', component: CuttingRegime },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
