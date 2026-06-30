<template>
  <div id="app">
    <nav v-if="isAuthenticated">
      <div>
        <strong>Bookmark Manager</strong>
      </div>
      <div>
        <router-link to="/">Dashboard</router-link>
        <a href="#" @click.prevent="logout">Logout</a>
      </div>
    </nav>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    const isAuthenticated = computed(() => {
      route.name; 
      return !!localStorage.getItem('token');
    });

    const logout = () => {
      localStorage.removeItem('token');
      router.push('/login');
    };

    return {
      isAuthenticated,
      logout
    };
  }
}
</script>
