<script setup lang="ts">
import { defineComponent } from 'vue';
import StockNews from './components/StockNews.vue';

defineComponent({
  name: 'App',
  components: {
    StockNews,
  },
});

</script>

<template>
  <div id="app">
    <StockNews />
  </div>
</template>

<style scoped>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 20px;
}
</style>
