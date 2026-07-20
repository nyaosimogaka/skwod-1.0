<template>

<v-form>

<v-text-field
    v-model="sport_name"
    label="Sport Name"
/>

<v-btn
    @click="save">

    Save

</v-btn>

</v-form>

</template>

<script setup>

import { ref }
from "vue";

const sport_name = ref("");

const emit =
    defineEmits([
        "save"
    ]);

const save = () => {

    emit(
        "save",
        {
            sport_name:
                sport_name.value
        }
    );
};

</script>