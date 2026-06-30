<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
      <h2 style="margin: 0;">My Bookmarks</h2>
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search title or category..." 
        style="width: 250px; margin-bottom: 0;"
      />
    </div>
    
    <div class="card">
      <h3 style="margin-top: 0;">{{ editingId ? 'Edit Bookmark' : 'Add New Bookmark' }}</h3>
      <form @submit.prevent="saveBookmark">
        <div class="form-group">
          <label>Title *</label>
          <input type="text" v-model="form.title" required />
        </div>
        <div class="form-group">
          <label>URL *</label>
          <input type="url" v-model="form.url" required />
        </div>
        <div class="form-group">
          <label>Category</label>
          <input type="text" v-model="form.category" />
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="form.description"></textarea>
        </div>
        <button type="submit">{{ editingId ? 'Update' : 'Add' }} Bookmark</button>
        <button type="button" class="btn-secondary" style="margin-left: 10px;" v-if="editingId" @click="cancelEdit">Cancel</button>
      </form>
    </div>

    <ul class="bookmark-list">
      <li v-for="bookmark in filteredBookmarks" :key="bookmark.id" class="bookmark-item">
        <div>
          <a :href="bookmark.url" target="_blank">{{ bookmark.title }}</a>
          <p style="margin: 5px 0 0; font-size: 0.9em; color: var(--text-gray);">
            <span v-if="bookmark.category">[{{ bookmark.category }}] </span>
            {{ bookmark.description }}
          </p>
        </div>
        <div class="bookmark-actions">
          <button class="btn-secondary" @click="editBookmark(bookmark)">Edit</button>
          <button class="btn-danger" @click="deleteBookmark(bookmark.id)">Delete</button>
        </div>
      </li>
      <li v-if="filteredBookmarks.length === 0" style="text-align: center; color: var(--text-gray); padding: 20px;">
        <span v-if="bookmarks.length === 0">No bookmarks yet. Add one above!</span>
        <span v-else>No bookmarks match your search.</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import api from '../api';

export default {
  setup() {
    const bookmarks = ref([]);
    const editingId = ref(null);
    const searchQuery = ref('');
    const form = ref({
      title: '',
      url: '',
      category: '',
      description: ''
    });

    const fetchBookmarks = async () => {
      try {
        const response = await api.get('/bookmarks/');
        bookmarks.value = response.data;
      } catch (error) {
        console.error("Error fetching bookmarks", error);
      }
    };

    const saveBookmark = async () => {
      try {
        if (editingId.value) {
          await api.put(`/bookmarks/${editingId.value}`, form.value);
        } else {
          await api.post('/bookmarks/', form.value);
        }
        cancelEdit();
        fetchBookmarks();
      } catch (error) {
        console.error("Error saving bookmark", error);
        alert(error.response?.data?.msg || "Error saving bookmark");
      }
    };

    const editBookmark = (bookmark) => {
      editingId.value = bookmark.id;
      form.value = {
        title: bookmark.title,
        url: bookmark.url,
        category: bookmark.category || '',
        description: bookmark.description || ''
      };
      window.scrollTo(0, 0);
    };

    const cancelEdit = () => {
      editingId.value = null;
      form.value = { title: '', url: '', category: '', description: '' };
    };

    const deleteBookmark = async (id) => {
      if (confirm('Are you sure you want to delete this bookmark?')) {
        try {
          await api.delete(`/bookmarks/${id}`);
          fetchBookmarks();
        } catch (error) {
          console.error("Error deleting bookmark", error);
        }
      }
    };

    const filteredBookmarks = computed(() => {
      const query = searchQuery.value.toLowerCase();
      if (!query) return bookmarks.value;
      
      return bookmarks.value.filter(b => {
        const titleMatch = b.title && b.title.toLowerCase().includes(query);
        const catMatch = b.category && b.category.toLowerCase().includes(query);
        return titleMatch || catMatch;
      });
    });

    onMounted(() => {
      fetchBookmarks();
    });

    return {
      bookmarks,
      editingId,
      form,
      searchQuery,
      filteredBookmarks,
      saveBookmark,
      editBookmark,
      cancelEdit,
      deleteBookmark
    };
  }
}
</script>
