<template>
  <section class="panel-card">
    <div class="section-top">
      <div>
        <h2>地图导航</h2>
        <p>支持多策略规划、预计耗时解释和路线收藏，北京样板场景可进行精细导航。</p>
      </div>
    </div>

    <div class="filter-bar">
      <select v-model="selectedCity" class="select-input" @change="handleCityChange">
        <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
      </select>
      <select v-model="selectedSceneName" class="select-input" @change="loadScene">
        <option v-for="scene in visibleScenes" :key="scene.name" :value="scene.name">{{ scene.label }}</option>
      </select>
      <select v-model="strategy" class="select-input">
        <option value="distance">最短距离</option>
        <option value="time">最快到达</option>
        <option value="congestion">避开拥堵</option>
        <option value="scenic">轻松逛/打卡优先</option>
      </select>
      <select v-model="transportMode" class="select-input">
        <option value="walk">步行</option>
        <option value="bike">骑行</option>
        <option value="shuttle">摆渡车</option>
        <option value="mixed">综合方式</option>
      </select>
    </div>

    <RouteMap :nodes="mapNodes" :path="displayPathCodes" />

    <div class="helper-grid">
      <div class="helper-card">
        <h3>当前城市</h3>
        <p>{{ selectedCity }}</p>
        <p>{{ currentSceneMessage }}</p>
      </div>
      <div class="helper-card">
        <h3>推荐起点</h3>
        <p v-for="item in suggestedNodes" :key="item.code">{{ item.name }}</p>
      </div>
    </div>

    <template v-if="supportsRouting">
      <form class="search-form" @submit.prevent="planRoute">
        <select v-model="startCode" class="select-input">
          <option v-for="node in placeOptions" :key="node.code" :value="node.code">{{ node.name }}</option>
        </select>
        <select v-model="endCode" class="select-input">
          <option v-for="node in placeOptions" :key="node.code" :value="node.code">{{ node.name }}</option>
        </select>
        <button class="primary-btn" type="submit">{{ singleLoading ? "规划中..." : "规划单点路线" }}</button>
      </form>

      <div v-if="singleRoute" class="route-summary route-card">
        <div class="section-top compact">
          <h3>{{ singleRoute.strategy_label }}</h3>
          <button class="secondary-btn" @click="saveCurrentRoute">收藏当前路线</button>
        </div>
        <p>{{ singleRoute.explanation }}</p>
        <div class="detail-stats">
          <span class="stat-pill">{{ singleRoute.total_distance_m }} m</span>
          <span class="stat-pill">{{ singleRoute.estimated_minutes }} 分钟</span>
          <span class="stat-pill">平均拥堵 {{ singleRoute.average_congestion }}</span>
        </div>
        <p><strong>路线：</strong> {{ singleRoute.path_names.join(" → ") }}</p>
      </div>

      <section v-if="singleRoute?.alternatives?.length" class="results-section">
        <div class="section-top compact">
          <h3>备选路线</h3>
          <span class="toolbar-hint">点击卡片可切换地图高亮</span>
        </div>
        <div class="card-grid compact-grid">
          <article
            v-for="item in singleRoute.alternatives"
            :key="item.strategy"
            class="item-card"
            :class="{ selected: selectedAlternativeStrategy === item.strategy }"
            @click="selectedAlternativeStrategy = item.strategy"
          >
            <h3>{{ item.strategy_label }}</h3>
            <p>{{ item.explanation }}</p>
            <p>{{ item.total_distance_m }} m · {{ item.estimated_minutes }} 分钟</p>
          </article>
        </div>
      </section>

      <form class="search-form" @submit.prevent="planMultiRoute">
        <select v-model="multiTargetCodes" class="select-input" multiple size="4">
          <option v-for="node in placeOptions" :key="node.code" :value="node.code">{{ node.name }}</option>
        </select>
        <button class="primary-btn" type="submit">{{ multiLoading ? "规划中..." : "规划多点闭环" }}</button>
      </form>

      <div v-if="multiRoute" class="route-summary route-card">
        <h3>{{ multiRoute.optimization_label }}</h3>
        <p>{{ multiRoute.explanation }}</p>
        <div class="detail-stats">
          <span class="stat-pill">{{ multiRoute.total_distance_m }} m</span>
          <span class="stat-pill">{{ multiRoute.estimated_minutes }} 分钟</span>
          <span class="stat-pill">{{ multiRoute.strategy_label }}</span>
        </div>
        <p><strong>闭环停靠：</strong> {{ multiRoute.ordered_stop_names.join(" → ") }}</p>
      </div>
    </template>

    <div v-else class="status-card">
      {{ selectedCity }}当前支持城市地图浏览与精选地点查看，精细导航即将上线。
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { api } from "../api/client";
import RouteMap from "../components/RouteMap.vue";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const cities = ["北京", "上海", "广州", "深圳"];
const selectedCity = ref("北京");
const selectedSceneName = ref("BUPT_Main_Campus");
const strategy = ref("distance");
const transportMode = ref("walk");
const scenes = ref<any[]>([]);
const featuredDestinations = ref<any[]>([]);
const startCode = ref("");
const endCode = ref("");
const multiTargetCodes = ref<string[]>([]);
const singleRoute = ref<any | null>(null);
const multiRoute = ref<any | null>(null);
const selectedAlternativeStrategy = ref("");
const singleLoading = ref(false);
const multiLoading = ref(false);
const scene = ref<{ nodes: any[] } | null>(null);
const facilities = ref<any[]>([]);

const visibleScenes = computed(() => scenes.value.filter((item) => item.city === selectedCity.value));
const supportsRouting = computed(() => visibleScenes.value.find((item) => item.name === selectedSceneName.value)?.supports_routing ?? false);
const placeOptions = computed(() => ([...(scene.value?.nodes ?? []), ...facilities.value]));
const mapNodes = computed(() => {
  if (supportsRouting.value) return placeOptions.value;
  return featuredDestinations.value
    .filter((item) => item.city === selectedCity.value)
    .map((item) => ({
      code: item.source_id,
      name: item.name,
      latitude: item.latitude,
      longitude: item.longitude
    }));
});
const currentSceneMessage = computed(() =>
  supportsRouting.value ? `${mapNodes.value.length} 个点位可用于精细规划。` : `${mapNodes.value.length} 个精选地点可用于城市浏览。`
);
const suggestedNodes = computed(() => placeOptions.value.slice(0, 4));
const displayPathCodes = computed(() => {
  if (selectedAlternativeStrategy.value && singleRoute.value?.alternatives?.length) {
    const alternative = singleRoute.value.alternatives.find((item: any) => item.strategy === selectedAlternativeStrategy.value);
    if (alternative) return alternative.path_codes;
  }
  if (Array.isArray(multiRoute.value?.path_codes) && multiRoute.value.path_codes.length) return multiRoute.value.path_codes;
  return singleRoute.value?.path_codes ?? [];
});

const loadMeta = async () => {
  const [sceneRes, featuredRes] = await Promise.all([api.get("/map/scenes"), api.get("/destinations/featured")]);
  scenes.value = sceneRes.data;
  featuredDestinations.value = featuredRes.data;
};

const syncDefaultNodes = () => {
  startCode.value = placeOptions.value[0]?.code ?? "";
  endCode.value = placeOptions.value[1]?.code ?? startCode.value;
  multiTargetCodes.value = placeOptions.value.slice(1, 4).map((item) => item.code);
};

const handleCityChange = async () => {
  selectedSceneName.value = visibleScenes.value[0]?.name ?? "";
  await loadScene();
};

const loadScene = async () => {
  singleRoute.value = null;
  multiRoute.value = null;
  selectedAlternativeStrategy.value = "";
  if (!supportsRouting.value) {
    scene.value = { nodes: [] };
    facilities.value = [];
    return;
  }
  const { data } = await api.get(`/map/scenes/${selectedSceneName.value}`);
  scene.value = data.scene;
  facilities.value = data.facilities;
  syncDefaultNodes();
};

const planRoute = async () => {
  singleLoading.value = true;
  multiRoute.value = null;
  selectedAlternativeStrategy.value = "";
  try {
    const { data } = await api.post("/routes/single", {
      scene_name: selectedSceneName.value,
      start_code: startCode.value,
      end_code: endCode.value,
      strategy: strategy.value,
      transport_mode: transportMode.value
    });
    singleRoute.value = data;
  } finally {
    singleLoading.value = false;
  }
};

const planMultiRoute = async () => {
  multiLoading.value = true;
  singleRoute.value = null;
  selectedAlternativeStrategy.value = "";
  try {
    const { data } = await api.post("/routes/multi", {
      scene_name: selectedSceneName.value,
      start_code: startCode.value,
      target_codes: multiTargetCodes.value,
      strategy: strategy.value,
      transport_mode: transportMode.value
    });
    multiRoute.value = data;
  } finally {
    multiLoading.value = false;
  }
};

const saveCurrentRoute = async () => {
  const payload =
    selectedAlternativeStrategy.value && singleRoute.value?.alternatives?.length
      ? singleRoute.value.alternatives.find((item: any) => item.strategy === selectedAlternativeStrategy.value) || singleRoute.value
      : singleRoute.value;
  if (!payload) return;
  if (!auth.isLoggedIn) {
    auth.openAuthModal("login");
    return;
  }
  await auth.saveRouteFavorite({
    scene_name: selectedSceneName.value,
    strategy: payload.strategy,
    transport_mode: transportMode.value,
    path_codes: payload.path_codes,
    path_names: payload.path_names,
    total_distance_m: payload.total_distance_m,
    estimated_minutes: payload.estimated_minutes,
    explanation: payload.explanation
  });
};

onMounted(async () => {
  await loadMeta();
  selectedSceneName.value = visibleScenes.value[0]?.name ?? "";
  await loadScene();
});
</script>
