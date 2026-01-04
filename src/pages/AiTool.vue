<template>
  <div class="ai-tool-page">
    <h1>AI Chat Tool</h1>
    
    <div class="chat-container">
      <div class="chat-messages">
        <template v-if="messages.length === 0">
          <p class="empty-message">Start a conversation with AI...</p>
        </template>
        <template v-else>
          <ChatMessage
            v-for="(message, index) in messages"
            :key="index"
            :content="message.content"
            :role="message.role"
            :timestamp="message.timestamp"
          />
        </template>
        <Loader v-if="loading" message="AI is thinking..." />
      </div>

      <div class="chat-input-section">
        <input
          v-model="userInput"
          type="text"
          placeholder="Type your message..."
          @keyup.enter="sendMessage"
          class="chat-input"
          :disabled="loading"
        />
        <Button
          label="Send"
          variant="primary"
          :disabled="loading || !userInput.trim()"
          @click="sendMessage"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ChatMessage from '../components/ChatMessage.vue';
import Loader from '../components/Loader.vue';
import Button from '../components/Button.vue';
import { useChat } from '../composables/useChat';

const messages = ref([]);
const userInput = ref('');
const loading = ref(false);

const { sendMessage: sendChatMessage } = useChat();

const sendMessage = async () => {
  if (!userInput.value.trim()) return;

  // Add user message
  messages.value.push({
    content: userInput.value,
    role: 'user',
    timestamp: new Date()
  });

  const input = userInput.value;
  userInput.value = '';
  loading.value = true;

  try {
    // Simulate AI response (replace with actual API call)
    const response = await sendChatMessage(input);
    messages.value.push({
      content: response || 'I understood your message, but I need more context to respond properly.',
      role: 'assistant',
      timestamp: new Date()
    });
  } catch (error) {
    console.error('Error sending message:', error);
    messages.value.push({
      content: 'Sorry, I encountered an error. Please try again.',
      role: 'assistant',
      timestamp: new Date()
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.ai-tool-page {
  max-width: 800px;
  margin: 0 auto;
  height: calc(100vh - 300px);
  display: flex;
  flex-direction: column;
}

.ai-tool-page h1 {
  color: #333;
  margin-bottom: 2rem;
  font-size: 32px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.empty-message {
  text-align: center;
  color: #999;
  margin: auto;
}

.chat-input-section {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
  background: #f8f9fa;
}

.chat-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

.chat-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.chat-input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}
</style>
