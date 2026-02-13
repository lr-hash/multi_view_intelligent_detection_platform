<template>
  <div class="login-page">
    <div class="background-overlay"></div>
    
    <div class="login-wrapper animate-fade-in">
      <div class="login-brand">
        <div class="logo">
          <svg style="width:48px;height:48px" viewBox="0 0 24 24"><path fill="currentColor" d="M12,2L4.5,20.29L5.21,21L12,18L18.79,21L19.5,20.29L12,2Z" /></svg>
        </div>
        <h1>多视域智能侦测平台</h1>
        <p>Industrial Intelligent Detection System</p>
      </div>

      <div class="login-card">
        <h2>用户登录</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-item">
            <label>账号</label>
            <div class="input-with-icon">
              <span class="icon">👤</span>
              <input type="text" v-model="username" placeholder="请输入用户名" required>
            </div>
          </div>
          
          <div class="form-item">
            <label>密码</label>
            <div class="input-with-icon">
              <span class="icon">🔒</span>
              <input type="password" v-model="password" placeholder="请输入密码" required>
            </div>
          </div>

          <div v-if="errorMessage" class="error-box">
            <span class="error-icon">⚠️</span>
            {{ errorMessage }}
          </div>

          <button type="submit" :disabled="isSubmitting" class="login-btn">
            <span v-if="!isSubmitting">登 录</span>
            <span v-else class="loading-dots">正在验证...</span>
          </button>
        </form>
      </div>
      
      <div class="login-footer">
        © 2026 煤矿安全智能监测系统 · 版权所有
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const username = ref('admin');
const password = ref('admin123');
const errorMessage = ref('');
const isSubmitting = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async () => {
  isSubmitting.value = true;
  errorMessage.value = '';
  try {
    await authStore.login(username.value, password.value);
    router.push('/');
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '身份验证失败，请检查账号密码';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.login-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #020617; /* Deep space dark */
  overflow: hidden;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.1) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(16, 185, 129, 0.1) 0%, transparent 40%);
  z-index: 1;
}

.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 440px;
  padding: 20px;
}

.login-brand {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  color: #3b82f6;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.5));
}

.login-brand h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 2px;
  margin: 0;
}

.login-brand p {
  color: #64748b;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.login-card {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.login-card h2 {
  font-size: 1.4rem;
  color: #f1f5f9;
  margin-bottom: 2rem;
  text-align: center;
}

.form-item {
  margin-bottom: 1.5rem;
}

.form-item label {
  display: block;
  font-size: 0.85rem;
  color: #94a3b8;
  margin-bottom: 0.6rem;
  font-weight: 500;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon .icon {
  position: absolute;
  left: 12px;
  font-size: 1.1rem;
}

.input-with-icon input {
  width: 100%;
  background: rgba(2, 6, 23, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 0.8rem 1rem 0.8rem 2.5rem;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s;
}

.input-with-icon input:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(2, 6, 23, 0.8);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.error-box {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
  padding: 0.8rem;
  border-radius: 8px;
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-btn {
  width: 100%;
  background: linear-gradient(to right, #3b82f6, #2563eb);
  color: #white;
  border: none;
  padding: 1rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(59, 130, 246, 0.4);
  filter: brightness(1.1);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 2rem;
  font-size: 0.8rem;
  color: #475569;
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
