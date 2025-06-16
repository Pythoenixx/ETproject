<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
              <h1 class="display-5 fw-bold mb-3">
                <i class="bi bi-table me-3"></i>Stand Table General (30 Years)
              </h1>
              <p class="lead mb-0">Summary of long-term stand structure and volume</p>

              <!-- Regime Selection -->
              <div class="mt-4">
                <label for="regime-select" class="form-label text-white">Select Regime:</label>
                <select 
                  id="regime-select" 
                  class="form-select w-auto mx-auto" 
                  v-model="selectedRegime"
                  @change="fetchData"
                >
                  <option v-for="regime in regimes" :key="regime" :value="regime">
                    {{ regime }}
                  </option>
                </select>
              </div>

              <!-- Toggle -->
              <div class="mt-3">
                <div class="btn-group">
                  <button class="btn btn-light" :class="{ active: metricType === 'Num' }" @click="metricType = 'Num'">Numbers</button>
                  <button class="btn btn-light" :class="{ active: metricType === 'Vol' }" @click="metricType = 'Vol'">Volumes</button>
                </div>
              </div>
            </div>

            <!-- Content -->
            <div class="card-body p-5">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-success" role="status" style="width: 3rem; height: 3rem;"></div>
                <p class="mt-3 text-muted">Loading data for Stand Table General regime {{ selectedRegime }}...</p>
              </div>

              <div v-else-if="error" class="alert alert-danger text-center">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
              </div>

              <div v-else>
                <div class="table-responsive">
                  <table class="table table-hover table-striped align-middle text-center">
                    <thead class="table-success">
                      <tr>
                        <th>Species Group</th>
                        <th>DClass1</th>
                        <th>DClass2</th>
                        <th>DClass3</th>
                        <th>DClass4</th>
                        <th>DClass5</th>
                        <th>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, index) in filteredData" :key="index">
                        <td>{{ row.species_group }}</td>
                        <td>{{ formatValue(row.DClass1) }}</td>
                        <td>{{ formatValue(row.DClass2) }}</td>
                        <td>{{ formatValue(row.DClass3) }}</td>
                        <td>{{ formatValue(row.DClass4) }}</td>
                        <td>{{ formatValue(row.DClass5) }}</td>
                        <td>{{ formatValue(row.Total) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
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
  name: 'StandTableGeneral',
  data() {
    return {
      regimes: ['45', '50', '55', '60', '65'],
      selectedRegime: '45',
      data: [],
      loading: false,
      error: null,
      metricType: 'Num'
    };
  },
  computed: {
    filteredData() {
      return this.data.filter(row => row.metric_type === this.metricType);
    },
    totalSum() {
      return this.filteredData.reduce((sum, row) => sum + parseFloat(row.Total || 0), 0);
    },
    averagePerGroup() {
      return this.filteredData.length > 0
        ? this.totalSum / this.filteredData.length
        : 0;
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch(`http://localhost:5000/api/stand-table-general?regime=${this.selectedRegime}`);
        const json = await response.json();
        this.data = json;
      } catch (err) {
        this.error = 'Failed to load data';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    formatValue(value) {
      if (this.metricType === 'Num') {
        return Math.round(value).toLocaleString();
      }
      return parseFloat(value).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    }
  },
  mounted() {
    this.fetchData();
  }
}
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
