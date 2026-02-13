import * as THREE from 'three';

/**
 * 将轨迹点数组转换为管状 3D 钻孔 (实钻态 - 96mm)
 */
export const createTrajectoryLine = (points, color = 0x3b82f6) => {
  if (points.length < 2) return new THREE.Group();
  const curvePoints = points.map(p => new THREE.Vector3(p.x, p.y, p.z));
  const curve = new THREE.CatmullRomCurve3(curvePoints);
  
  // 半径 0.048m = 48mm, 直径 96mm
  const geometry = new THREE.TubeGeometry(curve, 64, 0.048, 8, false);
  const material = new THREE.MeshPhongMaterial({ 
    color,
    specular: 0xffffff,
    shininess: 30,
    transparent: true,
    opacity: 0.9
  });
  
  return new THREE.Mesh(geometry, material);
};

/**
 * 创建设计态轨迹 (虚线感)
 */
export const createDesignTrajectory = (start, length, azimuth, dip, color = 0x94a3b8) => {
  const radAz = (azimuth * Math.PI) / 180;
  const radDip = (dip * Math.PI) / 180;
  
  const distH = length * Math.cos(radDip);
  const de = distH * Math.sin(radAz);
  const dn = distH * Math.cos(radAz);
  const dz = length * Math.sin(radDip);

  const end = new THREE.Vector3(start.x + de, start.y + dz, start.z - dn);
  const points = [new THREE.Vector3(start.x, start.y, start.z), end];
  
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  const material = new THREE.LineDashedMaterial({
    color,
    dashSize: 2,
    gapSize: 1,
    scale: 1
  });
  
  const line = new THREE.Line(geometry, material);
  line.computeLineDistances();
  return line;
};

/**
 * 创建巷道骨架
 */
export const createRoadway = (points, width = 4, height = 3.5, color = 0x334155) => {
  if (points.length < 2) return new THREE.Group();
  const curvePoints = points.map(p => new THREE.Vector3(p.x, p.y, p.z));
  const curve = new THREE.CatmullRomCurve3(curvePoints);
  
  // 使用类似矩形的管道
  const geometry = new THREE.BoxGeometry(width, height, 1);
  const shape = new THREE.Shape();
  shape.moveTo(-width/2, -height/2);
  shape.lineTo(width/2, -height/2);
  shape.lineTo(width/2, height/2);
  shape.lineTo(-width/2, height/2);
  shape.lineTo(-width/2, -height/2);

  const extrudeSettings = {
    steps: 100,
    bevelEnabled: false,
    extrudePath: curve
  };

  const extrudeGeo = new THREE.ExtrudeGeometry(shape, extrudeSettings);
  const material = new THREE.MeshPhongMaterial({
    color,
    transparent: true,
    opacity: 0.3,
    side: THREE.DoubleSide
  });

  return new THREE.Mesh(extrudeGeo, material);
};

/**
 * 创建钻场标记节点 (发光球体)
 */
export const createSiteMarker = (position, name, color = 0x0ea5e9) => {
  const group = new THREE.Group();
  
  // 核心
  const geo = new THREE.SphereGeometry(1.5, 16, 16);
  const mat = new THREE.MeshPhongMaterial({
    color,
    emissive: color,
    emissiveIntensity: 0.5
  });
  const mesh = new THREE.Mesh(geo, mat);
  group.add(mesh);

  // 外圈光晕
  const haloGeo = new THREE.SphereGeometry(2.5, 16, 16);
  const haloMat = new THREE.MeshBasicMaterial({
    color,
    transparent: true,
    opacity: 0.2
  });
  group.add(new THREE.Mesh(haloGeo, haloMat));

  group.position.set(position.x, position.y, position.z);
  group.userData = { name, isSite: true };
  
  return group;
};

/**
 * 创建煤层地层参考
 */
export const createCoalSeam = (center, width, height, thickness = 4, color = 0x111827) => {
  const geometry = new THREE.BoxGeometry(width, thickness, height);
  const material = new THREE.MeshPhongMaterial({
    color,
    transparent: true,
    opacity: 0.4
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(center.x, center.y - thickness/2, center.z);
  return mesh;
};

/**
 * 创建顶板参考平面 (15m 处)
 */
export const createRoofLayer = (center, width, height, targetHeight = 15, color = 0x10b981) => {
  const geometry = new THREE.PlaneGeometry(width, height);
  const material = new THREE.MeshBasicMaterial({
    color,
    transparent: true,
    opacity: 0.1,
    side: THREE.DoubleSide,
    wireframe: true
  });
  const plane = new THREE.Mesh(geometry, material);
  plane.rotation.x = -Math.PI / 2;
  plane.position.set(center.x, center.y + targetHeight, center.z);
  return plane;
};

/**
 * 原有的压裂和震源函数保留并优化...
 */
export const createFractureSphere = (position, radius = 5, color = 0x22c55e) => {
  const group = new THREE.Group();
  const core = new THREE.Mesh(
    new THREE.SphereGeometry(radius * 0.4, 16, 16),
    new THREE.MeshBasicMaterial({ color })
  );
  group.add(core);

  const glow = new THREE.Mesh(
    new THREE.SphereGeometry(radius, 32, 32),
    new THREE.MeshPhongMaterial({
      color,
      transparent: true,
      opacity: 0.2,
      blending: THREE.AdditiveBlending
    })
  );
  group.add(glow);

  group.position.set(position.x, position.y, position.z);
  return group;
};