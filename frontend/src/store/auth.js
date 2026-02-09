import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      try {
        const response = await api.login(username, password);
        const { token, user } = response.data;
        if (token) {
          this.token = token;
          this.user = user;
          localStorage.setItem('token', token);
          localStorage.setItem('user', JSON.stringify(user));
          return true;
        }
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
      return false;
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.reload();
    },
  },
});

