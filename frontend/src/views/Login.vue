<template>
  <div class="card" style="max-width: 400px; margin: 50px auto;">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>Email</label>
        <input type="text" v-model="email" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="password" required />
      </div>
      <p v-if="error" style="color: #ff4c4c;">{{ error }}</p>
      <button type="submit" style="width: 100%;">Login</button>
    </form>
    <p style="text-align: center; margin-top: 15px;">
      Don't have an account? <router-link to="/register" style="color: var(--primary-red);">Register here</router-link>
    </p>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

export default {
  setup() {
    const email = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();

    const handleLogin = async () => {
      try {
        const response = await api.post('/auth/login', {
          email: email.value,
          password: password.value
        });
        localStorage.setItem('token', response.data.access_token);
        router.push('/');
      } catch (err) {
        error.value = err.response?.data?.msg || 'Login failed';
      }
    };

    return { email, password, error, handleLogin };
  }
}
</script>
