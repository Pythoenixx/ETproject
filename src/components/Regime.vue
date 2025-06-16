<template>
  <div class="min-vh-100 py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
      <div class="card shadow-lg border-0" style="border-radius: 20px; overflow: hidden;">
        <!-- Header -->
        <div class="card-header py-5 text-white text-center" style="background: linear-gradient(135deg, #2d5a27, #4a7d3a);">
          <h1 class="fw-bold mb-1">
            🌲 Forest Regime 
          </h1>
          <p class="mb-0 lead">Analyze & filter forest tree data by regime</p>
        </div>

        <div class="card-body p-4">
          <!-- Regime Selector -->
          <div class="mb-4">
            <label for="tableSelect" class="form-label fw-semibold">Select Regime:</label>
            <select id="tableSelect" class="form-select" v-model="selectedTable" @change="fetchData">
              <option disabled value="">-- Select Table --</option>
              <option value="forest_45">45</option>
              <option value="forest_50">50</option>
              <option value="forest_55">55</option>
              <option value="forest_60">60</option>
              <option value="forest_65">65</option>
            </select>
          </div>

          <!-- Filters -->
          <div class="card mb-4">
            <div class="card-body">
              <div class="row g-3 align-items-end">
                <div class="col-md-3">
                  <label class="form-label fw-semibold">Species</label>
                  <input type="text" class="form-control" placeholder="Search species..." v-model="filters.species">
                </div>
                <div class="col-md-2">
                  <label class="form-label fw-semibold">Min Diameter</label>
                  <input type="number" class="form-control" v-model="filters.minDiameter">
                </div>
                <div class="col-md-2">
                  <label class="form-label fw-semibold">Status</label>
                  <select class="form-select" v-model="filters.status">
                    <option value="">All</option>
                    <option v-for="status in statusOptions" :value="status">{{ status }}</option>
                  </select>
                </div>
                <div class="col-md-3 d-flex gap-2">
                  <button class="btn btn-success w-100" @click="fetchData">Apply</button>
                  <button class="btn btn-outline-secondary w-100" @click="resetFilters">Reset</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Data Display -->
          <div class="card">
            <div class="card-body">
              <!-- Top Controls -->
              <div class="d-flex justify-content-between flex-wrap mb-3 gap-2">
                <div class="d-flex align-items-center">
                  <span class="me-2">Show</span>
                  <select class="form-select form-select-sm w-auto" v-model="itemsPerPage">
                    <option value="10">10</option>
                    <option value="25">25</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                  </select>
                  <span class="ms-2">entries</span>
                </div>
                <div class="d-flex">
                  <input type="text" class="form-control form-control-sm" placeholder="Search..." v-model="searchQuery">
                </div>
              </div>

              <!-- Loading Spinner -->
              <div v-if="loading" class="text-center my-5">
                <div class="spinner-border text-success" role="status"></div>
                <p class="mt-3 text-muted">Loading forest data...</p>
              </div>

              <!-- Table -->
              <div v-else class="table-responsive">
                <table class="table table-striped table-hover table-bordered align-middle">
                  <thead class="table-success text-center">
                    <tr>
                      <th v-for="column in columns" :key="column.key" @click="sortBy(column.key)" :class="{ 'sortable': column.sortable }">
                        {{ column.label }}
                        <span v-if="sortColumn === column.key" class="ms-1">
                          {{ sortDirection === 'asc' ? '↑' : '↓' }}
                        </span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in paginatedData" :key="item.TreeNum">
                      <td>{{ item.BlockX }},{{ item.BlockY }}</td>
                      <td>{{ item.x }},{{ item.y }}</td>
                      <td>{{ item.TreeNum }}</td>
                      <td>
                        <span class="badge bg-secondary">{{ item.species }}</span>
                        <small class="text-muted d-block">{{ item.spgroup }}</small>
                      </td>
                      <td class="text-end">{{ formatNumber(item.diameter) }}</td>
                      <td class="text-end">{{ formatNumber(item.height) }}</td>
                      <td class="text-end">{{ formatNumber(item.volume, 3) }}</td>
                      <td>
                        <span :class="statusBadgeClass(item.status)">{{ item.status }}</span>
                      </td>
                      <td>{{ item.PROD }}</td>
                      <td>
                        <span v-if="item.cut_angle" class="badge bg-warning text-dark">
                          {{ item.cut_angle }}°
                        </span>
                      </td>
                      <td>
                        <span v-if="item.stem_damage">
                          {{ item.stem_damage }}
                        </span>
                      </td>
                      <td>
                        <span v-if="item.crown_damage">
                          {{ item.crown_damage }}
                        </span>
                      </td>
                      <td class="text-end">{{ formatNumber(item.d30) }}</td>
                      <td class="text-end">{{ formatNumber(item.VOL30, 3) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Pagination -->
              <div class="d-flex justify-content-between align-items-center mt-4 flex-wrap gap-2">
                <div>
                  Showing {{ paginationStart }} to {{ paginationEnd }} of {{ filteredData.length }} entries
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="prevPage">Previous</button>
                    </li>

                    <li class="page-item" :class="{ active: currentPage === 1 }">
                    <button class="page-link" @click="goToPage(1)">1</button>
                    </li>

                    <li class="page-item" v-if="visiblePageNumbers[0] > 2">
                    <span class="page-link">...</span>
                    </li>

                    <li
                    class="page-item"
                    v-for="page in visiblePageNumbers"
                    :key="page"
                    :class="{ active: currentPage === page }"
                    >
                    <button class="page-link" @click="goToPage(page)">{{ page }}</button>
                    </li>

                    <li class="page-item" v-if="visiblePageNumbers[visiblePageNumbers.length - 1] < pageCount - 1">
                    <span class="page-link">...</span>
                    </li>

                    <li class="page-item" :class="{ active: currentPage === pageCount }">
                    <button class="page-link" @click="goToPage(pageCount)">{{ pageCount }}</button>
                    </li>

                    <li class="page-item" :class="{ disabled: currentPage === pageCount }">
                    <button class="page-link" @click="nextPage">Next</button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div> <!-- end card-body -->
      </div> <!-- end card -->
    </div> <!-- end container -->
  </div>
</template>

<script>
export default {
  name: 'ForestInventory',
    data() {
    return {
        selectedTable: 'forest_45', // default selected table
        loading: false,
        error: null,
        forestData: [],
        filters: {
        species: '',
        minDiameter: null,
        status: '',
        },
        statusOptions: ['live', 'dead', 'harvested', 'damaged'],
        columns: [
        { key: 'BlockX', label: 'Block', sortable: true },
        { key: 'x', label: 'Coordinates', sortable: false },
        { key: 'TreeNum', label: 'Tree #', sortable: true },
        { key: 'species', label: 'Species/Group', sortable: true },
        { key: 'diameter', label: 'Diameter (cm)', sortable: true },
        { key: 'height', label: 'Height (m)', sortable: true },
        { key: 'volume', label: 'Volume (m³)', sortable: true },
        { key: 'status', label: 'Status', sortable: true },
        { key: 'PROD', label: 'Production', sortable: true },
        { key: 'cut_angle', label: 'Cut Angle', sortable: true },
        { key: 'stem_damage', label: 'Stem Damage', sortable: true },
        { key: 'crown_damage', label: 'Crown Damage', sortable: true },
        { key: 'd30', label: 'd30 (cm)', sortable: true },
        { key: 'VOL30', label: 'VOL30 (m³)', sortable: true }
        ],
        sortColumn: 'TreeNum',
        sortDirection: 'asc',
        searchQuery: '',
        currentPage: 1,
        itemsPerPage: 25
    }
    },

  computed: {
    filteredData() {
      let data = [...this.forestData];

      if (this.filters.species) {
        data = data.filter(item =>
          item.species.toLowerCase().includes(this.filters.species.toLowerCase())
        );
      }

      if (this.filters.minDiameter) {
        data = data.filter(item =>
          item.diameter >= parseFloat(this.filters.minDiameter)
        );
      }

      if (this.filters.status) {
        data = data.filter(item => item.status === this.filters.status);
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        data = data.filter(item =>
          Object.values(item).some(val =>
            String(val).toLowerCase().includes(query)
          )
        );
      }

      if (this.sortColumn) {
        data.sort((a, b) => {
          let valA = a[this.sortColumn];
          let valB = b[this.sortColumn];
          if (!isNaN(valA)) valA = parseFloat(valA);
          if (!isNaN(valB)) valB = parseFloat(valB);
          if (valA < valB) return this.sortDirection === 'asc' ? -1 : 1;
          if (valA > valB) return this.sortDirection === 'asc' ? 1 : -1;
          return 0;
        });
      }

      return data;
    },
    visiblePageNumbers() {
        const total = this.pageCount;
        const current = this.currentPage;
        const delta = 2;
        const range = [];

        let start = Math.max(2, current - delta);
        let end = Math.min(total - 1, current + delta);

        if (current - delta <= 2) start = 2;
        if (current + delta >= total - 1) end = total - 1;

        for (let i = start; i <= end; i++) {
        range.push(i);
        }

        return range;
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },
    pageCount() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage);
    },
    paginationStart() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    paginationEnd() {
      const end = this.currentPage * this.itemsPerPage;
      return end > this.filteredData.length ? this.filteredData.length : end;
    }
  },
  watch: {
    itemsPerPage() {
      this.currentPage = 1;
    },
    searchQuery() {
      this.currentPage = 1;
    }
  },
  async created() {
    await this.fetchData();
  },
  methods: {
  async fetchData() {
    this.loading = true;
    this.error = null;
    try {
      const res = await fetch(`http://localhost:5000/api/forest-data?table=${this.selectedTable}`);
      if (!res.ok) throw new Error('Failed to fetch data');
      this.forestData = await res.json();
    } catch (err) {
      console.error('Error:', err);
      this.error = 'Failed to load forest data. Please try again later.';
    } finally {
      this.loading = false;
    }
  },

    resetFilters() {
      this.filters = {
        species: '',
        minDiameter: null,
        status: '',
      };
      this.searchQuery = '';
      this.currentPage = 1;
    },
    sortBy(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
    },
    statusBadgeClass(status) {
      return {
        badge: true,
        'bg-success': status === 'KEEP',
        'bg-danger': status === 'VICTIM',
        'bg-warning text-dark': status === 'CUT',
      };
    },
    formatNumber(value, decimals = 1) {
      if (value === null || value === undefined) return '-';
      return parseFloat(value).toFixed(decimals);
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    nextPage() {
      if (this.currentPage < this.pageCount) this.currentPage++;
    },
    goToPage(page) {
      this.currentPage = page;
    }
  }
}
</script>

<style scoped>
.table-responsive {
  max-height: 70vh;
  overflow-y: auto;
}
.sortable {
  cursor: pointer;
}
.sortable:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
.badge {
  font-size: 0.75em;
  font-weight: 600;
  padding: 0.35em 0.65em;
}
.table th {
  position: sticky;
  top: 0;
  background-color: #eaf4ec;
  z-index: 10;
}
.table {
  font-size: 0.875rem;
}
.text-end {
  text-align: right;
}
.page-link {
  color: #2d5a27;
}
.page-item.active .page-link {
  background-color: #8bc34a;
  border-color: #8bc34a;
  color: white;
}
.page-link:hover {
  color: #1e3d19;
  background-color: rgba(74, 125, 58, 0.1);
}
.form-select:focus,
.form-control:focus {
  border-color: #4a7d3a;
  box-shadow: 0 0 0 0.2rem rgba(74, 125, 58, 0.25);
}
</style>