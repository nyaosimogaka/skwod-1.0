<template>

<SportForm
    @save="createSport"
/>

</template>

<script setup>

import {
    createSport
}
from "../../api/sportApi";

import SportForm
from "../../components/sports/SportForm.vue";

const createSportHandler =
    async (payload) => {

    await createSport(
        payload
    );
};

</script>