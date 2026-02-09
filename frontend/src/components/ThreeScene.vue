<template>
  <div ref="sceneContainer" class="three-scene-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const sceneContainer = ref(null);
let scene, camera, renderer, controls;
let animationId;

// 初始化场景
const initScene = () => {
  // 1. 创建场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0a); // 符合工业准则的深色背景

  // 2. 创建相机
  const width = sceneContainer.value.clientWidth;
  const height = sceneContainer.value.clientHeight;
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 2000);
  camera.position.set(50, 50, 100);

  // 3. 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  sceneContainer.value.appendChild(renderer.domElement);

  // 4. 添加控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // 5. 添加辅助工具
  const axesHelper = new THREE.AxesHelper(50);
  scene.add(axesHelper);

  const gridHelper = new THREE.GridHelper(200, 20);
  scene.add(gridHelper);

  // 6. 添加基础灯光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(10, 20, 10);
  scene.add(directionalLight);
};

// 渲染循环
const animate = () => {
  animationId = requestAnimationFrame(animate);
  if (controls) controls.update();
  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
};

// 窗口大小调整监听
const handleResize = () => {
  if (!sceneContainer.value) return;
  const width = sceneContainer.value.clientWidth;
  const height = sceneContainer.value.clientHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
};

onMounted(() => {
  initScene();
  animate();
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  cancelAnimationFrame(animationId);
  if (renderer) {
    renderer.dispose();
    renderer.forceContextLoss();
  }
});

// 暴露 API 给父组件
defineExpose({
  scene,
  camera,
  renderer
});
</script>

<style scoped>
.three-scene-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
