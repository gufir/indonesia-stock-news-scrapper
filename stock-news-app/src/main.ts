import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';


const app = createApp(App);

// Use the router
app.use(router);

app.mount('#app');
