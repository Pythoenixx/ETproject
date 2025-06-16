<template> 
  <div class="container py-5">
    <h2 class="mb-4 text-center">🌱 Regime Sustainability Analysis</h2>

    <div class="mb-4 text-center">
      <p>Select regimes to compare sustainability metrics:</p>
      <div class="btn-group">
        <button
          v-for="regime in regimes"
          :key="regime"
          class="btn btn-outline-success"
          :class="{ active: selectedRegimes.includes(regime) }"
          @click="toggleRegime(regime)"
        >
          Regime {{ regime }}
        </button>
      </div>
    </div>

    <div class="mb-3 text-center">
      <label for="metricSelect" class="form-label fw-semibold">Comparison Type:</label>
      <select id="metricSelect" v-model="selectedMetric" class="form-select w-auto d-inline-block ms-2">
        <option value="volume">Volume (m³)</option>
        <option value="number">Number of Trees</option>
      </select>
    </div>

    <div v-if="loading" class="text-center">Loading data...</div>
    <div v-else-if="selectedRegimes.length === 0" class="text-center text-muted">
      Please select at least one regime.
    </div>
    <div v-else>
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  components: { Bar },
  data() {
    return {
      regimes: ['45', '50', '55', '60', '65'],
      selectedRegimes: ['45', '50', '55', '60', '65'],
      selectedMetric: 'volume', // 'volume' or 'number'
      sustainabilityData: {},   // will store values per regime
      loading: true,
    };
  },
  computed: {
    chartData() {
      const labels = this.selectedRegimes;
      const metricLabel = this.selectedMetric === 'number' ? 'Num' : 'Vol';

      return {
        labels,
        datasets: [
          {
            label: this.selectedMetric === 'number' ? 'Total Trees' : 'Total Production (m³)',
            backgroundColor: '#28a745',
            data: labels.map(r => this.sustainabilityData[r]?.production || 0),
          },
          {
            label: this.selectedMetric === 'number' ? 'Remaining Trees' : 'Remaining Volume (m³)',
            backgroundColor: '#007bff',
            data: labels.map(r => this.sustainabilityData[r]?.remaining || 0),
          },
          {
            label: this.selectedMetric === 'number' ? 'Damaged Trees' : 'Damage Volume (m³)',
            backgroundColor: '#dc3545',
            data: labels.map(r => this.sustainabilityData[r]?.damage || 0),
          },
          {
            label: '30-Year Production',
            backgroundColor: '#ffc107',
            data: labels.map(r => this.sustainabilityData[r]?.prod30 || 0),
          },
        ],
      };
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: {
            display: true,
            text: 'Sustainability Comparison by Regime',
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: this.selectedMetric === 'number' ? 'Number of Trees' : 'Volume (m³)',
            },
          },
        },
      };
    },
  },
  methods: {
    toggleRegime(regime) {
      if (this.selectedRegimes.includes(regime)) {
        this.selectedRegimes = this.selectedRegimes.filter(r => r !== regime);
      } else {
        this.selectedRegimes.push(regime);
      }
    },
    calculateTotalByMetric(data, metricType) {
      let total = 0;
      for (const row of data) {
        if (row.metric_type === metricType) {
          const value = parseFloat(row.Total);
          if (!isNaN(value)) total += value;
        }
      }
      return Number(total.toFixed(2));
    },
    async fetchAllData() {
      this.loading = true;
      const results = {};
      const metricType = this.selectedMetric === 'number' ? 'Num' : 'Vol';

      for (const regime of this.regimes) {
        try {
          const [prodRes, remRes, dmgRes, genRes, prod30Res] = await Promise.all([
            fetch(`http://localhost:5000/api/stand-table-production?regime=${regime}`),
            fetch(`http://localhost:5000/api/stand-table-remaining?regime=${regime}`),
            fetch(`http://localhost:5000/api/stand-table-damage?regime=${regime}`),
            fetch(`http://localhost:5000/api/stand-table-general?regime=${regime}`),
            fetch(`http://localhost:5000/api/stand-table-production30?regime=${regime}`),
          ]);

          const [prodData, remData, dmgData, genData, prod30Data] = await Promise.all([
            prodRes.json(),
            remRes.json(),
            dmgRes.json(),
            genRes.json(),
            prod30Res.json(),
          ]);

          results[regime] = {
            production: this.calculateTotalByMetric(prodData, metricType),
            remaining: this.calculateTotalByMetric(remData, metricType),
            damage: this.calculateTotalByMetric(dmgData, metricType),
            general: this.calculateTotalByMetric(genData, metricType),
            prod30: this.calculateTotalByMetric(prod30Data, metricType),
          };
        } catch (err) {
          console.error(`Error fetching data for regime ${regime}:`, err);
        }
      }

      this.sustainabilityData = results;
      this.loading = false;
    },
  },
  watch: {
    selectedMetric() {
      this.fetchAllData(); // refetch when user switches between "number" and "volume"
    },
  },
  mounted() {
    this.fetchAllData();
  },
};
</script>

<style scoped>
.container {
  max-width: 1000px;
}
.btn-group .btn.active {
  background-color: #28a745;
  color: white;
  border-color: #28a745;
}
</style>
