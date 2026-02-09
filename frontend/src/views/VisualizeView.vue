<template>
  <div class="visualize-container">
    <three-scene ref="threeSceneRef" @click="handleSceneClick" />
    <div v-if="selectedData" class="info-panel">
      <h3>{{ selectedData.type === 'borehole' ? '钻孔详情' : '压裂段详情' }}</h3>
      <template v-if="selectedData.type === 'borehole'">
        <p><strong>钻孔编号:</strong> {{ selectedData.borehole_no }}</p>
        <p><strong>所属钻场:</strong> {{ selectedData.site_name }}</p>
        <p><strong>设计长度:</strong> {{ selectedData.design_length }} m</p>
      </template>
      <template v-else>
        <p><strong>段号:</strong> {{ selectedData.segment_no }}</p>
        <p><strong>压力:</strong> {{ selectedData.pressure.toFixed(2) }} MPa</p>
        <p><strong>排量:</strong> {{ selectedData.total_volume.toFixed(2) }} m³</p>
        <p><strong>流量:</strong> {{ selectedData.flow_rate.toFixed(2) }} m³/min</p>
      </template>
      <button @click="selectedData = null">关闭</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import ThreeScene from '@/components/ThreeScene.vue';
import { createTrajectoryLine, createFractureSphere } from '@/utils/three-utils';
import api from '@/services/api';

const threeSceneRef = ref(null);
const selectedData = ref(null);
const interactiveObjects = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

const COLORS = {
  DEFAULT: 0x00ff00,
  HIGHLIGHT: 0xffa500,
  FRACTURE_LOW: 0x00ff00,
  FRACTURE_HIGH: 0xff0000,
};

// 根据数值映射颜色 (绿 -> 红)
function getHeatColor(value, min, max) {
  const normalized = Math.min(1, Math.max(0, (value - min) / (max - min)));
  return new THREE.Color().lerpColors(
    new THREE.Color(COLORS.FRACTURE_LOW),
    new THREE.Color(COLORS.FRACTURE_HIGH),
    normalized
  );
}

async function fetchDataAndRender() {
  if (!threeSceneRef.value) return;
  const { scene } = threeSceneRef.value;

  try {
    const response = await api.getDrillingDesign();
    const sites = response.data;
    
    let offset = null;

    for (const site of sites) {
      if (!offset) {
        offset = { x: site.coord_e, y: site.coord_z, z: -site.coord_n };
      }

      const sitePosition = new THREE.Vector3(
        site.coord_e - offset.x,
        site.coord_z - offset.y,
        -site.coord_n - offset.z
      );

      // 渲染钻场标记
      const siteHelper = new THREE.Mesh(
        new THREE.SphereGeometry(2, 16, 16),
        new THREE.MeshBasicMaterial({ color: 0xff0000 })
      );
      siteHelper.position.copy(sitePosition);
      scene.add(siteHelper);

      for (const borehole of site.boreholes) {
        if (borehole.trajectories && borehole.trajectories.length > 1) {
          const points = borehole.trajectories.map(p => ({
            x: p.coord_e - offset.x,
            y: p.coord_z - offset.y,
            z: -p.coord_n - offset.z
          }));
          
          const line = createTrajectoryLine(points, COLORS.DEFAULT);
          line.userData = { ...borehole, site_name: site.name, type: 'borehole' };
          scene.add(line);
          interactiveObjects.push(line);

          // 获取压裂详情并渲染
          await renderFractureSegments(borehole.id, offset);
        }
      }
    }

  } catch (error) {
    console.error("Failed to fetch or render design data:", error);
  }
}

async function renderFractureSegments(boreholeId, offset) {
  const { scene } = threeSceneRef.value;
  try {
    const res = await api.getBoreholeFractureData(boreholeId);
    const fractureData = res.data;

    fractureData.forEach(seg => {
      const pos = {
        x: seg.position.x - offset.x,
        y: seg.position.y - offset.y,
        z: seg.position.z - offset.z
      };

      // 动态映射：半径 -> 压力，颜色 -> 排量
      const radius = 2 + (seg.pressure / 10);
      const color = getHeatColor(seg.total_volume, 100, 1000);

      const sphere = createFractureSphere(pos, radius, color);
      sphere.userData = { ...seg, type: 'segment' };
      scene.add(sphere);
      interactiveObjects.push(sphere);
    });
  } catch (e) {
    console.warn(`No fracture data for borehole ${boreholeId}`);
  }
}

function handleSceneClick(event) {
  if (!threeSceneRef.value) return;
  const { camera } = threeSceneRef.value;
  
  // 计算鼠标在 3D 空间中的归一化坐标
  const rect = event.target.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(interactiveObjects);

  if (intersects.length > 0) {
    selectedData.value = intersects[0].object.userData;
  } else {
    selectedData.value = null;
  }
}

onMounted(() => {
  setTimeout(() => {
    fetchDataAndRender();
  }, 200);
});
</script>

<style scoped>
.visualize-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 4rem - 4rem); /* Full height minus header and main padding */
}
#scene-container {
  width: 100%;
  height: 100%;
}
.info-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: rgba(26, 41, 82, 0.9);
  border: 1px solid #2a3f78;
  color: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}
.info-panel h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid #2a3f78;
  padding-bottom: 0.5rem;
}
.info-panel p {
  margin: 0.5rem 0;
}
.info-panel button {
    margin-top: 1rem;
    width: 100%;
    padding: 0.5rem;
    background-color: #f44336;
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}
</style>
