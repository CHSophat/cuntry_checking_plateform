<template>
  <div class="home-page">
    <h1>Welcome to AI Frontend Vue</h1>
    <p>A modern Vue.js application for AI-powered interactions.</p>
    
    <div class="features">
      <div class="feature-card">
        <h3>Interactive AI Chat</h3>
        <p>Chat with AI powered by local JSON Server</p>
        <RouterLink to="/ai-tool">
          <Button label="Try AI Tool" variant="primary" />
        </RouterLink>
      </div>
      
      <div class="feature-card">
        <h3>Modern Vue 3</h3>
        <p>Built with Vue 3 Composition API</p>
      </div>
      
      <div class="feature-card">
        <h3>Clean Architecture</h3>
        <p>Well-organized project structure with composables, stores, and services</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import Button from '../components/Button.vue';
</script>

<style scoped>
.home-page {
  text-align: center;
}

.home-page h1 {
  font-size: 48px;
  margin-bottom: 1rem;
  color: #333;
}

.home-page p {
  font-size: 18px;
  color: #666;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.feature-card h3 {
  color: #007bff;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  margin-bottom: 1.5rem;
}

.feature-card a {
  text-decoration: none;
}
</style>
