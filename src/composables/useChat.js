import { ref } from 'vue';
import { useAiStore } from '../store/aiStore';
import { aiService } from '../services/aiService';

export const useChat = () => {
  const aiStore = useAiStore();
  const isProcessing = ref(false);

  const sendMessage = async (userMessage) => {
    try {
      aiStore.setLoading(true);
      aiStore.clearError();

      // Add user message to store
      aiStore.addMessage(userMessage, 'user');

      // Call AI service
      const response = await aiService.chat(userMessage);

      // Add AI response to store
      aiStore.addMessage(response, 'assistant');

      return response;
    } catch (error) {
      console.error('Error in useChat:', error);
      aiStore.setError(error.message || 'Failed to get AI response');
      throw error;
    } finally {
      aiStore.setLoading(false);
    }
  };

  const clearChat = () => {
    aiStore.clearMessages();
  };

  return {
    sendMessage,
    clearChat,
    messages: aiStore.messages,
    isLoading: aiStore.isLoading,
    error: aiStore.error
  };
};
