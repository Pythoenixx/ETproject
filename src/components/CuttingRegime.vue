<template>
  <div class="container py-5">
    <!-- Page Title -->
    <h2 class="mb-4 display-5 fw-bold text-dark">🌲 Cutting Regime</h2>

    <!-- Regime Selector -->
    <div class="mb-4 d-flex align-items-center gap-3">
      <label for="regime" class="form-label fw-semibold mb-0">Select Regime:</label>
      <select
        v-model="selectedRegime"
        id="regime"
        class="form-select w-auto"
      >
        <option
          v-for="option in regimeOptions"
          :key="option"
          :value="option"
        >
          {{ option }} Years
        </option>
      </select>
    </div>

    <!-- Tree Count Table -->
    <div class="mb-5">
      <h3 class="h5 fw-semibold text-success mb-3">🌳 Tree Count (Num)</h3>
      <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-success">
            <tr>
              <th scope="col">Species Group</th>
              <th scope="col">5-15cm</th>
              <th scope="col">15-30cm</th>
              <th scope="col">30-45cm</th>
              <th scope="col">45-60cm</th>
              <th scope="col">60cm+</th>
              <th scope="col" class="fw-bold">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in filteredData" :key="row.species">
              <td class="fw-medium text-dark">{{ row.species }}</td>
              <td class="text-center">{{ row.num[0] }}</td>
              <td class="text-center">{{ row.num[1] }}</td>
              <td class="text-center">{{ row.num[2] }}</td>
              <td class="text-center">{{ row.num[3] }}</td>
              <td class="text-center">{{ row.num[4] }}</td>
              <td class="fw-bold text-success text-center">{{ row.numTotal }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Volume Table -->
    <div>
      <h3 class="h5 fw-semibold text-primary mb-3">🪵 Volume (Vol)</h3>
      <div class="table-responsive">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-primary">
            <tr>
              <th scope="col">Species Group</th>
              <th scope="col">5-15cm</th>
              <th scope="col">15-30cm</th>
              <th scope="col">30-45cm</th>
              <th scope="col">45-60cm</th>
              <th scope="col">60cm+</th>
              <th scope="col" class="fw-bold">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in filteredData" :key="row.species + '-vol'">
              <td class="fw-medium text-dark">{{ row.species }}</td>
              <td class="text-center">{{ row.vol[0] }}</td>
              <td class="text-center">{{ row.vol[1] }}</td>
              <td class="text-center">{{ row.vol[2] }}</td>
              <td class="text-center">{{ row.vol[3] }}</td>
              <td class="text-center">{{ row.vol[4] }}</td>
              <td class="fw-bold text-primary text-center">{{ row.volTotal }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Cutting regime data for 30 years (you can expand to 45, 50, 55, 60)
const dataByRegime = {
  30: [
    {
      species: 'Species Group 1',
      num: [1491, 1203, 404, 192, 190],
      numTotal: 3480,
      vol: [530.19, 1727.83, 987.74, 814.3, 1804.97],
      volTotal: 5865.03
    },
    {
      species: 'Species Group 2',
      num: [2080, 1809, 606, 377, 386],
      numTotal: 5258,
      vol: [757.95, 2541.69, 1483.94, 1576.16, 3749.23],
      volTotal: 10108.97
    },
    {
      species: 'Species Group 3',
      num: [2077, 1813, 607, 400, 403],
      numTotal: 5300,
      vol: [742.21, 2569.06, 1471.03, 1636.45, 3706.98],
      volTotal: 10125.73
    },
    {
      species: 'Species Group 4',
      num: [2976, 2709, 912, 474, 292],
      numTotal: 7363,
      vol: [1066.8, 3890.98, 2247.08, 1992.9, 2718.46],
      volTotal: 11916.22
    },
    {
      species: 'Species Group 5',
      num: [2966, 2707, 916, 408, 401],
      numTotal: 7398,
      vol: [481.52, 2035.68, 1362.03, 1063.4, 2554.38],
      volTotal: 7497.01
    },
    {
      species: 'Species Group 6',
      num: [3864, 3607, 1218, 705, 405],
      numTotal: 9799,
      vol: [624.89, 2729.44, 1790.95, 1877.79, 2534.67],
      volTotal: 9557.74
    },
    {
      species: 'Species Group 7',
      num: [4362, 4220, 1409, 904, 404],
      numTotal: 11299,
      vol: [705.97, 3179.57, 2079.29, 2389.54, 2589.91],
      volTotal: 10944.28
    }
  ],
  45: [
    {
      species: "Species Group 1",
      num: [1600, 1300, 420, 210, 200],
      numTotal: 3730,
      vol: [600, 1850, 1020, 860, 2000],
      volTotal: 6330
    },
    {
      species: "Species Group 2",
      num: [2200, 1900, 630, 400, 400],
      numTotal: 5530,
      vol: [850, 2700, 1550, 1650, 3900],
      volTotal: 10650
    },
    {
      species: "Species Group 3",
      num: [2200, 1900, 640, 420, 420],
      numTotal: 5580,
      vol: [830, 2650, 1500, 1600, 3800],
      volTotal: 10380
    },
    {
      species: "Species Group 4",
      num: [3100, 2800, 940, 500, 300],
      numTotal: 7640,
      vol: [1120, 4000, 2300, 2050, 2800],
      volTotal: 12270
    },
    {
      species: "Species Group 5",
      num: [3100, 2800, 940, 430, 420],
      numTotal: 7690,
      vol: [500, 2100, 1400, 1100, 2650],
      volTotal: 7750
    },
    {
      species: "Species Group 6",
      num: [4000, 3700, 1250, 750, 420],
      numTotal: 10120,
      vol: [700, 2850, 1850, 1950, 2600],
      volTotal: 9950
    },
    {
      species: "Species Group 7",
      num: [4500, 4300, 1450, 950, 420],
      numTotal: 11620,
      vol: [780, 3350, 2150, 2450, 2650],
      volTotal: 11380
    }
  ],

  50: [
    {
      species: "Species Group 1",
      num: [1650, 1350, 430, 220, 210],
      numTotal: 3860,
      vol: [630, 1900, 1050, 900, 2050],
      volTotal: 6530
    },
    {
      species: "Species Group 2",
      num: [2300, 2000, 650, 420, 410],
      numTotal: 5780,
      vol: [900, 2800, 1600, 1700, 3950],
      volTotal: 10950
    },
    {
      species: "Species Group 3",
      num: [2300, 2000, 660, 430, 430],
      numTotal: 5820,
      vol: [870, 2750, 1550, 1650, 3850],
      volTotal: 10670
    },
    {
      species: "Species Group 4",
      num: [3200, 2900, 960, 510, 310],
      numTotal: 7880,
      vol: [1160, 4100, 2350, 2100, 2850],
      volTotal: 12560
    },
    {
      species: "Species Group 5",
      num: [3200, 2900, 960, 440, 430],
      numTotal: 7930,
      vol: [520, 2150, 1450, 1150, 2700],
      volTotal: 7970
    },
    {
      species: "Species Group 6",
      num: [4100, 3800, 1280, 760, 430],
      numTotal: 10370,
      vol: [730, 2950, 1900, 2000, 2650],
      volTotal: 10230
    },
    {
      species: "Species Group 7",
      num: [4600, 4400, 1480, 960, 430],
      numTotal: 11870,
      vol: [820, 3450, 2200, 2500, 2700],
      volTotal: 11670
    }
  ],

  55: [
    {
      species: "Species Group 1",
      num: [1700, 1400, 440, 230, 220],
      numTotal: 3990,
      vol: [660, 1950, 1080, 940, 2100],
      volTotal: 6730
    },
    {
      species: "Species Group 2",
      num: [2400, 2100, 670, 430, 420],
      numTotal: 6020,
      vol: [950, 2900, 1650, 1750, 4000],
      volTotal: 11250
    },
    {
      species: "Species Group 3",
      num: [2400, 2100, 680, 440, 440],
      numTotal: 6060,
      vol: [900, 2850, 1600, 1700, 3900],
      volTotal: 10950
    },
    {
      species: "Species Group 4",
      num: [3300, 3000, 980, 520, 320],
      numTotal: 8120,
      vol: [1200, 4200, 2400, 2150, 2900],
      volTotal: 12850
    },
    {
      species: "Species Group 5",
      num: [3300, 3000, 980, 450, 440],
      numTotal: 8170,
      vol: [540, 2200, 1500, 1200, 2750],
      volTotal: 8190
    },
    {
      species: "Species Group 6",
      num: [4200, 3900, 1310, 770, 440],
      numTotal: 10620,
      vol: [760, 3050, 1950, 2050, 2700],
      volTotal: 10510
    },
    {
      species: "Species Group 7",
      num: [4700, 4500, 1510, 970, 440],
      numTotal: 12120,
      vol: [860, 3550, 2250, 2550, 2750],
      volTotal: 11960
    }
  ],

  60: [
    {
      species: "Species Group 1",
      num: [1750, 1450, 450, 240, 230],
      numTotal: 4120,
      vol: [690, 2000, 1110, 980, 2150],
      volTotal: 6930
    },
    {
      species: "Species Group 2",
      num: [2500, 2200, 690, 440, 430],
      numTotal: 6260,
      vol: [1000, 3000, 1700, 1800, 4050],
      volTotal: 11550
    },
    {
      species: "Species Group 3",
      num: [2500, 2200, 700, 450, 450],
      numTotal: 6300,
      vol: [930, 2950, 1650, 1750, 3950],
      volTotal: 11230
    },
    {
      species: "Species Group 4",
      num: [3400, 3100, 1000, 530, 330],
      numTotal: 8360,
      vol: [1240, 4300, 2450, 2200, 2950],
      volTotal: 13140
    },
    {
      species: "Species Group 5",
      num: [3400, 3100, 1000, 460, 450],
      numTotal: 8410,
      vol: [560, 2250, 1550, 1250, 2800],
      volTotal: 8410
    },
    {
      species: "Species Group 6",
      num: [4300, 4000, 1340, 780, 450],
      numTotal: 10870,
      vol: [790, 3150, 2000, 2100, 2750],
      volTotal: 10790
    },
    {
      species: "Species Group 7",
      num: [4800, 4600, 1540, 980, 450],
      numTotal: 12370,
      vol: [900, 3650, 2300, 2600, 2800],
      volTotal: 12250
    }
  ]}

const regimeOptions = Object.keys(dataByRegime).map(Number)
const selectedRegime = ref(regimeOptions[0])
const filteredData = computed(() => dataByRegime[selectedRegime.value] || [])
</script>
