<template>
  <PanelCard title="智能体协作展示" subtitle="课程要求中的任务分解、文档辅助和协作流程">
    <button class="primary-btn" @click="load">加载智能体说明</button>
    <pre>{{ JSON.stringify(agents, null, 2) }}</pre>
  </PanelCard>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { api } from "../api/client";
import PanelCard from "../components/PanelCard.vue";

const agents = ref<Record<string, unknown>>({});

const load = async () => {
  const { data } = await api.get("/agents");
  agents.value = data;
};
</script>
