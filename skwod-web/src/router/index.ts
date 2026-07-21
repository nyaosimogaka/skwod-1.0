import { createRouter, createWebHistory } from "vue-router";

import AppLayout from "../layouts/AppLayout.vue";

import DashboardView from "../views/DashboardView.vue";
import SportListView from "../views/sports/SportListView.vue";

const routes = [
  {
    path: "/",
    component: AppLayout,
    children: [
      {
        path: "",
        component: DashboardView,
      },
      {
        path: "sports",
        component: SportListView,
      },
    ],
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});