<template>
  <PanelCard title="数据导入与状态" subtitle="查看当前演示数据和导入目录">
    <button class="primary-btn" @click="load">刷新状态</button>
    <pre>{{ JSON.stringify(status, null, 2) }}</pre>
  </PanelCard>
</template>

<script setup lang="ts">
import { ref } from "vue";

import { api } from "../api/client";
import PanelCard from "../components/PanelCard.vue";

const status = ref<Record<string, unknown>>({});

const load = async () => {
  const { data } = await api.get("/admin/import/status");
  status.value = data;
};
</script>
