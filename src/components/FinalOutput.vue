<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
              <h1 class="display-5 fw-bold mb-3">
                <i class="bi bi-bar-chart-fill me-3"></i>Final Output Summary
              </h1>
              <p class="lead mb-0">Compiled production data and volume metrics</p>
              
              <!-- Regime Selection -->
              <div class="mt-4">
                <label for="regime-select" class="form-label text-white">Select Regime:</label>
                <select 
                  id="regime-select" 
                  class="form-select w-auto mx-auto" 
                  v-model="selectedRegime"
                  @change="fetchFinalOutput"
                >
                  <option v-for="regime in regimes" :value="regime" :key="regime">
                  {{ regime }}
                  </option>
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
                <p class="mt-3 text-muted">Fetching final output data for regime {{ selectedRegime }}...</p>
              </div>

              <!-- Error (optional) -->
              <div v-else-if="error" class="alert alert-danger text-center">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
              </div>

              <!-- Data Table -->
              <div v-else>
                <div class="table-responsive">
                  <table class="table table-hover table-striped align-middle text-center">
                    <thead class="table-success">
                      <tr>
                        <th>Species Group</th>
                        <th>Total Volume (m³)</th>
                        <th>Production (m³)</th>
                        <th>Damage (m³)</th>
                        <th>Remainder (m³)</th>
                        <th>Volume 30cm (m³)</th>
                        <th>Prod 30cm (m³)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, index) in data" :key="index">
                        <td>{{ row.Species_Group || 'N/A' }}</td>
                        <td>{{ formatNumber(row.Total_Volume) }}</td>
                        <td>{{ formatNumber(row.Production) }}</td>
                        <td class="text-danger">{{ formatNumber(row.Damage) }}</td>
                        <td>{{ formatNumber(row.Remainder) }}</td>
                        <td>{{ formatNumber(row.Volume30) }}</td>
                        <td>{{ formatNumber(row.Prod30) }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <p class="mt-4 text-muted text-end">Showing {{ data.length }} record(s) for regime {{ selectedRegime }}</p>
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
  name: 'FinalOutput',
  data() {
    return {
      data: [],
      loading: true,
      error: null,
      selectedRegime: 45, // Default selection
      regimes: [45, 50, 55, 60, 65] // Available regimes
    };
  },
  methods: {
    async fetchFinalOutput() {
      this.loading = true;
      this.error = null;
      try {
        const res = await fetch(`http://localhost:5000/api/final_output/${this.selectedRegime}`);
        if (!res.ok) throw new Error(`Failed to fetch final output data for regime ${this.selectedRegime}.`);
        this.data = await res.json();
      } catch (err) {
        console.error('Error:', err);
        this.error = `Unable to load data for regime ${this.selectedRegime}. Please try again later.`;
      } finally {
        this.loading = false;
      }
    },
    formatNumber(value) {
      return parseFloat(value).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    },
  },
  mounted() {
    this.fetchFinalOutput();
  },
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
