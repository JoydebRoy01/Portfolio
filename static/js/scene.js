/* 3D background: drifting embers, wireframe shapes and rings.
   The camera flies forward as the page scrolls and leans toward the pointer.
   Phones get fewer particles and a lower resolution; reduced-motion users
   get a single still frame. */

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";

const canvas = document.querySelector("[data-scene]");
if (canvas) init(canvas);

function init(canvas) {
  const isSmall = window.matchMedia("(max-width: 760px)").matches;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: !isSmall, powerPreference: "high-performance" });
  } catch (e) {
    canvas.remove(); // No WebGL: the page still works without the 3D layer.
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, isSmall ? 1.5 : 2));
  renderer.setSize(window.innerWidth, window.innerHeight, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 200);
  camera.position.set(0, 0, 10);

  const TRAVEL = 110;           // how far the camera flies over the whole page
  const DEPTH = TRAVEL + 40;    // how deep the scene goes

  // ---------- Embers ----------
  const COUNT = isSmall ? 420 : 1400;
  const positions = new Float32Array(COUNT * 3);
  const speeds = new Float32Array(COUNT);
  const colors = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 40;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 26;
    positions[i * 3 + 2] = 10 - Math.random() * DEPTH;
    speeds[i] = 0.004 + Math.random() * 0.016;
  }
  const emberGeo = new THREE.BufferGeometry();
  emberGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  emberGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

  const emberMat = new THREE.PointsMaterial({
    size: isSmall ? 0.16 : 0.13,
    map: makeDotTexture(),
    vertexColors: true,
    transparent: true,
    depthWrite: false,
    sizeAttenuation: true,
  });
  const embers = new THREE.Points(emberGeo, emberMat);
  scene.add(embers);

  // ---------- Wireframe shapes along the flight path ----------
  const shapeMat = new THREE.MeshBasicMaterial({ wireframe: true, transparent: true, opacity: 0.32 });
  const ringMat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.22, side: THREE.DoubleSide });
  const geos = [
    new THREE.IcosahedronGeometry(1.6, 1),
    new THREE.TorusKnotGeometry(1.1, 0.32, 90, 10),
    new THREE.OctahedronGeometry(1.5, 0),
    new THREE.DodecahedronGeometry(1.4, 0),
  ];
  const shapes = [];
  const SHAPES = isSmall ? 6 : 12;
  for (let i = 0; i < SHAPES; i++) {
    const mesh = new THREE.Mesh(geos[i % geos.length], shapeMat);
    const side = i % 2 === 0 ? -1 : 1;
    mesh.position.set(side * (5 + Math.random() * 5), (Math.random() - 0.5) * 7, -6 - (i / SHAPES) * TRAVEL);
    mesh.userData.spin = new THREE.Vector3(Math.random() * 0.006, 0.004 + Math.random() * 0.006, 0);
    mesh.userData.floatOffset = Math.random() * Math.PI * 2;
    mesh.userData.baseY = mesh.position.y;
    const s = 0.7 + Math.random() * 0.8;
    mesh.scale.setScalar(s);
    scene.add(mesh);
    shapes.push(mesh);
  }

  // Thin rings the camera passes through, like gates
  const rings = [];
  const RINGS = isSmall ? 4 : 7;
  for (let i = 0; i < RINGS; i++) {
    const ring = new THREE.Mesh(new THREE.RingGeometry(7.5, 7.56, 96), ringMat);
    ring.position.z = -14 - (i / RINGS) * TRAVEL;
    ring.rotation.z = Math.random() * Math.PI;
    scene.add(ring);
    rings.push(ring);
  }

  // ---------- Theme colours ----------
  function applyTheme() {
    const css = getComputedStyle(document.documentElement);
    const accent = new THREE.Color(css.getPropertyValue("--accent").trim() || "#FF3B4E");
    const ink = new THREE.Color(css.getPropertyValue("--ink").trim() || "#ffffff");
    const isLight = document.documentElement.getAttribute("data-theme") === "light";
    const cool = new THREE.Color(isLight ? "#3B4BD8" : "#8FA0FF");

    for (let i = 0; i < COUNT; i++) {
      const r = Math.random();
      const c = r < 0.55 ? accent : r < 0.85 ? ink : cool;
      colors[i * 3] = c.r; colors[i * 3 + 1] = c.g; colors[i * 3 + 2] = c.b;
    }
    emberGeo.attributes.color.needsUpdate = true;

    // Additive glow looks great on dark but disappears on light backgrounds.
    emberMat.blending = isLight ? THREE.NormalBlending : THREE.AdditiveBlending;
    emberMat.opacity = isLight ? 0.55 : 0.9;
    emberMat.needsUpdate = true;
    shapeMat.color = accent;
    shapeMat.opacity = isLight ? 0.22 : 0.32;
    ringMat.color = isLight ? ink : accent;
    ringMat.opacity = isLight ? 0.12 : 0.22;
    if (reduceMotion) render();
  }
  applyTheme();
  document.addEventListener("themechange", applyTheme);

  // ---------- Input ----------
  let scrollProgress = 0;
  let pointerX = 0, pointerY = 0;
  const readScroll = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    scrollProgress = max > 0 ? window.scrollY / max : 0;
  };
  readScroll();
  window.addEventListener("scroll", readScroll, { passive: true });
  window.addEventListener("pointermove", (e) => {
    pointerX = (e.clientX / window.innerWidth) * 2 - 1;
    pointerY = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });
  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    readScroll();
    if (reduceMotion) render();
  });

  // ---------- Loop ----------
  const camTarget = new THREE.Vector3();
  let smoothProgress = scrollProgress;
  const clock = new THREE.Clock();

  function render() {
    renderer.render(scene, camera);
  }

  function tick() {
    const t = clock.getElapsedTime();
    smoothProgress += (scrollProgress - smoothProgress) * 0.06;

    camTarget.set(pointerX * 1.2, -pointerY * 0.8, 10 - smoothProgress * TRAVEL);
    camera.position.lerp(camTarget, 0.05);
    camera.rotation.z = Math.sin(smoothProgress * Math.PI * 2) * 0.06 - pointerX * 0.02;
    camera.lookAt(camera.position.x * 0.3, camera.position.y * 0.3, camera.position.z - 20);

    // Embers rise and wrap around
    const pos = emberGeo.attributes.position.array;
    for (let i = 0; i < COUNT; i++) {
      const y = i * 3 + 1;
      pos[y] += speeds[i];
      pos[i * 3] += Math.sin(t * 0.6 + i) * 0.002;
      if (pos[y] > 13) pos[y] = -13;
    }
    emberGeo.attributes.position.needsUpdate = true;

    for (const m of shapes) {
      m.rotation.x += m.userData.spin.x;
      m.rotation.y += m.userData.spin.y;
      m.position.y = m.userData.baseY + Math.sin(t * 0.8 + m.userData.floatOffset) * 0.4;
    }
    rings.forEach((r, i) => { r.rotation.z += 0.0015 * (i % 2 ? 1 : -1); });

    render();
    requestAnimationFrame(tick);
  }

  if (reduceMotion) {
    render();
  } else {
    requestAnimationFrame(tick);
  }
}

function makeDotTexture() {
  const c = document.createElement("canvas");
  c.width = c.height = 64;
  const g = c.getContext("2d");
  const grd = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, "rgba(255,255,255,1)");
  grd.addColorStop(0.35, "rgba(255,255,255,.55)");
  grd.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = grd;
  g.fillRect(0, 0, 64, 64);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
