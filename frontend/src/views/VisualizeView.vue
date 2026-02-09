<template>
  <div class="visualize-container">
    <div id="scene-container" ref="sceneContainer" @click="onSceneClick"></div>
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
import { onMounted, onUnmounted, ref } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import api from '@/services/api';

const sceneContainer = ref(null);
const selectedBorehole = ref(null);

let renderer, camera, scene, controls, raycaster, mouse;
const interactiveObjects = [];
let selectedObject = null;

const COLORS = {
  DEFAULT: 0x00ff00,
  HIGHLIGHT: 0xffa500,
};

function init() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x11162a);

  camera = new THREE.PerspectiveCamera(75, sceneContainer.value.clientWidth / sceneContainer.value.clientHeight, 0.1, 20000);
  camera.position.set(0, 100, 500);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(sceneContainer.value.clientWidth, sceneContainer.value.clientHeight);
  sceneContainer.value.appendChild(renderer.domElement);
  
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
  directionalLight.position.set(100, 100, 50);
  scene.add(directionalLight);

  const gridHelper = new THREE.GridHelper(2000, 20);
  gridHelper.rotation.x = Math.PI / 2;
  scene.add(gridHelper);

  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2();

  window.addEventListener('resize', onWindowResize);
}

function onSceneClick(event) {
    const rect = sceneContainer.value.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(interactiveObjects);

    if (intersects.length > 0) {
        const firstIntersected = intersects[0].object;
        
        // Deselect previous
        if (selectedObject) {
            selectedObject.material.color.set(COLORS.DEFAULT);
        }

        // Select new
        selectedObject = firstIntersected;
        selectedObject.material.color.set(COLORS.HIGHLIGHT);
        selectedBorehole.value = selectedObject.userData;

    } else {
         // Deselect if clicking on empty space
        if (selectedObject) {
            selectedObject.material.color.set(COLORS.DEFAULT);
        }
        selectedObject = null;
        selectedBorehole.value = null;
    }
}


function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

function onWindowResize() {
    if (sceneContainer.value) {
        camera.aspect = sceneContainer.value.clientWidth / sceneContainer.value.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(sceneContainer.value.clientWidth, sceneContainer.value.clientHeight);
    }
}

async function fetchDataAndRender() {
    try {
        const response = await api.getDrillingDesign();
        const sites = response.data;
        const center = new THREE.Vector3();
        let objectCount = 0;

        sites.forEach(site => {
            const sitePosition = new THREE.Vector3(site.coord_e, site.coord_z, -site.coord_n);
            const siteHelper = new THREE.Mesh(new THREE.SphereGeometry(10, 16, 16), new THREE.MeshBasicMaterial({ color: 0xff0000 }));
            siteHelper.position.copy(sitePosition);
            scene.add(siteHelper);
            center.add(sitePosition);
            objectCount++;

            site.boreholes.forEach(borehole => {
                if (borehole.trajectories && borehole.trajectories.length > 1) {
                    const points = borehole.trajectories.map(p => new THREE.Vector3(p.coord_e, p.coord_z, -p.coord_n));
                    const geometry = new THREE.BufferGeometry().setFromPoints(points);
                    // Use a thicker material for easier clicking
                    const material = new THREE.LineBasicMaterial({ color: COLORS.DEFAULT, linewidth: 5 });
                    const line = new THREE.Line(geometry, material);
                    
                    line.userData = { ...borehole, site_name: site.name };
                    scene.add(line);
                    interactiveObjects.push(line);
                }
            });
        });

        if (objectCount > 0) {
            center.divideScalar(objectCount);
            controls.target.copy(center);
        }

    } catch (error) {
        console.error("Failed to fetch or render drilling design data:", error);
    }
}

onMounted(() => {
  init();
  fetchDataAndRender();
  animate();
})

onUnmounted(() => {
    window.removeEventListener('resize', onWindowResize);
    if (sceneContainer.value && renderer.domElement) {
        sceneContainer.value.removeChild(renderer.domElement);
    }
})

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
