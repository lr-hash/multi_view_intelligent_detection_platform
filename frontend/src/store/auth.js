import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null, // User info can be stored here after fetching
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const response = await api.login(username, password);
      const token = response.data.token;
      if (token) {
        this.token = token;
        localStorage.setItem('token', token);
        // The interceptor in api.js will now automatically use this token
        
        // You might want to fetch user details here and store them
        // this.user = await api.getUserProfile();
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      // After this, the router guard will automatically redirect to /login
      // on the next route navigation. We can also force a reload to do it immediately.
      window.location.reload();
    },
  },
});

