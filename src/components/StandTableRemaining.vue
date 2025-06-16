<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
              <h1 class="display-6 fw-bold mb-2">
                <i class="bi bi-archive-fill me-2"></i>Stand Table Remaining
              </h1>
              <p class="lead mb-0">Remaining volume by species group and diameter class</p>

              <!-- Regime Selector -->
              <div class="mt-4">
                <label for="regime-select" class="form-label text-white">Select Regime:</label>
                <select
                  id="regime-select"
                  class="form-select w-auto mx-auto"
                  v-model="selectedRegime"
                  @change="fetchData"
                >
                  <option v-for="regime in regimes" :key="regime" :value="regime">{{ regime }}</option>
                </select>
              </div>
            </div>

            <!-- Content -->
            <div class="card-body p-4">
              <!-- Loading Spinner -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-success" role="status" style="width: 3rem; height: 3rem;">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Loading data for Stand Table Remaining {{ selectedRegime }}...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger text-center">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
              </div>

            <!-- Toggle + Table Content -->
            <div v-else>
            <!-- Toggle Buttons -->
            <div class="text-center mb-4">
                <div class="btn-group">
                <button 
                    class="btn btn-outline-success" 
                    :class="{ active: selectedMetric === 'Num' }" 
                    @click="selectedMetric = 'Num'">
                    View by Number
                </button>
                <button 
                    class="btn btn-outline-success" 
                    :class="{ active: selectedMetric === 'Vol' }" 
                    @click="selectedMetric = 'Vol'">
                    View by Volume
                </button>
                </div>
            </div>

            <!-- Table -->
            <div class="table-responsive">
                <table class="table table-hover table-striped align-middle text-center">
                <thead class="table-success sticky-top">
                    <tr>
                    <th>Species Group</th>
                    <th>Metric Type</th>
                    <th>5cm-15cm</th>
                    <th>15cm-30cm</th>
                    <th>30cm-45cm</th>
                    <th>45cm-60cm</th>
                    <th>60cm+</th>
                    <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr 
                    v-for="(row, index) in filteredData" 
                    :key="index">
                    <td>{{ row.species_group }}</td>
                    <td>{{ row.metric_type }}</td>
                    <td>{{ formatNumber(row.DClass1) }}</td>
                    <td>{{ formatNumber(row.DClass2) }}</td>
                    <td>{{ formatNumber(row.DClass3) }}</td>
                    <td>{{ formatNumber(row.DClass4) }}</td>
                    <td>{{ formatNumber(row.DClass5) }}</td>
                    <td class="fw-semibold">{{ formatNumber(row.Total) }}</td>
                    </tr>
                </tbody>
                </table>
            </div>
            <p class="mt-4 text-muted text-end">
                Showing {{ filteredData.length }} {{ selectedMetric }} record(s) for regime {{ selectedRegime }}
            </p>
            </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StandTableRemaining',
  data() {
    return {
      regimes: ['45', '50', '55', '60', '65'],
      selectedRegime: '45',
      selectedMetric: 'Vol',
      data: [],
      loading: false,
      error: null
    };
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      this.data = [];

      try {
        const res = await fetch(`http://localhost:5000/api/stand-table-remaining?regime=${this.selectedRegime}`);
        if (!res.ok) throw new Error('Failed to fetch data');
        this.data = await res.json();
      } catch (err) {
        this.error = err.message || 'An error occurred';
      } finally {
        this.loading = false;
      }
    },
    formatNumber(value) {
    const number = parseFloat(value);
    if (isNaN(number)) return '0.00'; // or return '–' if you want a dash
    return number.toFixed(2);
    }
  },
  computed: {
    filteredData() {
        return this.data.filter(row => row.metric_type === this.selectedMetric);
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.form-select {
  max-width: 200px;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ced4da;
}
.table th,
.table td {
  vertical-align: middle;
}
.table th {
  position: sticky;
  top: 0;
  z-index: 1;
}
.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.02);
}
.table-hover tbody tr:hover {
  background-color: rgba(74, 125, 58, 0.05);
}
.text-success {
  color: #2d5a27 !important;
}
</style>
