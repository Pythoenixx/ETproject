<template>
  <div class="stand-table">
    <h2>Stand Table Data</h2>
    <div v-for="(category, index) in categories" :key="index" class="category-table">
      <h3>{{ category.name }}</h3>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th rowspan="2">Species Group</th>
              <th rowspan="2">Type</th>
              <th colspan="5">Diameter Classes</th>
              <th rowspan="2">Total</th>
            </tr>
            <tr>
              <th>5-15cm</th>
              <th>15-30cm</th>
              <th>30-45cm</th>
              <th>45-60cm</th>
              <th>60cm+</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(group, groupIndex) in category.tableData" :key="groupIndex">
              <tr>
                <td :rowspan="2" class="species-group">{{ group.species }}</td>
                <td class="type">Num</td>
                <td v-for="(value, index) in group.num" :key="'num'+index">{{ formatNumber(value) }}</td>
                <td>{{ formatNumber(group.numTotal) }}</td>
              </tr>
              <tr>
                <td class="type">Vol</td>
                <td v-for="(value, index) in group.vol" :key="'vol'+index">{{ formatNumber(value) }}</td>
                <td>{{ formatNumber(group.volTotal) }}</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StandTable',
  data() {
    const generalData = [
        {
          species: 'Species Group1',
          num: [1491, 1203, 404, 198, 204],
          numTotal: 3500,
          vol: [86.45, 571.02, 645.77, 765.99, 2171.17],
          volTotal: 4240.4
        },
        {
          species: 'Species Group2',
          num: [2080, 1810, 606, 401, 403],
          numTotal: 5300,
          vol: [122.28, 841.63, 981.66, 1544.32, 4405.53],
          volTotal: 7895.42
        },
        {
          species: 'Species Group3',
          num: [2077, 1813, 607, 400, 403],
          numTotal: 5300,
          vol: [121.62, 847.52, 975.69, 1542.51, 4253.64],
          volTotal: 7740.98
        },
        {
          species: 'Species Group4',
          num: [2976, 2709, 912, 497, 306],
          numTotal: 7400,
          vol: [173.51, 1276.96, 1473.51, 1923.48, 3216.39],
          volTotal: 8063.85
        },
        {
          species: 'Species Group5',
          num: [2967, 2708, 916, 408, 401],
          numTotal: 7400,
          vol: [178.18, 474.24, 994.63, 991.98, 2672.39],
          volTotal: 5311.42
        },
        {
          species: 'Species Group6',
          num: [3865, 3607, 1218, 705, 405],
          numTotal: 9800,
          vol: [232.11, 638.59, 1313.1, 1735.06, 2679.25],
          volTotal: 6598.11
        },
        {
          species: 'Species Group7',
          num: [4362, 4220, 1409, 904, 405],
          numTotal: 11300,
          vol: [261.2, 740.44, 1524.12, 2234.34, 2719.47],
          volTotal: 7479.57
        }
    ];

    const productionData = [
    {
      species: "Species Group 1",
      num: [0, 0, 0, 198, 204],
      numTotal: 3500,
      vol: [0, 0, 0, 708.08, 2056.72],
      volTotal: 2764.8
    },
    {
      species: "Species Group 2",
      num: [0, 0, 0, 401, 403],
      numTotal: 5300,
      vol: [0, 0, 0, 1417.38, 3975.08],
      volTotal: 5392.46
    },
    {
      species: "Species Group 3",
      num: [0, 0, 0, 400, 403],
      numTotal: 5300,
      vol: [0, 0, 0, 0, 0],
      volTotal: 0
    },
    {
      species: "Species Group 4",
      num: [0, 0, 0, 497, 306],
      numTotal: 7400,
      vol: [0, 0, 0, 1702.39, 2628.94],
      volTotal: 4331.33
    },
    {
      species: "Species Group 5",
      num: [0, 0, 0, 408, 401],
      numTotal: 7400,
      vol: [0, 0, 0, 0, 0],
      volTotal: 0
    },
    {
      species: "Species Group 6",
      num: [0, 0, 0, 705, 405],
      numTotal: 9800,
      vol: [0, 0, 0, 0, 0],
      volTotal: 0
    },
    {
      species: "Species Group 7",
      num: [0, 0, 0, 904, 405],
      numTotal: 11300,
      vol: [0, 0, 0, 0, 0],
      volTotal: 0
    }
  ];

  const damageData = [
    {
      species: "Species Group 1",
      num: [0, 0, 0, 6, 14],
      numTotal: 20,
      vol: [0, 0, 0, 23.98, 122.01],
      volTotal: 145.99
    },
    {
      species: "Species Group 2",
      num: [0, 1, 0, 24, 17],
      numTotal: 42,
      vol: [0, 0.22, 0, 93.2, 175.09],
      volTotal: 268.51
    },
    {
      species: "Species Group 3",
      num: [0, 0, 0, 0, 0],
      numTotal: 0,
      vol: [0, 0, 0, 0, 0],
      volTotal: 0
    },
    {
      species: "Species Group 4",
      num: [0, 0, 0, 23, 14],
      numTotal: 37,
      vol: [0, 0, 0, 85.59, 152.1],
      volTotal: 237.69
    },
    {
      species: "Species Group 5",
      num: [1, 1, 0, 0, 0],
      numTotal: 2,
      vol: [0.09, 0.09, 0, 0, 0],
      volTotal: 0.18
    },
    {
      species: "Species Group 6",
      num: [1, 0, 0, 0, 0],
      numTotal: 1,
      vol: [0.09, 0, 0, 0, 0],
      volTotal: 0.09
    },
    {
      species: "Species Group 7",
      num: [0, 0, 0, 0, 1],
      numTotal: 1,
      vol: [0, 0, 0, 0, 6.33],
      volTotal: 6.33
    }
  ];

  const remainingData = [
  {
    species: "Species Group 1",
    num: [1491, 1203, 404, 192, 190],
    numTotal: 3480,
    vol: [86.45, 571.02, 645.77, 742.01, 2049.16],
    volTotal: 4094.41
  },
  {
    species: "Species Group 2",
    num: [2080, 1809, 606, 377, 386],
    numTotal: 5258,
    vol: [122.28, 841.41, 981.66, 1451.12, 4230.44],
    volTotal: 7626.91
  },
  {
    species: "Species Group 3",
    num: [2077, 1813, 607, 400, 403],
    numTotal: 5300,
    vol: [121.62, 847.52, 975.69, 1542.51, 4253.64],
    volTotal: 7740.98
  },
  {
    species: "Species Group 4",
    num: [2976, 2709, 912, 474, 292],
    numTotal: 7363,
    vol: [173.51, 1276.96, 1473.51, 1837.89, 3064.29],
    volTotal: 7826.16
  },
  {
    species: "Species Group 5",
    num: [2966, 2707, 916, 408, 401],
    numTotal: 7398,
    vol: [178.09, 474.15, 994.63, 991.98, 2672.39],
    volTotal: 5311.24
  },
  {
    species: "Species Group 6",
    num: [3864, 3607, 1218, 705, 405],
    numTotal: 9799,
    vol: [232.02, 638.59, 1313.1, 1735.06, 2679.25],
    volTotal: 6598.02
  },
  {
    species: "Species Group 7",
    num: [4362, 4220, 1409, 904, 404],
    numTotal: 11299,
    vol: [261.2, 740.44, 1524.12, 2234.34, 2713.14],
    volTotal: 7473.24
  }
];

const general30YearsData = [
  {
    species: "Species Group 1",
    num: [1491, 1203, 404, 192, 190],
    numTotal: 3480,
    vol: [530.19, 1727.83, 987.74, 814.3, 1804.97],
    volTotal: 5865.03
  },
  {
    species: "Species Group 2",
    num: [2080, 1809, 606, 377, 386],
    numTotal: 5258,
    vol: [757.95, 2541.69, 1483.94, 1576.16, 3749.23],
    volTotal: 10108.97
  },
  {
    species: "Species Group 3",
    num: [2077, 1813, 607, 400, 403],
    numTotal: 5300,
    vol: [742.21, 2569.06, 1471.03, 1636.45, 3706.98],
    volTotal: 10125.73
  },
  {
    species: "Species Group 4",
    num: [2976, 2709, 912, 474, 292],
    numTotal: 7363,
    vol: [1066.8, 3890.98, 2247.08, 1992.9, 2718.46],
    volTotal: 11916.22
  },
  {
    species: "Species Group 5",
    num: [2966, 2707, 916, 408, 401],
    numTotal: 7398,
    vol: [481.52, 2035.68, 1362.03, 1063.4, 2554.38],
    volTotal: 7497.01
  },
  {
    species: "Species Group 6",
    num: [3864, 3607, 1218, 705, 405],
    numTotal: 9799,
    vol: [624.89, 2729.44, 1790.95, 1877.79, 2534.67],
    volTotal: 9557.74
  },
  {
    species: "Species Group 7",
    num: [4362, 4220, 1409, 904, 404],
    numTotal: 11299,
    vol: [705.97, 3179.57, 2079.29, 2389.54, 2589.91],
    volTotal: 10944.28
  }
];

const production30YearsData = [
  {
    species: "Species Group 1",
    num: [1491, 1203, 404, 192, 190],
    numTotal: 3480,
    vol: [530.19, 1727.83, 987.74, 814.3, 1804.97],
    volTotal: 5865.03
  },
  {
    species: "Species Group 2",
    num: [2080, 1809, 606, 377, 386],
    numTotal: 5258,
    vol: [757.95, 2541.69, 1483.94, 1576.16, 3749.23],
    volTotal: 10108.97
  },
  {
    species: "Species Group 3",
    num: [2077, 1813, 607, 400, 403],
    numTotal: 5300,
    vol: [742.21, 2569.06, 1471.03, 1636.45, 3706.98],
    volTotal: 10125.73
  },
  {
    species: "Species Group 4",
    num: [2976, 2709, 912, 474, 292],
    numTotal: 7363,
    vol: [1066.8, 3890.98, 2247.08, 1992.9, 2718.46],
    volTotal: 11916.22
  },
  {
    species: "Species Group 5",
    num: [2966, 2707, 916, 408, 401],
    numTotal: 7398,
    vol: [481.52, 2035.68, 1362.03, 1063.4, 2554.38],
    volTotal: 7497.01
  },
  {
    species: "Species Group 6",
    num: [3864, 3607, 1218, 705, 405],
    numTotal: 9799,
    vol: [624.89, 2729.44, 1790.95, 1877.79, 2534.67],
    volTotal: 9557.74
  },
  {
    species: "Species Group 7",
    num: [4362, 4220, 1409, 904, 404],
    numTotal: 11299,
    vol: [705.97, 3179.57, 2079.29, 2389.54, 2589.91],
    volTotal: 10944.28
  }
];





    return {
      categories: [
        { name: 'General', tableData: JSON.parse(JSON.stringify(generalData)) },
        { name: 'Production', tableData: JSON.parse(JSON.stringify(productionData)) },
        { name: 'Damage', tableData: JSON.parse(JSON.stringify(damageData)) },
        { name: 'Remaining', tableData: JSON.parse(JSON.stringify(remainingData)) },
        { name: 'General 30 Years', tableData: JSON.parse(JSON.stringify(general30YearsData)) },
        { name: 'Production 30 Years', tableData: JSON.parse(JSON.stringify(production30YearsData)) }
      ]
    };
  },
  methods: {
    formatNumber(num) {
      const isVolume = typeof num === 'number' && num % 1 !== 0;
      return num.toLocaleString(undefined, {
        minimumFractionDigits: isVolume ? 2 : 0,
        maximumFractionDigits: isVolume ? 2 : 0
      });
    }
  }
};
</script>

<style scoped>
.stand-table {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

h3 {
  margin-top: 40px;
  margin-bottom: 10px;
  color: #34495e;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
  font-size: 0.9em;
}

th, td {
  padding: 10px 12px;
  text-align: right;
  border: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  text-align: center;
  position: sticky;
  top: 0;
}

td.species-group {
  font-weight: 500;
  text-align: left;
  background-color: #f0f0f0;
}

td.type {
  font-weight: 500;
  text-align: left;
  background-color: #f8f8f8;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}

@media (max-width: 768px) {
  th, td {
    padding: 6px 8px;
    font-size: 0.8em;
  }
}
</style>
