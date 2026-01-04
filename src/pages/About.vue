<template>
  <div class="about-page">
    <h1>About AI Frontend Vue</h1>
    
    <div class="about-content">
      <section>
        <h2>Project Overview</h2>
        <p>
          AI Frontend Vue is a modern web application built with Vue.js 3 that demonstrates
          best practices for frontend development including component composition, state management,
          and service integration.
        </p>
      </section>

      <section>
        <h2>Features</h2>
        <ul>
          <li>Interactive AI Chat Interface</li>
          <li>Real-time Message Updates</li>
          <li>Clean Component Architecture</li>
          <li>Pinia State Management</li>
          <li>Vue Router for Navigation</li>
          <li>Composable Hooks for Reusability</li>
        </ul>
      </section>

      <section>
        <h2>Technology Stack</h2>
        <ul>
          <li>Vue.js 3</li>
          <li>Vite</li>
          <li>Pinia</li>
          <li>Vue Router</li>
          <li>JSON Server (Mock API)</li>
        </ul>
      </section>

      <section>
        <h2>Project Structure</h2>
        <p>
          The project follows a modular architecture with clear separation of concerns:
        </p>
        <ul>
          <li><strong>Components:</strong> Reusable UI components</li>
          <li><strong>Pages:</strong> Page-level components</li>
          <li><strong>Layouts:</strong> Layout wrappers</li>
          <li><strong>Store:</strong> Pinia store for state management</li>
          <li><strong>Services:</strong> API service integration</li>
          <li><strong>Composables:</strong> Reusable logic hooks</li>
          <li><strong>Utils:</strong> Utility functions and helpers</li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.about-page {
  max-width: 900px;
  margin: 0 auto;
}

.about-page h1 {
  color: #333;
  margin-bottom: 2rem;
  font-size: 36px;
}

.about-content section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #dee2e6;
}

.about-content section:last-child {
  border-bottom: none;
}

.about-content h2 {
  color: #007bff;
  margin-bottom: 1rem;
  font-size: 24px;
}

.about-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.about-content ul {
  margin-left: 2rem;
  color: #666;
}

.about-content li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}
</style>
