import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import DataVisualization from './components/DataVisualization.vue'
import TreeList from './components/TreeList.vue'
import TreePlot from './components/TreePlot.vue'
import './style.css'

const routes = [
  { path: '/', component: Home },
  { path: '/data-visualization', component: DataVisualization },
  { path: '/list-of-trees', component: TreeList },
  { path: '/tree-plot', component: TreePlot },
  { path: '/production-data', component: { template: '<div class="container py-5"><h2>Production Data - Coming Soon</h2></div>' } },
  { path: '/cutting-regions', component: { template: '<div class="container py-5"><h2>Cutting Regions - Coming Soon</h2></div>' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
