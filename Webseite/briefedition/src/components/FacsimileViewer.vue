<!-- HINWEIS: Diese Komponente wurde Schritt für Schritt  mithilfe von GPT-5 generiert und anschließend überarbeitet. -->
  
<!--  Der FacsimileViewer wird in der SingleLetterView verwendet, um die Digitalisate anzuzeigen.  -->
<template>
  <div class="facsimile-viewer">

    <!-- Carousel -->
    <div class="carousel-container position-relative">
      <div class="carousel-inner">
        <div v-for="(img, idx) in images" :key="idx" class="carousel-item" :class="{ active: idx === currentImageIndex }">
          <img :src="img" class="d-block carousel-image" alt="Digitalisat" @mousedown="startDrag" @wheel.prevent="onWheel"/>
        </div>
      </div>

      <!-- Buttons zur Navigation (im Bootstrap Style) -->
      <button class="carousel-control-prev" type="button" @click="prevSlide">
        <span class="carousel-control-prev-icon"></span>
      </button>

      <button class="carousel-control-next" type="button"@click="nextSlide">
        <span class="carousel-control-next-icon"></span>
      </button>
    </div>

    <!-- Rotation, Zoom und Reset der Ansicht -->
    <div class="mt-2 d-flex justify-content-center gap-2">
      <button class="btn btn-dark button" @click="rotateImage(-90)">⟲ Drehen</button>
      <button class="btn btn-dark button" @click="rotateImage(90)">⟳ Drehen</button>
      <button class="btn btn-dark button" @click="zoomImage(1.2)">＋ Zoom</button>
      <button class="btn btn-dark button" @click="zoomImage(0.8)">− Zoom</button>
      <button class="btn btn-dark button" @click="resetTransform">Reset</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const dragging = ref(false); // Dragging des Bildes (aktiv bzw. inaktiv)
const last = ref({ x: 0, y: 0 }); // Position der Maus
const props = defineProps({       // Digitalisate (Bilder)
  images: { type: Array, required: true }
});

// Carousel-Status
const currentImageIndex = ref(0);

// Status der Bildtransformation (gedreht, gezoomt, Position des Mauszeigers)
const rotation = ref(0);
const scale = ref(1);
const pos = ref({ x: 0, y: 0 });

// Für Navigation des Carousels
// Nächstes Bild (blättern)
function nextSlide() {
  currentImageIndex.value =
    (currentImageIndex.value + 1) % props.images.length;
  resetTransform();
}
// Voriges Bild (blättern)
function prevSlide() {
  currentImageIndex.value =
    (currentImageIndex.value - 1 + props.images.length) % props.images.length;
  resetTransform();
}
// Transformieren des aktuellen Bildes (drehen, zoomen) ausführen
function applyTransform() {
  const img = document.querySelector(".carousel-item.active img");
  if (!img) return;
  img.style.transform =
    `translate(${pos.value.x}px, ${pos.value.y}px)` +
    ` rotate(${rotation.value}deg)` +
    ` scale(${scale.value})`;
}
// Rotation
function rotateImage(deg) {
  rotation.value += deg;
  applyTransform();
}
// Zoom
function zoomImage(factor) {
  scale.value *= factor;
  applyTransform();
}
// Reset
function resetTransform() {
  rotation.value = 0;
  scale.value = 1;
  pos.value = { x: 0, y: 0 };
  applyTransform();
}
// Dragging im Bild und Zoomen mit Scroll
function startDrag(e) {
  e.preventDefault();       // verhindert Textauswahl
  dragging.value = true;    // Drag aktivieren
  last.value = { x: e.clientX, y: e.clientY };

  // Globale Listener für Mausbewegung und Loslassen
  window.addEventListener("mousemove", onDrag);
  window.addEventListener("mouseup", endDrag);
}
// Dragging
function onDrag(e) {
  if (!dragging.value) return; // nur bewegen, wenn gedrückt

  const dx = e.clientX - last.value.x;
  const dy = e.clientY - last.value.y;

  pos.value.x += dx;
  pos.value.y += dy;

  last.value = { x: e.clientX, y: e.clientY };
  applyTransform();
}
// Drag bewegen bei loslassen der Maus
function endDrag() {
  dragging.value = false;    // Drag deaktivieren
  window.removeEventListener("mousemove", onDrag);
  window.removeEventListener("mouseup", endDrag);
}
// Zoomen mit Mausrad
function onWheel(e) {
  const delta = e.deltaY < 0 ? 1.1 : 0.9;
  scale.value *= delta;
  applyTransform();
}

// Bei Wechsel des Bildes (der Slide): Reset
watch(currentImageIndex, resetTransform);
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  margin: auto;
  overflow: hidden;
  background-color: gray;
}

.carousel-inner {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.carousel-item {
  display: none;
  width: 100%;
  height: 100%;
  text-align: center;
}

.carousel-item.active {
  display: block;
}

.carousel-image {
  max-width: 100%;
  height: auto;
  cursor: grab;
  user-select: none;
  transform-origin: center center;
  transition: transform 0.25s ease;
}

.carousel-image.dragging {
  cursor: grabbing;
  transition: none;
}

.carousel-control-prev,
.carousel-control-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.3);
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.carousel-control-prev {
  left: 10px;
}

.carousel-control-next {
  right: 10px;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  display: inline-block;
  width: 1.5rem;
  height: 1.5rem;
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

.button {
  background-color: var(--primary-blue) !important;
}
</style>
