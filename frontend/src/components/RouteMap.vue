<template>
  <div class="map-shell">
    <div v-if="mapError" class="map-error">地图加载失败，请稍后重试。</div>
    <div ref="mapEl" class="route-map"></div>
  </div>
</template>

<script setup lang="ts">
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps<{
  nodes: Array<{ code: string; name: string; latitude: number; longitude: number }>;
  path: string[];
  pathColor?: string;
}>();

const mapEl = ref<HTMLDivElement | null>(null);
const mapError = ref(false);
let map: L.Map | null = null;
let markersLayer: L.LayerGroup | null = null;
let pathLayer: L.Polyline | null = null;

const renderMap = () => {
  if (!map) return;
  const nodeMap = new Map(props.nodes.map((item) => [item.code, item]));
  markersLayer?.clearLayers();

  props.nodes.forEach((node) => {
    const marker = L.circleMarker([node.latitude, node.longitude], {
      radius: 7,
      color: "#9f4f28",
      weight: 2,
      fillColor: "#d97941",
      fillOpacity: 0.95
    }).bindPopup(`${node.name}`);
    markersLayer?.addLayer(marker);
  });

  if (pathLayer) {
    map.removeLayer(pathLayer);
    pathLayer = null;
  }

  const coordinates = props.path
    .map((code) => nodeMap.get(code))
    .filter(Boolean)
    .map((node) => [node!.latitude, node!.longitude] as [number, number]);

  if (coordinates.length > 1) {
    pathLayer = L.polyline(coordinates, {
      color: props.pathColor ?? "#b65a2e",
      weight: 5,
      opacity: 0.85
    }).addTo(map);
    map.fitBounds(pathLayer.getBounds(), { padding: [30, 30] });
  } else if (props.nodes.length > 0) {
    const bounds = L.latLngBounds(props.nodes.map((node) => [node.latitude, node.longitude] as [number, number]));
    map.fitBounds(bounds, { padding: [30, 30] });
  }
};

onMounted(() => {
  if (!mapEl.value) return;
  map = L.map(mapEl.value, { zoomControl: true });
  const tileLayer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  });
  tileLayer.on("tileerror", () => {
    mapError.value = true;
  });
  tileLayer.addTo(map);
  markersLayer = L.layerGroup().addTo(map);
  renderMap();
});

watch(
  () => [props.nodes, props.path],
  () => {
    renderMap();
  },
  { deep: true }
);

onBeforeUnmount(() => {
  map?.remove();
});
</script>
