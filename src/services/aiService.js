import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const aiService = {
  /**
   * Send a chat message to the AI
   * @param {string} message - The user's message
   * @returns {Promise<string>} The AI's response
   */
  async chat(message) {
    try {
      // For now, we'll simulate a response
      // Replace with actual API call when backend is ready
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(`Echo: ${message}`);
        }, 500);
      });

      // Uncomment when API is ready:
      // const response = await apiClient.post('/chat', { message });
      // return response.data.reply;
    } catch (error) {
      console.error('AI Service Error:', error);
      throw new Error(error.response?.data?.message || error.message);
    }
  },

  /**
   * Get chat history
   * @returns {Promise<Array>} Array of messages
   */
  async getChatHistory() {
    try {
      const response = await apiClient.get('/search_examples');
      return response.data;
    } catch (error) {
      console.error('Error fetching chat history:', error);
      throw error;
    }
  },

  /**

  /**
   * Search locations by name
   * @param {string} query - Search query
   * @returns {Promise<Array>} Filtered locations
   */
  async searchLocations(query) {
    try {
      const response = await apiClient.get('/vietnam_locations', {
        params: {
          q: query
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error searching locations:', error);
      throw error;
    }
  }
};
