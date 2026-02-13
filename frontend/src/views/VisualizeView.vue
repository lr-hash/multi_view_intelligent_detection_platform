<template>
  <div class="visualize-container">
    <three-scene ref="threeSceneRef" @click="handleSceneClick" />
    
    <!-- 顶部控制与图层面板 -->
    <div class="overlay-controls">
      <div class="control-group">
        <h4>图层管理</h4>
        <div class="layer-item" v-for="(val, key) in layers" :key="key">
          <input type="checkbox" :id="key" v-model="layers[key]" @change="toggleLayers">
          <label :for="key">{{ layerNames[key] }}</label>
        </div>
      </div>
      <div class="control-group">
        <h4>视图控制</h4>
        <button @click="resetView" class="ui-btn">全景复位</button>
        <button @click="toggle2D" class="ui-btn">{{ is2D ? '3D视角' : '2D俯视' }}</button>
      </div>
    </div>

    <!-- 状态统计 -->
    <div class="top-status-bar">
      <div class="status-node">
        <span class="dot pulse-blue"></span>
        <span class="label">5 钻场 | 30 钻孔 (96mm)</span>
      </div>
      <div class="status-node" v-if="hoverInfo">
        <span class="label">当前聚焦: {{ hoverInfo }}</span>
      </div>
    </div>

    <!-- 详情面板 -->
    <div v-if="selectedData" class="info-panel animate-slide-in">
      <div class="panel-header">
        <h3>{{ getPanelTitle() }}</h3>
        <button class="close-btn" @click="selectedData = null">×</button>
      </div>
      
      <div class="panel-body">
        <template v-if="selectedData.type === 'borehole'">
          <div class="info-row"><span class="label">编号:</span> <span class="val highlight">{{ selectedData.borehole_no }}</span></div>
          <div class="info-row"><span class="label">孔径:</span> <span class="val">96 mm</span></div>
          <div class="info-row"><span class="label">设计长度:</span> <span class="val">{{ selectedData.design_length.toFixed(1) }} m</span></div>
          <div class="info-row"><span class="label">方位/倾角:</span> <span class="val">{{ selectedData.azimuth }}° / {{ selectedData.dip_angle }}°</span></div>
          <div class="info-row"><span class="label">分段数:</span> <span class="val">{{ selectedData.segments }} 段</span></div>
        </template>
        
        <template v-else-if="selectedData.type === 'site'">
          <div class="info-row"><span class="label">钻场名称:</span> <span class="val highlight">{{ selectedData.name }}</span></div>
          <div class="info-row"><span class="label">位置:</span> <span class="val">{{ selectedData.location }}</span></div>
          <div class="info-row"><span class="label">包含钻孔:</span> <span class="val">6 个 (1#-6#)</span></div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, watch } from 'vue';
import * as THREE from 'three';
import ThreeScene from '@/components/ThreeScene.vue';
import * as TUtils from '@/utils/three-utils';
import api from '@/services/api';

const threeSceneRef = ref(null);
const selectedData = ref(null);
const hoverInfo = ref(null);
const is2D = ref(false);

const layers = reactive({
  roadway: true,
  coalSeam: true,
  designLine: true,
  actualPipe: true,
  sites: true,
  roof: false
});

const layerNames = {
  roadway: '巷道骨架',
  coalSeam: '地质层位 (煤层)',
  designLine: '设计轨迹 (虚线)',
  actualPipe: '实钻轨迹 (96mm)',
  sites: '钻场节点',
  roof: '15m 顶板层位'
};

const stats = reactive({ boreholeCount: 0, fractureCount: 0, msCount: 0 });
const interactiveObjects = [];
const layerGroups = {};

let sceneOffset = { x: 0, y: 0, z: 0 };

const getPanelTitle = () => {
  if (!selectedData.value) return '';
  return selectedData.value.type === 'site' ? '钻场详情' : '钻孔全生命周期参数';
};

async function initVisuals() {
  if (!threeSceneRef.value) return;
  const { scene } = threeSceneRef.value;

  // 初始化图层分组
  Object.keys(layers).forEach(key => {
    const group = new THREE.Group();
    scene.add(group);
    layerGroups[key] = group;
  });

  try {
    const response = await api.getDrillingDesign();
    const sites = response.data;
    if (!sites.length) return;

    // 以第一个钻场为坐标原点
    sceneOffset = { x: sites[0].coord_e, y: sites[0].coord_z, z: -sites[0].coord_n };

    // 1. 渲染巷道骨架 (简化为连接钻场的路径)
    const roadwayPoints = sites.map(s => ({ x: s.coord_e - sceneOffset.x, y: s.coord_z - sceneOffset.y, z: -s.coord_n - sceneOffset.z }));
    const roadwayMesh = TUtils.createRoadway(roadwayPoints);
    layerGroups.roadway.add(roadwayMesh);

    // 2. 渲染煤层
    const coalSeam = TUtils.createCoalSeam({x: 0, y: 0, z: -500}, 300, 1500);
    layerGroups.coalSeam.add(coalSeam);

    // 3. 渲染顶板层位
    const roof = TUtils.createRoofLayer({x: 0, y: 0, z: -500}, 300, 1500, 15);
    layerGroups.roof.add(roof);

    for (const site of sites) {
      // 钻场标记
      const pos = { x: site.coord_e - sceneOffset.x, y: site.coord_z - sceneOffset.y, z: -site.coord_n - sceneOffset.z };
      const marker = TUtils.createSiteMarker(pos, site.name);
      marker.userData = { ...site, type: 'site' };
      layerGroups.sites.add(marker);
      interactiveObjects.push(marker.children[0]); // 将核心球体加入交互

      for (const borehole of site.boreholes) {
        // 设计轨迹
        const designLine = TUtils.createDesignTrajectory(pos, borehole.design_length, borehole.azimuth, borehole.dip_angle);
        layerGroups.designLine.add(designLine);

        // 实钻管路 (96mm)
        if (borehole.trajectories?.length > 1) {
          const points = borehole.trajectories.map(p => ({
            x: p.coord_e - sceneOffset.x,
            y: p.coord_z - sceneOffset.y,
            z: -p.coord_n - sceneOffset.z
          }));
          
          const pipe = TUtils.createTrajectoryLine(points);
          pipe.userData = { ...borehole, type: 'borehole' };
          layerGroups.actualPipe.add(pipe);
          interactiveObjects.push(pipe);
        }
      }
    }
    
    toggleLayers(); // 应用初始显隐
  } catch (error) {
    console.error("Viz Error:", error);
  }
}

function toggleLayers() {
  Object.keys(layers).forEach(key => {
    if (layerGroups[key]) layerGroups[key].visible = layers[key];
  });
}

function resetView() {
  const { controls, camera } = threeSceneRef.value;
  camera.position.set(100, 100, 100);
  controls.target.set(0, 0, 0);
  controls.update();
  is2D.value = false;
}

function toggle2D() {
  const { controls, camera } = threeSceneRef.value;
  if (!is2D.value) {
    camera.position.set(0, 500, 0);
    controls.target.set(0, 0, 0);
    is2D.value = true;
  } else {
    resetView();
  }
  controls.update();
}

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function handleSceneClick(event) {
  const { camera } = threeSceneRef.value;
  const rect = event.target.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(interactiveObjects);
  
  if (intersects.length > 0) {
    let obj = intersects[0].object;
    // 如果是 SiteMarker 的子物体，找父级的 userData
    const data = obj.userData.type ? obj.userData : (obj.parent?.userData?.type ? obj.parent.userData : null);
    selectedData.value = data;
  } else {
    selectedData.value = null;
  }
}

onMounted(() => {
  setTimeout(initVisuals, 300);
});
</script>

<style scoped>
.visualize-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 8rem);
  background: #020617;
}

.overlay-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(15, 23, 42, 0.85);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  width: 200px;
  backdrop-filter: blur(8px);
  z-index: 100;
}

.control-group { margin-bottom: 1.5rem; }
.control-group h4 { margin: 0 0 0.8rem 0; font-size: 0.9rem; color: #94a3b8; border-bottom: 1px solid #334155; padding-bottom: 5px; }

.layer-item { margin-bottom: 0.6rem; display: flex; align-items: center; font-size: 0.85rem; }
.layer-item input { margin-right: 10px; cursor: pointer; }

.ui-btn {
  width: 100%;
  padding: 8px;
  background: #334155;
  border: 1px solid #475569;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 8px;
  font-size: 0.8rem;
}
.ui-btn:hover { background: #475569; }

.top-status-bar {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  gap: 15px;
}
.status-node {
  background: rgba(15, 23, 42, 0.8);
  padding: 8px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  color: #f1f5f9;
}

.info-panel {
  position: absolute;
  bottom: 40px;
  right: 240px;
  background: rgba(30, 41, 59, 0.95);
  width: 320px;
  border-radius: 12px;
  border: 1px solid #3b82f6;
  color: #fff;
  z-index: 100;
}
.panel-header { padding: 1rem; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
.panel-body { padding: 1rem; }
.info-row { display: flex; justify-content: space-between; margin-bottom: 0.8rem; }
.info-row .label { color: #94a3b8; }
.info-row .val { font-weight: bold; }
.val.highlight { color: #3b82f6; }

.close-btn { background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 1.2rem; }

.animate-slide-in { animation: slideIn 0.3s ease-out; }
@keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
</style>
