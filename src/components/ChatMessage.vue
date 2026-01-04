<template>
  <div :class="['message', `message-${role}`]">
    <div class="message-content">
      <p>{{ content }}</p>
      <span class="message-time">{{ formattedTime }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  role: {
    type: String,
    default: 'user',
    validator: (value) => ['user', 'assistant'].includes(value)
  },
  timestamp: {
    type: [Date, String],
    default: () => new Date()
  }
});

const formattedTime = computed(() => {
  const date = props.timestamp instanceof Date ? props.timestamp : new Date(props.timestamp);
  return date.toLocaleTimeString();
});
</script>

<style scoped>
.message {
  display: flex;
  margin-bottom: 16px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-user {
  justify-content: flex-end;
}

.message-assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
  word-wrap: break-word;
}

.message-user .message-content {
  background-color: #007bff;
  color: white;
}

.message-assistant .message-content {
  background-color: #f1f3f5;
  color: #333;
}

.message-time {
  display: block;
  font-size: 12px;
  margin-top: 8px;
  opacity: 0.7;
}

.message-user .message-time {
  text-align: right;
}

.message-assistant .message-time {
  text-align: left;
}
</style>
