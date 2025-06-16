<template>
<div v-if="loading" class="loading-indicator">
  Loading tree data...
</div>
<div v-if="error" class="error-message">
  {{ error }}
</div>

<div class="tree-plot-container">
  
  <div class="controls-panel">
    <div class="control-group">
      <label for="tableSelect" class="form-label fw-semibold">Select Regime:</label>
      <select id="tableSelect" class="form-select" v-model="selectedTable" @change="fetchTreeData">
            <option disabled value="">-- Select Table --</option>
            <option value="forest_45">Forest 45</option>
            <option value="forest_50">Forest 50</option>
            <option value="forest_55">Forest 55</option>
            <option value="forest_60">Forest 60</option>
            <option value="forest_65">Forest 65</option>
          </select>
      <label for="blockSelect">Block Selection:</label>
    <select id="blockSelect" v-model="selectedBlock" @change="filterData">
      <option v-for="block in availableBlocks" :key="block.value" :value="block.value">
        {{ block.label }}
      </option>
    </select>


      
  <!-- Tooltip -->
  <div v-if="tooltip.visible" class="tooltip" :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }">
    <div><strong>Tree #:</strong> {{ tooltip.tree?.TreeNum || 'N/A' }}</div>
    <div><strong>Position:</strong> ({{ tooltip.tree?.x }}, {{ tooltip.tree?.y }})</div>
    <div><strong>Species:</strong> {{ tooltip.tree?.species || 'Unknown' }}</div>
    <div><strong>Group:</strong> {{ tooltip.tree?.spgroup }}</div>
    <div><strong>DBH:</strong> {{ tooltip.tree?.Diameter }} cm</div>
    <div><strong>Status:</strong> {{ tooltip.tree?.status }}</div>
    <div v-if="tooltip.tree?.status.toUpperCase() === 'CUT'">
      <strong>Cut Angle:</strong> {{ tooltip.tree?.CutAngle }}°
    </div>
    <div v-if="tooltip.tree?.StemHeight">
      <strong>Height:</strong> {{ tooltip.tree?.StemHeight }} m
    </div>
    <div v-if="tooltip.tree?.Damage">
      <strong>Damage:</strong> {{ tooltip.tree?.Damage }}
    </div>
  </div>
</div>
    
    <div class="control-group">
      <label>
        <input type="checkbox" v-model="showCutLines" @change="redrawPlot">
        Show Cut Direction Lines
      </label>
    </div>
    
    <div class="control-group">
      <label>
        <input type="checkbox" v-model="showCrownAOE" @change="redrawPlot">
        Show Crown Area of Effect
      </label>
    </div>
    
    <div class="control-group">
      <label>
        <input type="checkbox" v-model="showGrid" @change="redrawPlot">
        Show Grid
      </label>
    </div>
    
    <div class="control-group">
      <label for="pointSize">Point Size:</label>
      <input 
        type="range" 
        id="pointSize" 
        v-model="pointSize" 
        min="1" 
        max="8" 
        @input="redrawPlot"
      >
      <span>{{ pointSize }}px</span>
    </div>
  </div>
  
  <!-- Debug Info -->
  <div class="debug-info" v-if="true">
    <small>
      Raw data count: {{ rawTreeData.length }} | 
      Available blocks: {{ availableBlocks.length }} | 
      Selected block: {{ selectedBlock }} | 
      Filtered trees: {{ filteredTrees.length }} |
      Block coords: {{ selectedBlock.split('-') }} |
      Coord ranges: X({{ coordinateRanges.xMin.toFixed(1) }} - {{ coordinateRanges.xMax.toFixed(1) }}), 
      Y({{ coordinateRanges.yMin.toFixed(1) }} - {{ coordinateRanges.yMax.toFixed(1) }})
    </small>
  </div>
  
  <div class="plot-container">
    <svg 
      ref="plotSvg" 
      :width="plotWidth" 
      :height="plotHeight"
      @mousemove="handleMouseMove"
      @mouseleave="hideTooltip"
      :viewBox="`0 0 ${plotWidth} ${plotHeight}`"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- Grid lines -->
      <g v-if="showGrid" class="grid">
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </g>
      
      <!-- Axes -->
      <g class="axes">
        <line :x1="margin" :y1="plotHeight - margin" :x2="plotWidth - margin" :y2="plotHeight - margin" 
              stroke="black" stroke-width="2"/>
        <line :x1="margin" :y1="margin" :x2="margin" :y2="plotHeight - margin" 
              stroke="black" stroke-width="2"/>
      </g>
      
      <!-- Crown AOE circles (drawn first so they appear behind trees) -->
      <g v-if="showCrownAOE" class="crown-aoe">
        <circle 
          v-for="(tree, index) in filteredTrees.filter(t => t.status.toUpperCase() === 'CUT')"
          :key="`crown-${index}`"
          :cx="scaleX(tree.crownCenter.x)"
          :cy="scaleY(tree.crownCenter.y)"
          :r="scaleDistance(6)"
          fill="rgba(0, 200, 0, 0.15)"
          stroke="rgba(0, 150, 0, 0.4)"
          stroke-width="1"
        />
      </g>
      
      <!-- Cut direction lines -->
      <g v-if="showCutLines" class="cut-lines">
        <g v-for="(tree, index) in filteredTrees.filter(t => t.status.toUpperCase() === 'CUT')" :key="`cut-${index}`">
          <line 
            :x1="scaleX(tree.x)" 
            :y1="scaleY(tree.y)" 
            :x2="scaleX(tree.cutLine1.x)" 
            :y2="scaleY(tree.cutLine1.y)"
            stroke="rgba(0, 0, 0, 0.8)" 
            stroke-width="1.5"
          />
          <line 
            :x1="scaleX(tree.x)" 
            :y1="scaleY(tree.y)" 
            :x2="scaleX(tree.cutLine2.x)" 
            :y2="scaleY(tree.cutLine2.y)"
            stroke="rgba(0, 0, 0, 0.8)" 
            stroke-width="1.5"
          />
        </g>
      </g>
      
      <!-- Trees -->
      <g class="trees">
        <circle 
          v-for="(tree, index) in filteredTrees"
          :key="`tree-${tree.TreeNum || index}`"
          :cx="scaleX(tree.x)"
          :cy="scaleY(tree.y)"
          :r="pointSize"
          :fill="getTreeColor(tree)"
          :stroke="getTreeStroke(tree)"
          :stroke-width="getTreeStrokeWidth(tree)"
          class="tree-point"
          @mouseenter="showTooltip($event, tree)"
        />
      </g>
      
      <!-- Axis labels -->
      <text :x="plotWidth / 2" :y="plotHeight - 20" text-anchor="middle" class="axis-label">
        X Position
      </text>
      <text :x="-150" :y="plotHeight / 2" text-anchor="middle" transform="rotate(-90, -90, 220)" class="axis-label">
        Y Position
      </text>
    </svg>
    
    <!-- Legend -->
    <div class="sidebar">
      <div class="legend">
        <h4>Species Groups</h4>
        <div class="legend-items">
          <div v-for="(color, group) in spgroupColors" :key="group" class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: color }"></div>
            <span>Group {{ group }}</span>
          </div>
        </div>
        
        <h4 style="margin-top: 15px;">Status Legend</h4>
        <div class="legend-items">
          <div class="legend-item">
            <div class="legend-color" style="background-color: #228B22; border: 1.5px solid #CC0000;"></div>
            <span>Cut Trees</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background-color: #228B22; border: 1px solid #FF6600;"></div>
            <span>Victim Trees</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background-color: #228B22; border: 0.5px solid rgba(0,0,0,0.3);"></div>
            <span>Keep Trees</span>
          </div>
        </div>
      </div>
      
      <!-- Statistics Panel -->
      <div class="stats-panel">
        <h4>Statistics</h4>
        <div>Total Trees: {{ filteredTrees.length }}</div>
        <div>Cut Trees: {{ filteredTrees.filter(t => t.status.toUpperCase() === 'CUT').length }}</div>
        <div>Keep Trees: {{ filteredTrees.filter(t => t.status.toUpperCase() === 'KEEP').length }}</div>
        <div>Victim Trees: {{ filteredTrees.filter(t => t.status.toUpperCase() === 'VICTIM').length }}</div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'TreeMap',
  data() {
    return {
      selectedTable: 'forest_45',
      rawTreeData: [],
      loading: false,
      error: null,
      selectedBlock: '', // Changed: Start empty to trigger proper initialization
      showCutLines: true,
      showCrownAOE: true,
      showGrid: true,
      pointSize: 3,
      plotWidth: 800,
      plotHeight: 700,
      margin: 60,
      tooltip: {
        visible: false,
        x: 0,
        y: 0,
        tree: null
      },
      spgroupColors: {
        "1": "#228B22",
        "2": "#8B4513",
        "3": "#4169E1",
        "4": "#87CEEB",
        "5": "#FF8C00",
        "6": "#FFD700",
        "7": "#696969"
      }
    }
  },
  computed: {
    availableBlocks() {
      if (!this.rawTreeData || this.rawTreeData.length === 0) {
        return [];
      }

      const blockMap = {};

      this.rawTreeData.forEach(tree => {
        // Handle different possible field names and convert to numbers
        const blockX = parseInt(tree.BlockX || tree.blockX || tree.block_x || 0);
        const blockY = parseInt(tree.BlockY || tree.blockY || tree.block_y || 0);
        
        const key = `${blockX}-${blockY}`;
        blockMap[key] = (blockMap[key] || 0) + 1;
      });

      const blocks = Object.entries(blockMap)
        .sort(([aX, aCount], [bX, bCount]) => {
          const [a1, a2] = aX.split('-').map(Number);
          const [b1, b2] = bX.split('-').map(Number);
          return a1 - b1 || a2 - b2;
        })
        .map(([block, count]) => ({
          label: `Block ${block} (${count} trees)`,
          value: block
        }));

      console.log('Available blocks:', blocks);
      return blocks;
    },
    
    filteredTrees() {
      if (!this.selectedBlock || !this.rawTreeData || this.rawTreeData.length === 0) {
        console.log('No block selected or no data:', { selectedBlock: this.selectedBlock, dataLength: this.rawTreeData.length });
        return [];
      }

      const [blockX, blockY] = this.selectedBlock.split('-').map(Number);
      console.log('Filtering for block:', blockX, blockY);
      
      const filtered = this.rawTreeData
        .filter(tree => {
          // Handle different possible field names
          const treeBlockX = parseInt(tree.BlockX || tree.blockX || tree.block_x || 0);
          const treeBlockY = parseInt(tree.BlockY || tree.blockY || tree.block_y || 0);
          
          const matches = treeBlockX === blockX && treeBlockY === blockY;
          return matches;
        })
        .map(tree => this.processTreeData(tree));
      
      console.log(`Filtered ${filtered.length} trees for block ${this.selectedBlock}`);
      
      // Log coordinate ranges for debugging
      if (filtered.length > 0) {
        const xCoords = filtered.map(t => t.x);
        const yCoords = filtered.map(t => t.y);
        console.log('X range:', Math.min(...xCoords), 'to', Math.max(...xCoords));
        console.log('Y range:', Math.min(...yCoords), 'to', Math.max(...yCoords));
      }
      
      return filtered;
    },
    
    // Calculate coordinate ranges for proper scaling
    coordinateRanges() {
      if (!this.filteredTrees || this.filteredTrees.length === 0) {
        return { xMin: 0, xMax: 100, yMin: 0, yMax: 100 };
      }
      
      const xCoords = this.filteredTrees.map(t => t.x);
      const yCoords = this.filteredTrees.map(t => t.y);
      
      const xMin = Math.min(...xCoords);
      const xMax = Math.max(...xCoords);
      const yMin = Math.min(...yCoords);
      const yMax = Math.max(...yCoords);
      
      // Add 10% padding
      const xPadding = (xMax - xMin) * 0.1;
      const yPadding = (yMax - yMin) * 0.1;
      
      return {
        xMin: xMin - xPadding,
        xMax: xMax + xPadding,
        yMin: yMin - yPadding,
        yMax: yMax + yPadding
      };
    }
  },
  
  watch: {
    // Watch for changes in available blocks and auto-select first one
    availableBlocks: {
      handler(newBlocks) {
        if (newBlocks.length > 0 && !this.selectedBlock) {
          this.selectedBlock = newBlocks[0].value;
          console.log('Auto-selected first block:', this.selectedBlock);
        }
      },
      immediate: true
    }
  },
  
  async created() {
    await this.fetchTreeData();
  },
  
  methods: {
    async fetchTreeData() {
      this.loading = true;
      this.error = null;
      try {
        console.log(`Fetching data for table: ${this.selectedTable}`);
        const res = await fetch(`http://localhost:5000/api/forest-data?table=${this.selectedTable}`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        
        const data = await res.json();
        console.log('Raw data received:', data.length, 'records');
        
        // Log first few records to check structure
        if (data.length > 0) {
          console.log('Sample record:', data[0]);
          console.log('Available fields:', Object.keys(data[0]));
        }
        
        this.rawTreeData = data;
        
        // Reset block selection when new data is loaded
        this.selectedBlock = '';
        
      } catch (err) {
        console.error("Failed to load tree data:", err);
        this.error = "Failed to load tree data.";
        this.rawTreeData = [];
      } finally {
        this.loading = false;
      }
    },

    processTreeData(tree) {
      // Handle different possible field names
      const processed = {
        ...tree,
        BlockX: parseInt(tree.BlockX || tree.blockX || tree.block_x || 0),
        BlockY: parseInt(tree.BlockY || tree.blockY || tree.block_y || 0),
        TreeNum: tree.TreeNum || tree.treeNum || tree.tree_num || tree.id || 'N/A',
        x: parseFloat(tree.x || tree.X || 0),
        y: parseFloat(tree.y || tree.Y || 0),
        spgroup: (tree.spgroup || tree.spGroup || tree.sp_group || '1').toString(),
        status: (tree.status || tree.Status || '-').toString().trim().toUpperCase(),
        cutAngle: parseFloat(tree.CutAngle || tree.cutAngle || tree.cut_angle || tree['Damage CutAngle'] || 0),
        stemHeight: parseFloat(tree.StemHeight || tree.stemHeight || tree.stem_height || tree['Stem Height'] || 15),
        Diameter: parseFloat(tree.Diameter || tree.diameter || tree.DBH || tree.dbh || 0),
        species: tree.species || tree.Species || 'Unknown'
      };

      processed.crownDiameter = tree.crownDiameter || tree.crown_diameter || (processed.Diameter ? processed.Diameter * 12 : 6);

      if (processed.status === 'CUT') {
        const angleRad = (90 - processed.cutAngle) * Math.PI / 180;
        const fallDistance = processed.stemHeight;

        processed.cutLine1 = {
          x: processed.x + fallDistance * Math.cos(angleRad + 0.1),
          y: processed.y + fallDistance * Math.sin(angleRad + 0.1)
        };
        processed.cutLine2 = {
          x: processed.x + fallDistance * Math.cos(angleRad - 0.1),
          y: processed.y + fallDistance * Math.sin(angleRad - 0.1)
        };
        processed.crownCenter = {
          x: processed.x + fallDistance * Math.cos(angleRad),
          y: processed.y + fallDistance * Math.sin(angleRad)
        };
        processed.crownRadius = processed.crownDiameter / 2;
      } else {
        // Provide default values for non-cut trees
        processed.crownCenter = { x: processed.x, y: processed.y };
        processed.cutLine1 = { x: processed.x, y: processed.y };
        processed.cutLine2 = { x: processed.x, y: processed.y };
      }

      return processed;
    },

    filterData() {
      console.log('Block selection changed to:', this.selectedBlock);
      this.$nextTick(() => {
        this.redrawPlot();
      });
    },

    redrawPlot() {
      this.$forceUpdate();
    },

    scaleX(x) {
      const ranges = this.coordinateRanges;
      const xRange = ranges.xMax - ranges.xMin;
      if (xRange === 0) return this.plotWidth / 2; // Center if no range
      
      return this.margin + ((x - ranges.xMin) / xRange) * (this.plotWidth - 2 * this.margin);
    },

    scaleY(y) {
      const ranges = this.coordinateRanges;
      const yRange = ranges.yMax - ranges.yMin;
      if (yRange === 0) return this.plotHeight / 2; // Center if no range
      
      return this.plotHeight - this.margin - ((y - ranges.yMin) / yRange) * (this.plotHeight - 2 * this.margin);
    },

    scaleDistance(distance) {
      const ranges = this.coordinateRanges;
      const avgRange = ((ranges.xMax - ranges.xMin) + (ranges.yMax - ranges.yMin)) / 2;
      if (avgRange === 0) return distance; // Fallback
      
      return (distance / avgRange) * Math.min(this.plotWidth - 2 * this.margin, this.plotHeight - 2 * this.margin);
    },

    getTreeColor(tree) {
      return this.spgroupColors[tree.spgroup] || "#000000";
    },

    getTreeStroke(tree) {
      const status = tree.status.toUpperCase();
      if (status === 'CUT') return '#CC0000';
      if (status === 'VICTIM') return '#FF6600';
      return 'rgba(0, 0, 0, 0.3)';
    },

    getTreeStrokeWidth(tree) {
      const status = tree.status.toUpperCase();
      if (status === 'CUT') return 1.5;
      if (status === 'VICTIM') return 1;
      return 0.5;
    },

    showTooltip(event, tree) {
      this.tooltip = {
        visible: true,
        x: event.clientX + 10,
        y: event.clientY - 10,
        tree: tree
      };
    },

    hideTooltip() {
      this.tooltip.visible = false;
    },

    handleMouseMove(event) {
      if (this.tooltip.visible) {
        this.tooltip.x = event.clientX + 10;
        this.tooltip.y = event.clientY - 10;
      }
    }
  },
  
  mounted() {
    this.redrawPlot();
  }
}
</script>

<style scoped>
.loading-indicator {
  padding: 15px;
  background: #f8f8f8;
  border-radius: 4px;
  text-align: center;
  margin: 10px 0;
}

.error-message {
  padding: 15px;
  background: #ffebee;
  color: #d32f2f;
  border-radius: 4px;
  margin: 10px 0;
}

.debug-info {
  padding: 10px;
  background: #e3f2fd;
  border-radius: 4px;
  margin: 10px 0;
  font-family: monospace;
}

.tree-plot-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  font-family: Arial, sans-serif;
  min-height: 100vh;
  width: 100%;
}

.controls-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-group label {
  font-weight: 500;
  white-space: nowrap;
}

.control-group select,
.control-group input[type="range"] {
  padding: 4px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.plot-container {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  flex: 1;
  width: 100%;
}

svg {
  border: 1px solid #ccc;
  background-color: white;
  border-radius: 4px;
  flex: 1;
  max-width: calc(100vw - 300px);
}

.tree-point {
  cursor: pointer;
  transition: r 0.2s ease;
}

.tree-point:hover {
  r: 6;
}

.axis-label {
  font-size: 14px;
  font-weight: bold;
  fill: #333;
}

.legend {
  min-width: 200px;
  padding: 15px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  min-width: 250px;
}

.legend h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 1px solid #000;
}

.tooltip {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 10px;
  border-radius: 6px;
  font-size: 12px;
  pointer-events: none;
  z-index: 1000;
  max-width: 200px;
}

.tooltip div {
  margin-bottom: 3px;
}

.stats-panel {
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.95);
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 150px;
}

.stats-panel h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.stats-panel div {
  margin-bottom: 5px;
  font-size: 14px;
}

.grid path {
  stroke-dasharray: 2,2;
}

@media (max-width: 768px) {
  .tree-plot-container {
    padding: 10px;
  }
  
  .plot-container {
    flex-direction: column;
  }
  
  .sidebar {
    min-width: auto;
    width: 100%;
  }
  
  .controls-panel {
    flex-direction: column;
    align-items: flex-start;
  }
  
  svg {
    max-width: 100%;
  }
}
</style>