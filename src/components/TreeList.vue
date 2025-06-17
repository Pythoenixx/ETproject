<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-12">
          <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
            <!-- Header -->
            <div class="card-header text-white text-center py-5" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
              <h1 class="display-5 fw-bold mb-3">
                <i class="bi bi-tree-fill me-3"></i>Forest Tree Inventory
              </h1>
              <p class="lead mb-0">Comprehensive tree data in table view</p>
            </div>

            <div class="card-body p-5">
              <!-- Statistics Cards -->
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="card stat-card h-100">
                    <div class="card-body text-center">
                      <div class="display-6 fw-bold text-success mb-2">{{ totalTrees }}</div>
                      <div class="text-muted small text-uppercase">Total Trees</div>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card stat-card h-100">
                    <div class="card-body text-center">
                      <div class="display-6 fw-bold text-success mb-2">{{ totalSpecies }}</div>
                      <div class="text-muted small text-uppercase">Unique Species</div>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card stat-card h-100">
                    <div class="card-body text-center">
                      <div class="display-6 fw-bold text-success mb-2">{{ totalSpeciesGroups }}</div>
                      <div class="text-muted small text-uppercase">Species Groups</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="card-body p-5">
              <!-- Loading State -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-success" role="status" style="width: 3rem; height: 3rem;">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Loading tree data...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <strong>Error loading data:</strong> {{ error }}
                <button class="btn btn-outline-danger btn-sm ms-3" @click="loadTreeData">
                  <i class="bi bi-arrow-clockwise me-1"></i>Retry
                </button>
              </div>

              <!-- Data loaded successfully -->
              <div v-else-if="trees.length > 0">
                <!-- Filters and Search -->
                <div class="card mb-4">
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-md-6">
                        <label class="form-label fw-bold">Search</label>
                        <div class="input-group">
                          <span class="input-group-text">
                            <i class="bi bi-search"></i>
                          </span>
                          <input 
                            type="text" 
                            class="form-control" 
                            placeholder="Search across all columns..." 
                            v-model="searchQuery"
                          >
                        </div>
                      </div>
                      <div class="col-md-3">
                        <label class="form-label fw-bold">Items per page</label>
                        <select class="form-select" v-model="itemsPerPage">
                          <option value="10">10</option>
                          <option value="25">25</option>
                          <option value="50">50</option>
                          <option value="100">100</option>
                        </select>
                      </div>
                      <div class="col-md-3">
                        <label class="form-label fw-bold">Sort by</label>
                          <select class="form-select" v-model="sortBy" @change="sortTable(sortBy)">
                          <option v-for="header in tableHeaders" :key="header.key" :value="header.key">
                            {{ header.text }}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Table View -->
                <div class="table-responsive">
                  <table class="table table-hover table-striped">
                    <thead class="table-success">
                      <tr>
                        <th v-for="header in tableHeaders" :key="header.key" @click="sortTable(header.key)" 
                            :class="{ 'sort-active': sortBy === header.key }" style="cursor: pointer;">
                          {{ header.text }}
                          <i class="bi ms-2" 
                             :class="sortDirection === 'asc' ? 'bi-arrow-up' : 'bi-arrow-down'"
                             v-if="sortBy === header.key"></i>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="tree in paginatedTrees" :key="tree.id">
                        <td v-for="header in tableHeaders" :key="header.key">
                          {{ formatCell(tree[header.key], header.key) }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- Pagination -->
                <div class="d-flex justify-content-between align-items-center mt-4">
                  <div class="text-muted">
                    Showing {{ firstItem }} to {{ lastItem }} of {{ filteredTrees.length }} entries
                  </div>
                  <nav>
                    <ul class="pagination">
                      <li class="page-item" :class="{ disabled: currentPage === 1 }">
                        <button class="page-link" @click="currentPage = 1" :disabled="currentPage === 1">
                          <i class="bi bi-chevron-double-left"></i>
                        </button>
                      </li>
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
                      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                        <button class="page-link" @click="currentPage = totalPages" :disabled="currentPage === totalPages">
                          <i class="bi bi-chevron-double-right"></i>
                        </button>
                      </li>
                    </ul>
                  </nav>
                </div>
              </div>

              <!-- No data state -->
              <div v-else class="text-center py-5">
                <i class="bi bi-tree display-1 text-muted mb-3"></i>
                <h4 class="text-muted">No tree data available</h4>
                <p class="text-muted">Please check that the CSV file is accessible.</p>
                <button class="btn btn-success" @click="loadTreeData">
                  <i class="bi bi-arrow-clockwise me-2"></i>Reload Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'TreeList',
  setup() {
    // Reactive data
    const trees = ref([])
    const loading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    const sortBy = ref('TreeNum')
    const sortDirection = ref('asc')

    // Table headers updated to match your database columns
    const tableHeaders = ref([
      { key: 'treeNum', text: 'Tree #' },
      { key: 'species', text: 'Species' },
      { key: 'species_group', text: 'Species Group', type: 'number' },
      { key: 'block_x', text: 'Block X', type: 'number' },
      { key: 'block_y', text: 'Block Y', type: 'number' },
      { key: 'coord_x', text: 'X Coord', type: 'number' },
      { key: 'coord_y', text: 'Y Coord', type: 'number' },
      { key: 'diameter_cm', text: 'Diameter (cm)', type: 'number' },
      { key: 'height_m', text: 'Height (m)', type: 'number' },
      { key: 'volume_m3', text: 'Volume (m³)', type: 'number' },
    ])

    // Fetch data from backend API
    const loadTreeData = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await fetch('http://localhost:5000/api/forest-trees')
        
        if (!response.ok) {
          throw new Error('Failed to fetch tree data from server')
        }

        const data = await response.json()
        
        // Transform data to match your frontend structure
        trees.value = data.map(tree => ({
          treeNum: tree.treeNum,
          species: tree.species,
          species_group: parseInt(tree.species_group) || 0,
          block_x: parseInt(tree.block_x) || 0,
          block_y: parseInt(tree.block_y) || 0,
          coord_x: parseInt(tree.coord_x) || 0,
          coord_y: parseInt(tree.coord_y) || 0,
          diameter_cm: parseFloat(tree.diameter_cm) || 0,
          height_m: parseFloat(tree.height_m) || 0,
          volume_m3: parseFloat(tree.volume_m3) || 0,
        }))

      } catch (err) {
        console.error('Error loading tree data:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    // Computed properties
    const totalTrees = computed(() => trees.value.length)
    
    const totalSpecies = computed(() => {
      const uniqueSpecies = new Set(trees.value.map(tree => tree.species))
      return uniqueSpecies.size
    })
    
    const totalSpeciesGroups = computed(() => {
      const uniqueGroups = new Set(trees.value.map(tree => tree.species_group))
      return uniqueGroups.size
    })

    const filteredTrees = computed(() => {
      if (!searchQuery.value) return trees.value
      
      const query = searchQuery.value.toLowerCase()
      return trees.value.filter(tree => {
        return Object.values(tree).some(value => 
          String(value).toLowerCase().includes(query)
        )
      })
    })

    const sortedTrees = computed(() => {
      return [...filteredTrees.value].sort((a, b) => {
        let aValue = a[sortBy.value]
        let bValue = b[sortBy.value]
        
        // Handle numeric sorting
        if (!isNaN(aValue)) aValue = Number(aValue)
        if (!isNaN(bValue)) bValue = Number(bValue)
        
        if (typeof aValue === 'number' && typeof bValue === 'number') {
          return sortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
        }
        
        // String sorting
        aValue = String(aValue).toLowerCase()
        bValue = String(bValue).toLowerCase()
        
        return sortDirection.value === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue)
      })
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredTrees.value.length / itemsPerPage.value)
    })

    const paginatedTrees = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return sortedTrees.value.slice(start, end)
    })

    const firstItem = computed(() => {
      return (currentPage.value - 1) * itemsPerPage.value + 1
    })

    const lastItem = computed(() => {
      return Math.min(currentPage.value * itemsPerPage.value, filteredTrees.value.length)
    })

    const visiblePages = computed(() => {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
      let end = Math.min(totalPages.value, start + maxVisible - 1)
      
      if (end - start < maxVisible - 1) {
        start = Math.max(1, end - maxVisible + 1)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    })

    // Methods
    const sortTable = (column) => {
      if (sortBy.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortBy.value = column
        sortDirection.value = 'asc'
      }
    }

    const formatCell = (value, key) => {
      if (value === undefined || value === null || value === '' || (typeof value === 'number' && isNaN(value))) {
        return '-'
      }

      // Format numeric values
      if (typeof value === 'number' || !isNaN(value)) {
        const numValue = parseFloat(value)
        if (key === 'volume') return numValue.toFixed(3)
        if (key === 'diameter' || key === 'height') return numValue.toFixed(1)
        return numValue
      }

      return value
    }

    // Load data on mount
    onMounted(loadTreeData)

    return {
      totalTrees,
      totalSpecies,
      totalSpeciesGroups,
      trees,
      loading,
      error,
      searchQuery,
      currentPage,
      itemsPerPage,
      sortBy,
      sortDirection,
      tableHeaders,
      filteredTrees,
      paginatedTrees,
      totalPages,
      firstItem: computed(() => (currentPage.value - 1) * itemsPerPage.value + 1),
      lastItem: computed(() => Math.min(currentPage.value * itemsPerPage.value, filteredTrees.value.length)),
      visiblePages: computed(() => {
        const maxVisible = 5
        let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
        let end = Math.min(totalPages.value, start + maxVisible - 1)
        if (end - start < maxVisible - 1) start = Math.max(1, end - maxVisible + 1)
        return Array.from({ length: end - start + 1 }, (_, i) => start + i)
      }),
      loadTreeData,
      sortTable,
      formatCell
    }
  }
}
</script>

<style scoped>
.stat-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.text-success {
  color: #2d5a27 !important;
}
.sort-active {
  background-color: rgba(74, 125, 58, 0.1);
}

.table-hover tbody tr:hover {
  background-color: rgba(74, 125, 58, 0.05);
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.02);
}

.page-link {
  color: #2d5a27;
}

.page-link:hover {
  color: #1e3d19;
  background-color: rgba(107, 160, 92, 0.1);
  border-color: #4a7d3a;
}

.page-item.active .page-link {
  background-color: #8bc34a;
  border-color: #8bc34a;
}

.form-select:focus,
.form-control:focus {
  border-color: #4a7d3a;
  box-shadow: 0 0 0 0.2rem rgba(74, 125, 58, 0.25);
}
</style>