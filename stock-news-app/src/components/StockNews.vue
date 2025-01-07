<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

export default defineComponent({
    data() {
        return {
            news: [] as Array<{ title: string; time: string; link: string; image: string; }>,
            loading: true
        };
    },

    methods: {
        fetchNews() {
            axios
                .get('http://localhost:8000/stock-news')
                .then((response) => {
                    if (response.data.status === 'success') {
                        this.news = response.data.data;
                    } else {
                        console.error('Failed to fetch news');
                    }
                    this.loading = false;
                })
                .catch((error) => {
                    console.error('Failed to fetch news', error);
                    this.loading = false;
                });
        },
    },

    watch: {
        news: {
            handler(newNews) {
                if (newNews.length) {
                    console.log('Stock news updated:', newNews);
                }
            },
            deep: true
        }
    },

    mounted() {
        this.fetchNews();
        setInterval(() => {
            this.fetchNews();
        }, 30000);
    },
});
</script>

<template>
    <div class="news-list">
    <h1>Latest Indonesia Stock News</h1>
    <div v-if="loading">Loading...</div>
    <ul v-if="!loading && news.length">
      <li v-for="(article, index) in news" :key="index" class="news-item">
        <a :href="article.link" target="_blank">
          <div class="news-header">
            <img v-if="article.image" :src="article.image" alt="news image" class="news-image" />
            <h3>{{ article.title }}</h3>
          </div>
        </a>
        <p>{{ article.time }}</p>
      </li>
    </ul>
    <div v-if="!loading && !news.length">No news available.</div>
  </div>
</template>

<style scoped>
.news-list {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.news-list h1 {
  text-align: center;
}

.news-list ul {
  list-style-type: none;
  padding: 0;
}

.news-list .news-item {
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
  padding-bottom: 10px;
}

.news-list .news-header {
  display: flex;
  align-items: center;
}

.news-list .news-image {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  object-fit: cover;
}

.news-list a {
  text-decoration: none;
  color: #007bff;
}

.news-list h3 {
  margin: 0;
  font-size: 18px;
}

.news-list p {
  font-size: 14px;
  color: #888;
}
</style>