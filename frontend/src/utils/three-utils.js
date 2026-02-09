import * as THREE from 'three';

/**
 * 将轨迹点数组转换为 Three.js 的线段对象
 * @param {Array} points - 坐标点数组 [{x, y, z}, ...]
 * @param {number} color - 颜色
 * @returns {THREE.Line}
 */
export const createTrajectoryLine = (points, color = 0x00ff00) => {
  const geometry = new THREE.BufferGeometry();
  const positions = [];
  
  points.forEach(p => {
    positions.push(p.x, p.y, p.z);
  });
  
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  
  const material = new THREE.LineBasicMaterial({ color });
  return new THREE.Line(geometry, material);
};

/**
 * 坐标对齐辅助 (将大地坐标偏移到场景中心附近)
 * @param {Array} points 
 * @param {Object} offset {x, y, z}
 */
export const alignCoordinates = (points, offset) => {
  return points.map(p => ({
    x: p.x - offset.x,
    y: p.y - offset.y,
    z: p.z - offset.z
  }));
};
