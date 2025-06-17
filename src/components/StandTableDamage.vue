<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #9c2f2f, #c44545);">
              <h1 class="display-5 fw-bold mb-3">
                <i class="bi bi-exclamation-diamond-fill me-3"></i>Stand Table Damage
              </h1>
              <p class="lead mb-0">Diameter Class Damage Distribution by Species Group</p>

              <!-- Regime Selection -->
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

            <!-- Body -->
            <div class="card-body p-5">
              <!-- Loading -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-danger" role="status" style="width: 3rem; height: 3rem;">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Loading damage data for regime {{ selectedRegime }}...</p>
              </div>

              <!-- Error -->
              <div v-else-if="error" class="alert alert-danger text-center">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
              </div>

              <!-- Content -->
              <div v-else>
                <!-- Toggle -->
                <div class="d-flex justify-content-center align-items-center mb-4">
                  <div class="btn-group" role="group">
                    <button 
                      class="btn" 
                      :class="metricType === 'Num' ? 'btn-danger' : 'btn-outline-danger'"
                      @click="metricType = 'Num'"
                    >
                      View by Number
                    </button>
                    <button 
                      class="btn" 
                      :class="metricType === 'Vol' ? 'btn-danger' : 'btn-outline-danger'"
                      @click="metricType = 'Vol'"
                    >
                      View by Volume
                    </button>
                  </div>
                </div>

                <!-- Table -->
                <div class="table-responsive">
                  <table class="table table-hover table-striped align-middle text-center">
                    <thead class="table-danger">
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
                  <p>Total Damage: <strong>{{ formatValue(totalSum) }}</strong></p>
                  <p>Average per Species Group: <strong>{{ formatValue(averagePerGroup) }}</strong></p>
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
      metricType: 'Vol'
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
        const res = await fetch(`http://localhost:5000/api/stand-table-damage?regime=${this.selectedRegime}`);
        const data = await res.json();

        if (res.ok) {
          this.tableData = data;
        } else {
          throw new Error(data.error || 'Failed to fetch damage table');
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
  background-color: rgba(196, 69, 69, 0.05);
}
.text-danger {
  color: #9c2f2f !important;
}
</style>
