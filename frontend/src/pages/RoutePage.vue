<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-3xl card-elevated p-6">
      <h2 class="text-xl font-bold text-gray-900">地图导航</h2>
      <p class="text-sm text-gray-500 mt-1">
        按真实出行流程规划：先确定风格，再选起终点，最后查看分段导航与备选线路。
      </p>
    </div>
    <!-- Travel profiles + location -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="bg-white rounded-3xl card-elevated p-5">
        <h3 class="text-sm font-semibold text-gray-900 mb-3">出行风格</h3>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="profile in travelProfiles"
            :key="profile.key"
            type="button"
            class="text-left p-3 rounded-2xl border-0 shadow-md shadow-gray-200/50 transition-all duration-200"
            :class="
              activeProfileKey === profile.key
                ? 'bg-primary-50 shadow-md shadow-primary-500/10'
                : 'bg-white '
            "
            @click="applyTravelProfile(profile.key)"
          >
            <strong class="text-sm text-gray-900">{{ profile.label }}</strong>
            <p class="text-xs text-gray-500 mt-0.5">
              {{ profile.description }}
            </p>
          </button>
        </div>
      </div>
      <div class="bg-white rounded-3xl card-elevated p-5">
        <h3 class="text-sm font-semibold text-gray-900 mb-3">出发方式</h3>
        <div class="flex flex-wrap items-center justify-between gap-3">
          <label
            class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer"
          >
            <input
              v-model="useCurrentLocation"
              type="checkbox"
              class="w-4 h-4 rounded text-primary-600 focus:ring-primary-500"
            />
            使用当前位置自动匹配最近起点
          </label>
          <button
            type="button"
            :disabled="!supportsGeolocation || locating"
            class="btn-soft-chip"
            @click="captureCurrentLocation"
          >
            {{ locating ? "定位中..." : "刷新定位" }}
          </button>
        </div>
        <p class="text-xs text-gray-400 mt-2">{{ locationMessage }}</p>
      </div>
    </div>
    <!-- Filters -->
    <div class="flex flex-wrap gap-3">
      <select
        v-model="selectedCity"
        class="soft-control text-sm text-gray-700"
        @change="handleCityChange"
      >
        <option v-for="city in cities" :key="city" :value="city">
          {{ city }}
        </option>
      </select>
      <select
        v-model="selectedSceneName"
        class="soft-control text-sm text-gray-700"
        @change="loadScene"
      >
        <option
          v-for="scene in visibleScenes"
          :key="scene.name"
          :value="scene.name"
        >
          {{ scene.label }}
        </option>
      </select>
      <select v-model="strategy" class="soft-control text-sm text-gray-700">
        <option value="distance">最短距离</option>
        <option value="time">最快到达</option>
        <option value="congestion">避开拥堵</option>
        <option value="scenic">轻松逛/打卡优先</option>
      </select>
      <select
        v-model="transportMode"
        class="soft-control text-sm text-gray-700"
      >
        <option value="walk">步行</option>
        <option value="bike">骑行</option>
        <option value="shuttle">摆渡车</option>
        <option value="mixed">综合方式</option>
      </select>
    </div>
    <!-- Map -->
    <RouteMap
      :nodes="mapNodes"
      :path="displayPathCodes"
      :current-location="currentLocation"
    />
    <!-- Info cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div
        class="bg-white rounded-2xl border-0 shadow-md shadow-gray-200/50 p-4"
      >
        <h3 class="text-sm font-semibold text-gray-900">当前城市</h3>
        <p class="text-sm text-gray-600 mt-1">{{ selectedCity }}</p>
        <p class="text-xs text-gray-400 mt-0.5">{{ currentSceneMessage }}</p>
      </div>
      <div
        class="bg-white rounded-2xl border-0 shadow-md shadow-gray-200/50 p-4"
      >
        <h3 class="text-sm font-semibold text-gray-900">推荐起点/停靠</h3>
        <p
          v-for="item in suggestedNodes"
          :key="item.code"
          class="text-xs text-gray-500 mt-0.5"
        >
          {{ item.name }}
        </p>
      </div>
      <div
        class="bg-white rounded-2xl border-0 shadow-md shadow-gray-200/50 p-4"
      >
        <h3 class="text-sm font-semibold text-gray-900">导航摘要</h3>
        <p class="text-xs text-gray-500 mt-1">
          {{
            activeNavigationSummary ||
            "规划后会显示路段数量、总时长与策略说明。"
          }}
        </p>
      </div>
    </div>
    <div v-if="routeError" class="alert-soft-error">{{ routeError }}</div>
    <template v-if="supportsRouting">
      <!-- Single route form -->
      <div class="bg-white rounded-3xl card-elevated p-6">
        <h3 class="text-base font-semibold text-gray-900 mb-4">单点路线规划</h3>
        <form class="flex flex-wrap gap-3" @submit.prevent="planRoute">
          <select
            v-model="startCode"
            class="soft-control text-sm text-gray-700 min-w-[180px]"
            :disabled="useCurrentLocation"
          >
            <option
              v-for="node in placeOptions"
              :key="node.code"
              :value="node.code"
            >
              {{ node.name }}
            </option>
          </select>
          <select
            v-model="endCode"
            class="soft-control text-sm text-gray-700 min-w-[180px]"
          >
            <option
              v-for="node in placeOptions"
              :key="node.code"
              :value="node.code"
            >
              {{ node.name }}
            </option>
          </select>
          <button type="submit" class="btn-soft-primary text-sm">
            {{ singleLoading ? "规划中..." : "规划单点路线" }}
          </button>
        </form>
      </div>
      <!-- Single route result -->
      <div
        v-if="singleRoute"
        class="bg-white rounded-3xl card-elevated p-6 space-y-3"
      >
        <div class="flex items-center justify-between gap-4 flex-wrap">
          <h3 class="text-base font-semibold text-gray-900">
            {{ singleRoute.strategy_label }}
          </h3>
          <button class="btn-soft-chip-primary" @click="saveCurrentRoute">
            收藏当前路线
          </button>
        </div>
        <p class="text-sm text-gray-600">{{ singleRoute.explanation }}</p>
        <p v-if="singleRoute.resolved_start_name" class="text-xs text-gray-400">
          实际起点：{{ singleRoute.resolved_start_name }}
        </p>
        <div class="flex flex-wrap gap-2">
          <span
            class="text-xs px-3 py-1.5 rounded-full bg-primary-50 text-primary-700 font-medium"
            >{{ singleRoute.total_distance_m }} m</span
          >
          <span
            class="text-xs px-3 py-1.5 rounded-full bg-accent-50 text-accent-600 font-medium"
            >{{ singleRoute.estimated_minutes }} 分钟</span
          >
          <span
            class="text-xs px-3 py-1.5 rounded-full bg-gray-100 text-gray-600"
            >平均拥堵 {{ singleRoute.average_congestion }}</span
          >
        </div>
        <p class="text-sm text-gray-700">
          <strong>路线：</strong> {{ singleRoute.path_names.join(" →") }}
        </p>
      </div>
      <!-- Alternatives -->
      <section v-if="singleRoute?.alternatives?.length">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-base font-semibold text-gray-900">备选路线</h3>
          <span class="text-xs text-gray-400">点击卡片可切换地图高亮</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <article
            v-for="item in singleRoute.alternatives"
            :key="item.strategy"
            class="rounded-2xl border-0 shadow-md shadow-gray-200/50 p-4 cursor-pointer transition-all duration-200"
            :class="
              selectedAlternativeStrategy === item.strategy
                ? 'bg-primary-50 shadow-md shadow-primary-500/10 ring-1 ring-primary-200'
                : 'bg-white hover:shadow-lg '
            "
            @click="selectedAlternativeStrategy = item.strategy"
          >
            <h3 class="font-semibold text-gray-900 text-sm">
              {{ item.strategy_label }}
            </h3>
            <p class="text-xs text-gray-500 mt-1">{{ item.explanation }}</p>
            <p class="text-xs text-gray-400 mt-1">
              {{ item.total_distance_m }} m · {{ item.estimated_minutes }} 分钟
            </p>
          </article>
        </div>
      </section>
      <!-- Multi route form -->
      <div class="bg-white rounded-3xl card-elevated p-6">
        <h3 class="text-base font-semibold text-gray-900 mb-4">多点闭环规划</h3>
        <form
          class="flex flex-wrap gap-3 items-end"
          @submit.prevent="planMultiRoute"
        >
          <select
            v-model="multiTargetCodes"
            class="soft-control text-sm text-gray-700 min-w-[220px]"
            multiple
            size="4"
          >
            <option
              v-for="node in placeOptions"
              :key="node.code"
              :value="node.code"
            >
              {{ node.name }}
            </option>
          </select>
          <button type="submit" class="btn-soft-primary text-sm">
            {{ multiLoading ? "规划中..." : "规划多点闭环" }}
          </button>
        </form>
      </div>
      <!-- Multi route result -->
      <div
        v-if="multiRoute"
        class="bg-white rounded-3xl card-elevated p-6 space-y-3"
      >
        <h3 class="text-base font-semibold text-gray-900">
          {{ multiRoute.optimization_label }}
        </h3>
        <p class="text-sm text-gray-600">{{ multiRoute.explanation }}</p>
        <p v-if="multiRoute.resolved_start_name" class="text-xs text-gray-400">
          实际起点：{{ multiRoute.resolved_start_name }}
        </p>
        <div class="flex flex-wrap gap-2">
          <span
            class="text-xs px-3 py-1.5 rounded-full bg-primary-50 text-primary-700 font-medium"
            >{{ multiRoute.total_distance_m }} m</span
          >
          <span
            class="text-xs px-3 py-1.5 rounded-full bg-accent-50 text-accent-600 font-medium"
            >{{ multiRoute.estimated_minutes }} 分钟</span
          >
          <span
            class="text-xs px-3 py-1.5 rounded-full bg-gray-100 text-gray-600"
            >{{ multiRoute.strategy_label }}</span
          >
        </div>
        <p class="text-sm text-gray-700">
          <strong>闭环停靠：</strong>
          {{ multiRoute.ordered_stop_names.join(" →") }}
        </p>
      </div>
      <!-- Segments -->
      <section
        v-if="activeSegments.length"
        class="bg-white rounded-3xl card-elevated p-6"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-base font-semibold text-gray-900">分段导航</h3>
          <span class="text-xs text-gray-400">按顺序执行即可完成整段行程</span>
        </div>
        <ol class="space-y-3">
          <li
            v-for="segment in activeSegments"
            :key="`segment-${segment.index}-${segment.from_code}-${segment.to_code}`"
            class="flex gap-3 items-start p-3 rounded-2xl border-0 shadow-md shadow-gray-200/50 bg-gray-50/50"
          >
            <div
              class="w-7 h-7 flex-shrink-0 flex items-center justify-center rounded-full bg-gradient-to-br from-primary-500 to-accent-500 text-white text-xs font-bold shadow-md shadow-primary-500/20"
            >
              {{ segment.index }}
            </div>
            <div class="min-w-0">
              <strong class="text-sm text-gray-900"
                >{{ segment.from_name }} → {{ segment.to_name }}</strong
              >
              <p class="text-xs text-gray-600 mt-1">
                {{ segment.instruction }}
              </p>
              <p class="text-xs text-gray-400 mt-0.5">
                {{ segment.distance_m }} 米 ·
                {{ segment.estimated_minutes }} 分钟 · 累计
                {{ segment.cumulative_distance_m }} 米
              </p>
            </div>
          </li>
        </ol>
      </section>
    </template>
    <div
      v-else
      class="p-4 rounded-2xl bg-gray-50 border-0 shadow-md shadow-gray-200/50 text-sm text-gray-500"
    >
      {{ selectedCity }}当前支持城市地图浏览与精选地点查看，精细导航即将上线。
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { api } from "../api/client";
import RouteMap from "../components/RouteMap.vue";
import { useAuthStore } from "../stores/auth";
const auth = useAuthStore();
const cities = ["北京", "上海", "广州", "深圳"];
const selectedCity = ref("北京");
const selectedSceneName = ref("BUPT_Main_Campus");
const strategy = ref("distance");
const transportMode = ref("walk");
const activeProfileKey = ref("balanced");
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
const routeError = ref("");
const useCurrentLocation = ref(false);
const locating = ref(false);
const currentLocation = ref<{ latitude: number; longitude: number } | null>(
  null,
);
const supportsGeolocation =
  typeof navigator !== "undefined" && "geolocation" in navigator;
const travelProfiles = [
  {
    key: "balanced",
    label: "省时优先",
    description: "最快到达 + 综合交通",
    strategy: "time",
    transportMode: "mixed",
  },
  {
    key: "urgent",
    label: "赶路直达",
    description: "最短距离 + 骑行",
    strategy: "distance",
    transportMode: "bike",
  },
  {
    key: "relaxed",
    label: "轻松漫游",
    description: "打卡优先 + 步行",
    strategy: "scenic",
    transportMode: "walk",
  },
  {
    key: "stable",
    label: "避堵稳妥",
    description: "避拥堵 + 综合交通",
    strategy: "congestion",
    transportMode: "mixed",
  },
];
const visibleScenes = computed(() =>
  scenes.value.filter((item) => item.city === selectedCity.value),
);
const supportsRouting = computed(
  () =>
    visibleScenes.value.find((item) => item.name === selectedSceneName.value)
      ?.supports_routing ?? false,
);
const placeOptions = computed(() => [
  ...(scene.value?.nodes ?? []),
  ...facilities.value,
]);
const mapNodes = computed(() => {
  if (supportsRouting.value) return placeOptions.value;
  return featuredDestinations.value
    .filter((item) => item.city === selectedCity.value)
    .map((item) => ({
      code: item.source_id,
      name: item.name,
      latitude: item.latitude,
      longitude: item.longitude,
    }));
});
const currentSceneMessage = computed(() =>
  supportsRouting.value
    ? `${mapNodes.value.length} 个点位可用于精细规划。`
    : `${mapNodes.value.length} 个精选地点可用于城市浏览。`,
);
const suggestedNodes = computed(() => placeOptions.value.slice(0, 4));
const activeNavigationSummary = computed(() => {
  if (
    selectedAlternativeStrategy.value &&
    singleRoute.value?.alternatives?.length
  ) {
    const alternative = singleRoute.value.alternatives.find(
      (item: any) => item.strategy === selectedAlternativeStrategy.value,
    );
    if (alternative) return alternative.navigation_summary;
  }
  return (
    multiRoute.value?.navigation_summary ||
    singleRoute.value?.navigation_summary ||
    ""
  );
});
const activeSegments = computed(() => {
  if (
    selectedAlternativeStrategy.value &&
    singleRoute.value?.alternatives?.length
  ) {
    const alternative = singleRoute.value.alternatives.find(
      (item: any) => item.strategy === selectedAlternativeStrategy.value,
    );
    if (alternative?.segments?.length) return alternative.segments;
  }
  return multiRoute.value?.segments || singleRoute.value?.segments || [];
});
const locationMessage = computed(() => {
  if (!supportsGeolocation) return "当前浏览器不支持定位，可手动选择起点。";
  if (!useCurrentLocation.value)
    return "可手动选择起点，或开启当前位置自动匹配。";
  if (locating.value) return "正在获取当前位置...";
  if (currentLocation.value) {
    return `已定位：${currentLocation.value.latitude.toFixed(5)}, ${currentLocation.value.longitude.toFixed(5)}（规划时将自动匹配最近点）。`;
  }
  return "尚未定位，点击“刷新定位”后可自动匹配最近起点。";
});
const displayPathCodes = computed(() => {
  if (
    selectedAlternativeStrategy.value &&
    singleRoute.value?.alternatives?.length
  ) {
    const alternative = singleRoute.value.alternatives.find(
      (item: any) => item.strategy === selectedAlternativeStrategy.value,
    );
    if (alternative) return alternative.path_codes;
  }
  if (
    Array.isArray(multiRoute.value?.path_codes) &&
    multiRoute.value.path_codes.length
  )
    return multiRoute.value.path_codes;
  return singleRoute.value?.path_codes ?? [];
});
const loadMeta = async () => {
  const [sceneRes, featuredRes] = await Promise.all([
    api.get("/map/scenes"),
    api.get("/destinations/featured"),
  ]);
  scenes.value = sceneRes.data;
  featuredDestinations.value = featuredRes.data;
};
const syncDefaultNodes = () => {
  startCode.value = placeOptions.value[0]?.code ?? "";
  endCode.value = placeOptions.value[1]?.code ?? startCode.value;
  multiTargetCodes.value = placeOptions.value
    .slice(1, 4)
    .map((item) => item.code);
};
const applyTravelProfile = (profileKey: string) => {
  const profile = travelProfiles.find((item) => item.key === profileKey);
  if (!profile) return;
  activeProfileKey.value = profile.key;
  strategy.value = profile.strategy;
  transportMode.value = profile.transportMode;
};
const captureCurrentLocation = async () => {
  if (!supportsGeolocation) return;
  locating.value = true;
  try {
    const coordinates = await new Promise<{
      latitude: number;
      longitude: number;
    }>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        reject,
        { enableHighAccuracy: true, timeout: 5000 },
      );
    });
    currentLocation.value = coordinates;
  } catch {
    routeError.value = "定位失败，请检查浏览器定位权限或改用手动起点。";
  } finally {
    locating.value = false;
  }
};
const locationPayload = () => {
  if (useCurrentLocation.value && currentLocation.value) {
    return {
      prefer_nearest_start: true,
      start_latitude: currentLocation.value.latitude,
      start_longitude: currentLocation.value.longitude,
    };
  }
  return {
    prefer_nearest_start: false,
    start_latitude: null,
    start_longitude: null,
  };
};
const ensureLocationReady = async () => {
  if (!useCurrentLocation.value) return true;
  if (currentLocation.value) return true;
  await captureCurrentLocation();
  return Boolean(currentLocation.value);
};
const handleCityChange = async () => {
  routeError.value = "";
  selectedSceneName.value = visibleScenes.value[0]?.name ?? "";
  await loadScene();
};
const loadScene = async () => {
  routeError.value = "";
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
  routeError.value = "";
  const canRoute = await ensureLocationReady();
  if (!canRoute && useCurrentLocation.value) {
    routeError.value = "无法获取当前位置，请改为手动起点或重试定位。";
    return;
  }
  singleLoading.value = true;
  multiRoute.value = null;
  selectedAlternativeStrategy.value = "";
  try {
    const { data } = await api.post("/routes/single", {
      scene_name: selectedSceneName.value,
      start_code: startCode.value,
      end_code: endCode.value,
      strategy: strategy.value,
      transport_mode: transportMode.value,
      ...locationPayload(),
    });
    singleRoute.value = data;
  } catch (error: any) {
    routeError.value =
      error?.response?.data?.detail || "路线规划失败，请稍后重试。";
  } finally {
    singleLoading.value = false;
  }
};
const planMultiRoute = async () => {
  routeError.value = "";
  const canRoute = await ensureLocationReady();
  if (!canRoute && useCurrentLocation.value) {
    routeError.value = "无法获取当前位置，请改为手动起点或重试定位。";
    return;
  }
  multiLoading.value = true;
  singleRoute.value = null;
  selectedAlternativeStrategy.value = "";
  try {
    const { data } = await api.post("/routes/multi", {
      scene_name: selectedSceneName.value,
      start_code: startCode.value,
      target_codes: multiTargetCodes.value,
      strategy: strategy.value,
      transport_mode: transportMode.value,
      ...locationPayload(),
    });
    multiRoute.value = data;
  } catch (error: any) {
    routeError.value =
      error?.response?.data?.detail || "多点路线规划失败，请稍后重试。";
  } finally {
    multiLoading.value = false;
  }
};
const saveCurrentRoute = async () => {
  const payload =
    selectedAlternativeStrategy.value && singleRoute.value?.alternatives?.length
      ? singleRoute.value.alternatives.find(
          (item: any) => item.strategy === selectedAlternativeStrategy.value,
        ) || singleRoute.value
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
    explanation: payload.explanation,
  });
};
onMounted(async () => {
  applyTravelProfile("balanced");
  await loadMeta();
  selectedSceneName.value = visibleScenes.value[0]?.name ?? "";
  await loadScene();
});
watch(useCurrentLocation, async (enabled) => {
  if (enabled && !currentLocation.value) {
    await captureCurrentLocation();
  }
});
</script>
