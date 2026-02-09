<template>
  <div class="visualize-container">
    <three-scene ref="threeSceneRef" />
    <div v-if="selectedBorehole" class="info-panel">
      <h3>钻孔详情</h3>
      <p><strong>钻孔编号:</strong> {{ selectedBorehole.borehole_no }}</p>
      <p><strong>所属钻场:</strong> {{ selectedBorehole.site_name }}</p>
      <p><strong>设计长度:</strong> {{ selectedBorehole.design_length }} m</p>
      <p><strong>孔径:</strong> {{ selectedBorehole.diameter }} mm</p>
      <p><strong>压裂段数:</strong> {{ selectedBorehole.segments }}</p>
      <button @click="selectedBorehole = null">关闭</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import * as THREE from 'three';
import ThreeScene from '@/components/ThreeScene.vue';
import { createTrajectoryLine } from '@/utils/three-utils';
import api from '@/services/api';

const threeSceneRef = ref(null);
const selectedBorehole = ref(null);
const interactiveObjects = [];

const COLORS = {
  DEFAULT: 0x00ff00,
  HIGHLIGHT: 0xffa500,
};

async function fetchDataAndRender() {
  if (!threeSceneRef.value) return;
  const { scene } = threeSceneRef.value;

  try {
    const response = await api.getDrillingDesign();
    const sites = response.data;
    
    // 简单模拟大地坐标到 3D 空间的对齐 (以第一个钻场为原点)
    let offset = null;

    sites.forEach(site => {
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

      site.boreholes.forEach(borehole => {
        if (borehole.trajectories && borehole.trajectories.length > 1) {
          const points = borehole.trajectories.map(p => ({
            x: p.coord_e - offset.x,
            y: p.coord_z - offset.y,
            z: -p.coord_n - offset.z
          }));
          
          const line = createTrajectoryLine(points, COLORS.DEFAULT);
          line.userData = { ...borehole, site_name: site.name };
          scene.add(line);
          interactiveObjects.push(line);
        }
      });
    });

  } catch (error) {
    console.error("Failed to fetch or render drilling design data:", error);
    // 如果 API 失败，渲染一条模拟轨迹用于演示
    renderMockTrajectory();
  }
}

function renderMockTrajectory() {
  const { scene } = threeSceneRef.value;
  const mockPoints = [
    {x: 0, y: 0, z: 0},
    {x: 10, y: 5, z: -20},
    {x: 30, y: 2, z: -50},
    {x: 60, y: -5, z: -100}
  ];
  const line = createTrajectoryLine(mockPoints, COLORS.DEFAULT);
  line.userData = { borehole_no: 'MOCK-001', site_name: '模拟钻场', design_length: 100, segments: 5 };
  scene.add(line);
}

onMounted(() => {
  // 等待组件挂载后获取数据
  setTimeout(() => {
    fetchDataAndRender();
  }, 100);
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
