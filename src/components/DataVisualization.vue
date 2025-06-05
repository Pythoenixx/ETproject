// src/components/DataVisualization.vue
<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-10">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
              <h1 class="display-5 fw-bold mb-3">
                <i class="bi bi-tree-fill me-3"></i>Forest Data Visualizer
              </h1>
              <p class="lead mb-0">Upload your forest CSV data and explore it with interactive visualizations</p>
            </div>

            <div class="card-body p-5">
              <!-- File Upload Section -->
              <div class="upload-zone p-5 text-center mb-4" @dragover.prevent @drop.prevent="handleDrop">
                <div class="mb-4">
                  <i class="bi bi-cloud-upload display-1 text-muted"></i>
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  class="d-none"
                  accept=".csv"
                  @change="handleFileSelect"
                />
                <button class="btn btn-forest btn-lg px-4 py-3" @click="$refs.fileInput.click()">
                  <i class="bi bi-file-earmark-arrow-up me-2"></i>Choose Forest CSV File
                </button>
                <p class="text-muted mt-3 mb-0">
                  Upload your Forest.csv file to start visualizing your data
                </p>
              </div>

              <!-- Data Preview Section -->
              <div v-if="forestData.length > 0">
                <!-- Statistics Cards -->
                <div class="row g-4 mb-4">
                  <div class="col-md-4">
                    <div class="card stat-card h-100">
                      <div class="card-body text-center">
                        <div class="display-6 fw-bold text-success mb-2">{{ forestData.length }}</div>
                        <div class="text-muted small text-uppercase">Total Records</div>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="card stat-card h-100">
                      <div class="card-body text-center">
                        <div class="display-6 fw-bold text-success mb-2">{{ dataColumns.length }}</div>
                        <div class="text-muted small text-uppercase">Columns</div>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-4">
                    <div class="card stat-card h-100">
                      <div class="card-body text-center">
                        <div class="display-6 fw-bold text-success mb-2">{{ numericColumns.length }}</div>
                        <div class="text-muted small text-uppercase">Numeric Columns</div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Data Table -->
                <div class="card mb-4">
                  <div class="card-header bg-light">
                    <div class="row align-items-center">
                      <div class="col">
                        <h5 class="mb-0">
                          <i class="bi bi-table me-2"></i>Data Preview
                        </h5>
                      </div>
                      <div class="col-auto">
                        <select class="form-select form-select-sm" v-model="rowsPerPage" @change="updatePagination">
                          <option value="10">10 rows</option>
                          <option value="25">25 rows</option>
                          <option value="50">50 rows</option>
                          <option value="100">100 rows</option>
                          <option :value="forestData.length">All rows</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="card-body p-0">
                    <div class="table-responsive">
                      <table class="table table-forest table-hover mb-0">
                        <thead>
                          <tr>
                            <th v-for="column in dataColumns" :key="column" class="fw-bold">
                              {{ column }}
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(row, index) in paginatedData" :key="index">
                            <td v-for="column in dataColumns" :key="column" :title="row[column]">
                              {{ row[column] }}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div class="card-footer bg-light">
                    <div class="row align-items-center">
                      <div class="col">
                        <small class="text-muted">
                          Showing {{ paginatedData.length }} of {{ forestData.length }} rows
                        </small>
                      </div>
                      <div class="col-auto">
                        <nav>
                          <ul class="pagination pagination-sm mb-0">
                            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                              <button class="page-link" @click="currentPage--" :disabled="currentPage === 1">
                                <i class="bi bi-chevron-left"></i>
                              </button>
                            </li>
                            <li
                              v-for="page in visiblePages"
                              :key="page"
                              class="page-item"
                              :class="{ active: page === currentPage }"
                            >
                              <button class="page-link" @click="currentPage = page">
                                {{ page }}
                              </button>
                            </li>
                            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                              <button class="page-link" @click="currentPage++" :disabled="currentPage === totalPages">
                                <i class="bi bi-chevron-right"></i>
                              </button>
                            </li>
                          </ul>
                        </nav>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Chart Controls -->
                <div class="card mb-4">
                  <div class="card-body">
                    <h5 class="card-title">
                      <i class="bi bi-gear-fill me-2"></i>Visualization Controls
                    </h5>
                    <div class="row g-3">
                      <div class="col-md-4">
                        <label class="form-label fw-bold">Chart Type</label>
                        <select class="form-select" v-model="chartType" @change="updateChart">
                          <option value="bar">Bar Chart</option>
                          <option value="line">Line Chart</option>
                          <option value="pie">Pie Chart</option>
                          <option value="scatter">Scatter Plot</option>
                        </select>
                      </div>
                      <div class="col-md-4">
                        <label class="form-label fw-bold">X-Axis</label>
                        <select class="form-select" v-model="xAxisColumn" @change="updateChart">
                          <option v-for="column in dataColumns" :key="column" :value="column">
                            {{ column }}
                          </option>
                        </select>
                      </div>
                      <div class="col-md-4">
                        <label class="form-label fw-bold">Y-Axis</label>
                        <select class="form-select" v-model="yAxisColumn" @change="updateChart">
                          <option v-for="column in numericColumns" :key="column" :value="column">
                            {{ column }}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Chart -->
                <div class="chart-container p-4">
                  <h5 class="text-center mb-4 text-success fw-bold">
                    {{ yAxisColumn }} vs {{ xAxisColumn }}
                  </h5>
                  <div style="position: relative; height: 400px;">
                    <canvas ref="chartCanvas"></canvas>
                  </div>
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
import { ref, computed, nextTick } from 'vue'
import Papa from 'papaparse'
import Chart from 'chart.js/auto'

export default {
  name: 'DataVisualization',
  setup() {
    // Reactive data
    const forestData = ref([])
    const dataColumns = ref([])
    const currentPage = ref(1)
    const rowsPerPage = ref(10)
    const chartType = ref('bar')
    const xAxisColumn = ref('')
    const yAxisColumn = ref('')
    const currentChart = ref(null)
    const chartCanvas = ref(null)

    // Computed properties
    const numericColumns = computed(() => {
      if (forestData.value.length === 0) return []
      
      return dataColumns.value.filter(col => {
        const values = forestData.value.slice(0, 10).map(row => row[col])
        return values.some(val => !isNaN(parseFloat(val)) && isFinite(val))
      })
    })

    const totalPages = computed(() => {
      return Math.ceil(forestData.value.length / rowsPerPage.value)
    })

    const paginatedData = computed(() => {
      const start = (currentPage.value - 1) * rowsPerPage.value
      const end = start + rowsPerPage.value
      return forestData.value.slice(start, end)
    })

    const visiblePages = computed(() => {
      const pages = []
      const maxButtons = 7
      let start = Math.max(1, currentPage.value - Math.floor(maxButtons / 2))
      let end = Math.min(totalPages.value, start + maxButtons - 1)
      
      if (end - start < maxButtons - 1) {
        start = Math.max(1, end - maxButtons + 1)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    })

    // Methods
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) processFile(file)
    }

    const handleDrop = (event) => {
      event.preventDefault()
      const file = event.dataTransfer.files[0]
      if (file && file.type === 'text/csv') {
        processFile(file)
      }
    }

    const processFile = (file) => {
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          // Clean the data
          forestData.value = results.data.map(row => {
            const cleanedRow = {}
            for (let key in row) {
              const cleanKey = key.trim()
              const cleanValue = row[key] ? row[key].trim() : ''
              cleanedRow[cleanKey] = cleanValue
            }
            return cleanedRow
          })

          if (forestData.value.length > 0) {
            dataColumns.value = Object.keys(forestData.value[0])
            setupDefaultColumns()
            updateChart()
          }
        },
        error: (error) => {
          alert('Error parsing CSV: ' + error.message)
        }
      })
    }

    const setupDefaultColumns = () => {
      if (dataColumns.value.length > 0) {
        xAxisColumn.value = dataColumns.value[0]
      }
      if (numericColumns.value.length > 0) {
        yAxisColumn.value = numericColumns.value[0]
      }
    }

    const updatePagination = () => {
      currentPage.value = 1
    }

    const updateChart = async () => {
      if (!xAxisColumn.value || !yAxisColumn.value) return

      await nextTick()

      if (currentChart.value) {
        currentChart.value.destroy()
      }

      const ctx = chartCanvas.value.getContext('2d')
      const chartData = prepareChartData()

      currentChart.value = new Chart(ctx, {
        type: chartType.value === 'scatter' ? 'scatter' : chartType.value,
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: chartType.value === 'pie',
              position: 'top',
            }
          },
          scales: chartType.value !== 'pie' ? {
            x: {
              title: { display: true, text: xAxisColumn.value }
            },
            y: {
              title: { display: true, text: yAxisColumn.value }
            }
          } : {}
        }
      })
    }

    const prepareChartData = () => {
      const colors = [
        '#2d5a27', '#4a7d3a', '#6ba05c', '#8bc34a', '#cddc39',
        '#ffeb3b', '#ffc107', '#ff9800', '#ff5722', '#795548'
      ]

      if (chartType.value === 'pie') {
        const groupedData = {}
        forestData.value.forEach(row => {
          const key = row[xAxisColumn.value] || 'Unknown'
          const value = parseFloat(row[yAxisColumn.value]) || 0
          groupedData[key] = (groupedData[key] || 0) + value
        })

        return {
          labels: Object.keys(groupedData),
          datasets: [{
            data: Object.values(groupedData),
            backgroundColor: colors.slice(0, Object.keys(groupedData).length),
            borderWidth: 2,
            borderColor: '#fff'
          }]
        }
      } else if (chartType.value === 'scatter') {
        const scatterData = forestData.value.map(row => ({
          x: parseFloat(row[xAxisColumn.value]) || 0,
          y: parseFloat(row[yAxisColumn.value]) || 0
        })).filter(point => !isNaN(point.x) && !isNaN(point.y))

        return {
          datasets: [{
            label: `${yAxisColumn.value} vs ${xAxisColumn.value}`,
            data: scatterData,
            backgroundColor: colors[0] + '80',
            borderColor: colors[0],
            borderWidth: 2
          }]
        }
      } else {
        // Bar or line chart
        const groupedData = {}
        forestData.value.forEach(row => {
          const key = row[xAxisColumn.value] || 'Unknown'
          const value = parseFloat(row[yAxisColumn.value]) || 0
          if (!groupedData[key]) {
            groupedData[key] = []
          }
          groupedData[key].push(value)
        })

        const labels = Object.keys(groupedData)
        const data = labels.map(label => {
          const values = groupedData[label]
          return values.reduce((sum, val) => sum + val, 0) / values.length
        })

        return {
          labels: labels,
          datasets: [{
            label: yAxisColumn.value,
            data: data,
            backgroundColor: colors[0] + (chartType.value === 'line' ? '40' : '80'),
            borderColor: colors[0],
            borderWidth: 2,
            fill: chartType.value === 'line' ? false : true
          }]
        }
      }
    }

    return {
      // Reactive data
      forestData,
      dataColumns,
      currentPage,
      rowsPerPage,
      chartType,
      xAxisColumn,
      yAxisColumn,
      chartCanvas,
      
      // Computed properties
      numericColumns,
      totalPages,
      paginatedData,
      visiblePages,
      
      // Methods
      handleFileSelect,
      handleDrop,
      updatePagination,
      updateChart
    }
  },
  
  // Cleanup when component is unmounted
  beforeUnmount() {
    if (this.currentChart) {
      this.currentChart.destroy()
    }
  }
}
</script>

<style scoped>
/* Custom styles for forest theme */
.btn-forest {
  background: linear-gradient(135deg, #2d5a27, #4a7d3a);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.btn-forest:hover {
  background: linear-gradient(135deg, #1e3d19, #2d5a27);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(45, 90, 39, 0.3);
  color: white;
}

.upload-zone {
  border: 3px dashed #6ba05c;
  border-radius: 15px;
  background: rgba(107, 160, 92, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-zone:hover {
  border-color: #4a7d3a;
  background: rgba(107, 160, 92, 0.1);
}

.stat-card {
  border: none;
  border-radius: 15px;
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.table-forest th {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  color: #2d5a27;
  border-bottom: 2px solid #4a7d3a;
  font-weight: 600;
}

.table-forest tbody tr:hover {
  background-color: rgba(107, 160, 92, 0.1);
}

.chart-container {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.page-link {
  color: #2d5a27;
  border-color: #dee2e6;
}

.page-link:hover {
  color: #1e3d19;
  background-color: rgba(107, 160, 92, 0.1);
  border-color: #4a7d3a;
}

.page-item.active .page-link {
  background-color: #8bc34a;
  border-color: #2d5a27;
}

.form-select:focus,
.form-control:focus {
  border-color: #4a7d3a;
  box-shadow: 0 0 0 0.2rem rgba(74, 125, 58, 0.25);
}

/* Responsive table scroll */
.table-responsive {
  border-radius: 10px;
}

/* Custom scrollbar for webkit browsers */
.table-responsive::-webkit-scrollbar {
  height: 8px;
}

.table-responsive::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.table-responsive::-webkit-scrollbar-thumb {
  background: #4a7d3a;
  border-radius: 10px;
}

.table-responsive::-webkit-scrollbar-thumb:hover {
  background: #2d5a27;
}

/* Animation for data loading */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fadeIn 0.6s ease-out;
}

/* Bootstrap Icons fallback */
.bi {
  display: inline-block;
  width: 1em;
  height: 1em;
  vertical-align: -0.125em;
}
</style>