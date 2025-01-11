<template>
  <div id="app">
    <nav>
      <router-link :to="'/'">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
    <router-view />
  </div>
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
