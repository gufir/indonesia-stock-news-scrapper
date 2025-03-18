<script lang="ts">
import axios from 'axios';
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      news: [] as Array<{ title: string; time: string; link: string; image: string }>,
      loading: true,
      currentPage: 1,
      pageSize: 5,
    };
  },

  computed: {
    paginatedNews(): Array<{ title: string; time: string; link: string; image: string }> {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.news.slice(start, end);
    },
    totalPages(): number {
      return Math.ceil(this.news.length / this.pageSize);
    },
  },

  methods: {
    async fetchNews() {
      this.loading = true;
      try {
        const [kontanResponse, bisnisResponse] = await Promise.all([
          axios.get('http://localhost:8000/stock/kontan'),
          axios.get('http://localhost:8000/stock/bisnis')
        ]);

        let combinedNews = [...kontanResponse.data, ...bisnisResponse.data];
        combinedNews = combinedNews
          .map(article => ({
            ...article,
            time: new Date(article.time)
          }))
          .sort((a, b) => b.time.getTime() - a.time.getTime());

        this.news = combinedNews;
      } catch (error) {
        console.error('Failed to fetch news', error);
      } finally {
        this.loading = false;
      }
    },
    
    goToPage(page: number): void {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
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
    }, 300000);
  },
});
</script>

<template>
    <div class="news-list">
    <h1>Latest Indonesia Stock News</h1>
    <div v-if="loading">Loading...</div>
    <ul v-if="!loading && news.length">
      <li v-for="(article, index) in paginatedNews" :key="index" class="news-item">
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

    <!-- Pagination Control-->
    <div v-if="!loading && totalPages > 1" class="pagination">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
    </div>
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

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.pagination button {
    margin: 0 5px;
    padding: 5px 10px;
    font-size: 14px;
    cursor: pointer;
    border: 1px solid #007bff;
    background-color: #fff;
    color: #007bff;
    border-radius: 5px;
    outline: none;
}

.pagination button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}

.pagination span {
    margin: 0 10px;
}
</style>