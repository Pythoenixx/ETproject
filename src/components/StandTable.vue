<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
              <h1 class="display-5 fw-bold mb-3">
                <i class="bi bi-tree-fill me-3"></i>Stand Table General
              </h1>
              <p class="lead mb-0">Diameter Class Distribution by Species Group</p>

              <!-- Regime Selector -->
              <div class="mt-4">
                <label for="regime-select" class="form-label text-white">Select Regime:</label>
                <select 
                  id="regime-select" 
                  class="form-select w-auto mx-auto" 
                  v-model="selectedRegime"
                  @change="fetchData"
                >
                  <option v-for="regime in regimes" :value="regime" :key="regime">{{ regime }}</option>
                </select>
              </div>
            </div>

            <!-- Content -->
            <div class="card-body p-5">
              <!-- Loading -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-success" role="status" style="width: 3rem; height: 3rem;">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Loading data for Stand Table {{ selectedRegime }}...</p>
              </div>

              <!-- Error -->
              <div v-else-if="error" class="alert alert-danger text-center">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
              </div>

              

              <!-- Data Table -->
              <div v-else>
                <!-- Toggle between Num and Vol -->
                <div class="d-flex justify-content-center align-items-center mb-4">
                  <div class="btn-group" role="group" aria-label="Metric Type Toggle">
                    <button 
                      class="btn" 
                      :class="metricType === 'Num' ? 'btn-success' : 'btn-outline-success'"
                      @click="metricType = 'Num'"
                    >
                      Number (Num)
                    </button>
                    <button 
                      class="btn" 
                      :class="metricType === 'Vol' ? 'btn-success' : 'btn-outline-success'"
                      @click="metricType = 'Vol'"
                    >
                      Volume (Vol)
                    </button>
                  </div>
                </div>

                <div class="table-responsive">
                  <table class="table table-hover table-striped align-middle text-center">
                    <thead class="table-success">
                      <tr>
                        <th>Species Group</th>
                        <th>Metric</th>
                        <th>5cm-15cm</th>
                        <th>15cm-30cm</th>
                        <th>30cm-45cm</th>
                        <th>45cm-60cm</th>
                        <th>60cm+</th>
                        <th>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, index) in filteredData" :key="index">
                        <td>{{ row.species_group }}</td>
                        <td>{{ row.metric_type }}</td>
                        <td>{{ formatValue(row.DClass1) }}</td>
                        <td>{{ formatValue(row.DClass2) }}</td>
                        <td>{{ formatValue(row.DClass3) }}</td>
                        <td>{{ formatValue(row.DClass4) }}</td>
                        <td>{{ formatValue(row.DClass5) }}</td>
                        <td class="fw-bold">{{ formatValue(row.Total) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- Summary -->
                <div class="mt-4 text-end text-muted">
                  <p>Total {{ metricType === 'Num' ? 'Trees' : 'Volume' }}: {{ formatValue(totalSum) }}</p>
                  <p>Average per Species Group: {{ formatValue(averagePerGroup) }}</p>
                </div>
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
  data() {
    return {
      selectedRegime: '45',
      regimes: ['45', '50', '55', '60', '65'],
      tableData: [],
      loading: false,
      error: null,
      metricType: 'Num'
    };
  },
  computed: {
    filteredData() {
      return this.tableData.filter(row => row.metric_type === this.metricType);
    },
    totalSum() {
      return this.filteredData.reduce((sum, row) => {
        const val = parseFloat(row.Total);
        return sum + (isNaN(val) ? 0 : val);
      }, 0);
    },
    averagePerGroup() {
      return this.filteredData.length ? this.totalSum / this.filteredData.length : 0;
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;

      try {
        const res = await fetch(`http://localhost:5000/api/stand-table?regime=${this.selectedRegime}`);
        const data = await res.json();

        if (res.ok) {
          this.tableData = data;
        } else {
          throw new Error(data.error || 'Failed to fetch data');
        }
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    formatValue(value) {
      const number = parseFloat(value);
      if (isNaN(number)) return '0';
      return number.toLocaleString(undefined, {
        minimumFractionDigits: this.metricType === 'Num' ? 0 : 2,
        maximumFractionDigits: 2
      });
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
