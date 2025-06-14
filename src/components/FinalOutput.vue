<template>
  <div class="final-output mb-5">
    <h2>Final Output Data</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Species Group</th>
            <th>Total Volume</th>
            <th>Production</th>
            <th>Damage</th>
            <th>Remainder</th>
            <th>Volume30</th>
            <th>Prod30</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in tableData" :key="index">
            <td>{{ row.species }}</td>
            <td>{{ formatNumber(row.totalVolume) }}</td>
            <td>{{ formatNumber(row.production) }}</td>
            <td>{{ formatNumber(row.damage) }}</td>
            <td>{{ formatNumber(row.remainder) }}</td>
            <td>{{ formatNumber(row.volume30) }}</td>
            <td>{{ formatNumber(row.prod30) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FinalOutput',
  data() {
    return {
      tableData: [
        { species: 'Species Group 1', totalVolume: 7479.57, production: 0, damage: 6.33, remainder: 0, volume30: 10944.28, prod30: 8004.56 },
        { species: 'Species Group 2', totalVolume: 4240.4, production: 2764.8, damage: 145.99, remainder: 2618.81, volume30: 5865.03, prod30: 4088.45 },
        { species: 'Species Group 3', totalVolume: 7895.42, production: 5392.46, damage: 268.51, remainder: 5124.17, volume30: 10108.97, prod30: 7415.6 },
        { species: 'Species Group 4', totalVolume: 7740.98, production: 0, damage: 0, remainder: 0, volume30: 10125.73, prod30: 7477.09 },
        { species: 'Species Group 5', totalVolume: 8063.85, production: 4331.33, damage: 237.69, remainder: 4093.64, volume30: 11916.22, prod30: 7971.99 },
        { species: 'Species Group 6', totalVolume: 5311.42, production: 0, damage: 0.18, remainder: 0, volume30: 7497.01, prod30: 5533.66 },
        { species: 'Species Group 7', totalVolume: 6598.11, production: 0, damage: 0.09, remainder: 0, volume30: 9557.74, prod30: 7017.19 }
      ]
    };
  },
  methods: {
    formatNumber(num) {
      // Format number with 2 decimal places and commas
      return num.toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    }
  }
};
</script>

<style scoped>
.final-output {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  text-align: center;
  position: sticky;
  top: 0;
}

td:first-child, th:first-child {
  text-align: left;
  font-weight: 500;
}

tr:hover {
  background-color: #f5f5f5;
}

@media (max-width: 768px) {
  th, td {
    padding: 8px 10px;
    font-size: 14px;
  }
}
</style>