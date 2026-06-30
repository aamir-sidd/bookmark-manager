<template>
  <div class="card" style="max-width: 400px; margin: 50px auto;">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>Email</label>
        <input type="text" v-model="email" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="password" required />
      </div>
      <p v-if="error" style="color: #ff4c4c;">{{ error }}</p>
      <p v-if="success" style="color: #28a745;">{{ success }}</p>
      <button type="submit" style="width: 100%;">Register</button>
    </form>
    <p style="text-align: center; margin-top: 15px;">
      Already have an account? <router-link to="/login" style="color: var(--primary-red);">Login here</router-link>
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
    const success = ref('');
    const router = useRouter();

    const handleRegister = async () => {
      error.value = '';
      success.value = '';
      try {
        await api.post('/auth/register', {
          email: email.value,
          password: password.value
        });
        success.value = 'Registration successful! Redirecting to login...';
        setTimeout(() => {
          router.push('/login');
        }, 1500);
      } catch (err) {
        error.value = err.response?.data?.msg || 'Registration failed';
      }
    };

    return { email, password, error, success, handleRegister };
  }
}
</script>
