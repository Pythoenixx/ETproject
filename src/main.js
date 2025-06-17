import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import CreateForest from './components/CreateForest.vue'
import TreeList from './components/TreeList.vue'
import FinalOuput from './components/FinalOutput.vue'
import TreeMap from './components/TreeMap.vue'
import Regime from './components/Regime.vue'
import StandTable from './components/StandTable.vue'
import StandTableProduction from './components/StandTableProduction.vue'
import StandTableDamage from './components/StandTableDamage.vue'
import StandTableRemaining from './components/StandTableRemaining.vue'
import StandTableGeneral30 from './components/StandTableGeneral30.vue'
import StandTableProduction30 from './components/StandTableProduction30.vue'
import Analysis from './components/Analysis.vue'
import './style.css'

const routes = [
  { path: '/', component: Home },
  { path: '/create-forest', component: CreateForest },
  { path: '/list-of-trees', component: TreeList },
  { path: '/tree-map', component: TreeMap },
  { path: '/final-output', component: FinalOuput },
  { path: '/stand-table/general', component: StandTable },
  { path: '/stand-table/production', component: StandTableProduction },
  { path: '/stand-table/damage', component: StandTableDamage },
  { path: '/stand-table/remaining', component: StandTableRemaining },
  { path: '/stand-table/general30', component: StandTableGeneral30 },
  { path: '/stand-table/production30', component: StandTableProduction30 },
  { path: '/regime', component: Regime },
  { path: '/analysis', component: Analysis },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
