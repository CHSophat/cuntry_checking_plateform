import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAiStore = defineStore('ai', () => {
  const messages = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const messageCount = computed(() => messages.value.length);

  const addMessage = (content, role = 'user') => {
    messages.value.push({
      id: Date.now(),
      content,
      role,
      timestamp: new Date()
    });
  };

  const setLoading = (loading) => {
    isLoading.value = loading;
  };

  const setError = (errorMessage) => {
    error.value = errorMessage;
  };

  const clearMessages = () => {
    messages.value = [];
    error.value = null;
  };

  const clearError = () => {
    error.value = null;
  };

  return {
    messages,
    isLoading,
    error,
    messageCount,
    addMessage,
    setLoading,
    setError,
    clearMessages,
    clearError
  };
});
