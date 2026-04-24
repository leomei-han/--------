import { createRouter, createWebHistory } from "vue-router";

import DestinationPage from "../pages/DestinationPage.vue";
import DiaryPage from "../pages/DiaryPage.vue";
import FacilityPage from "../pages/FacilityPage.vue";
import FoodPage from "../pages/FoodPage.vue";
import HomePage from "../pages/HomePage.vue";
import RoutePage from "../pages/RoutePage.vue";
import SearchPage from "../pages/SearchPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomePage },
    { path: "/destinations", component: DestinationPage },
    { path: "/search", component: SearchPage },
    { path: "/routes", component: RoutePage },
    { path: "/facilities", component: FacilityPage },
    { path: "/foods", component: FoodPage },
    { path: "/diaries", component: DiaryPage },
  ],
});

export default router;
