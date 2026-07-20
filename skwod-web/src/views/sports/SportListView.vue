<template>

<v-container>

<v-btn
    @click="loadSports">

    Refresh

</v-btn>

<SportTable
    :sports="sports"
/>

</v-container>

</template>

<script setup>

import { ref, onMounted }
from "vue";

import { getSports }
from "../../api/sportApi";

import SportTable
from "../../components/sports/SportTable.vue";

const sports = ref([]);

const loadSports = async () => {

    const response =
        await getSports();

    sports.value =
        response.data;
};

onMounted(loadSports);

</script>