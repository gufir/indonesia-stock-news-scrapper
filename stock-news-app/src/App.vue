<script lang="ts">
  import HeaderApp from './components/HeaderApp.vue'
  import { defineComponent } from "vue";
  export default defineComponent({
  name: "App",
  components: {
    HeaderApp,
  },
});
</script>

<template>
  <div id="app">
    <HeaderApp/>
  </div>
  <router-view />
</template>

<style scoped>
nav {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}
nav a {
  text-decoration: none;
  color: #007bff;
}
nav a.router-link-active {
  font-weight: bold;
  color: #0056b3;
}
</style>
