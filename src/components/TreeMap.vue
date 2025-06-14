<template>
  <div class="tree-plot-container">
    <div class="controls-panel">
      <div class="control-group">
        <label for="blockSelect">Block Selection:</label>
        <select id="blockSelect" v-model="selectedBlock" @change="filterData">
          <option v-for="block in availableBlocks" :key="block" :value="block">
            Block {{ block }}
          </option>
        </select>
        
    <!-- Tooltip -->
    <div 
      v-if="tooltip.visible" 
      class="tooltip"
      :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
    >
      <div><strong>Tree ID:</strong> {{ tooltip.tree?.id || 'N/A' }}</div>
      <div><strong>Position:</strong> ({{ tooltip.tree?.x }}, {{ tooltip.tree?.y }})</div>
      <div><strong>Species Group:</strong> {{ tooltip.tree?.spgroup }}</div>
      <div><strong>Status:</strong> {{ tooltip.tree?.status }}</div>
      <div v-if="tooltip.tree?.status.toUpperCase() === 'CUT'">
        <strong>Cut Angle:</strong> {{ tooltip.tree?.cutAngle }}°
      </div>
      <div v-if="tooltip.tree?.stemHeight">
        <strong>Stem Height:</strong> {{ tooltip.tree?.stemHeight }}
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
            :key="`tree-${index}`"
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
  props: {
    treeData: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      selectedBlock: '1',
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
      if (!this.treeData.length) return ['1'];
      const blocks = [...new Set(this.treeData.map(tree => tree.BlockX?.toString().trim()))];
      return blocks.filter(Boolean).sort();
    },
    filteredTrees() {
      if (!this.treeData.length) return this.generateSampleData();
      
      return this.treeData
        .filter(tree => 
          tree.BlockX?.toString().trim() === this.selectedBlock && 
          tree.BlockY?.toString().trim() === this.selectedBlock
        )
        .map(tree => this.processTreeData(tree));
    }
  },
  methods: {
    generateSampleData() {
      // Generate sample data for demonstration - more trees like the reference image
      const sampleTrees = [];
      for (let i = 0; i < 400; i++) {
        const tree = {
          id: i + 1,
          x: Math.random() * 100,
          y: Math.random() * 100,
          spgroup: Math.floor(Math.random() * 7) + 1,
          status: this.getRandomStatus(),
          cutAngle: Math.random() * 360,
          stemHeight: 10 + Math.random() * 20
        };
        sampleTrees.push(this.processTreeData(tree));
      }
      return sampleTrees;
    },
    
    getRandomStatus() {
      const rand = Math.random();
      if (rand < 0.6) return 'KEEP';      // 60% keep
      else if (rand < 0.75) return 'CUT';  // 15% cut
      else if (rand < 0.85) return 'VICTIM'; // 10% victim
      else return '-';                     // 15% other
    },
    
    processTreeData(tree) {
      const processedTree = {
        ...tree,
        x: parseFloat(tree.x),
        y: parseFloat(tree.y),
        spgroup: tree.spgroup?.toString() || '1',
        status: tree.status?.toString().trim() || '-',
        cutAngle: parseFloat(tree['Damage(Cut angle)'] || tree.cutAngle || 0),
        stemHeight: parseFloat(tree['Stem Height'] || tree.stemHeight || 15)
      };
      
      // Calculate cut lines and crown center for CUT trees
      if (processedTree.status.toUpperCase() === 'CUT') {
        const angle0 = processedTree.cutAngle;
        const angle1 = processedTree.cutAngle + 1;
        const angle2 = processedTree.cutAngle - 1;
        const height = processedTree.stemHeight;
        
        const angleRad0 = (90 - angle0) * Math.PI / 180;
        const angleRad1 = (90 - angle1) * Math.PI / 180;
        const angleRad2 = (90 - angle2) * Math.PI / 180;
        
        const dx = height * Math.cos(angleRad1);
        const dy0 = height * Math.sin(angleRad0);
        const dy1 = height * Math.sin(angleRad1);
        const dy2 = height * Math.sin(angleRad2);
        
        processedTree.cutLine1 = {
          x: processedTree.x + dx,
          y: processedTree.y + dy1
        };
        processedTree.cutLine2 = {
          x: processedTree.x + dx,
          y: processedTree.y + dy2
        };
        processedTree.crownCenter = {
          x: processedTree.x + dx,
          y: processedTree.y + dy0
        };
      }
      
      return processedTree;
    },
    
    filterData() {
      this.$nextTick(() => {
        this.redrawPlot();
      });
    },
    
    redrawPlot() {
      // Force reactivity update
      this.$forceUpdate();
    },
    
    scaleX(x) {
      return this.margin + (x / 100) * (this.plotWidth - 2 * this.margin);
    },
    
    scaleY(y) {
      return this.plotHeight - this.margin - (y / 100) * (this.plotHeight - 2 * this.margin);
    },
    
    scaleDistance(distance) {
      return (distance / 100) * (this.plotWidth - 2 * this.margin);
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
    // Initial plot setup
    this.redrawPlot();
  }
}
</script>

<style scoped>
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