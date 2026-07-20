<template>

<v-data-table
    :items="sports"
    :headers="headers">

</v-data-table>

</template>

<script setup>

const props = defineProps({
    sports: Array
});

const headers = [
    {
        title: "Sport",
        key: "sport_name"
    }
];

</script>