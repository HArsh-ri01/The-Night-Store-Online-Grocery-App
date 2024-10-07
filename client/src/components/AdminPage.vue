<template>
    <div>
        <admin-navbar />
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="mb-0">Welcome to the Admin Page, {{ username }}!</h2>
            <router-link to="/add-category" class="btn btn-primary">Add Category</router-link>
        </div>
        <div class="container mt-4">
            <!-- Display categories as card forms -->
            <div v-if="categories.length > 0" class=" cardgrid row">
                <div v-for="category in categories" :key="category.id" class="card">
                    <img :src="`http://127.0.0.1:5000/Uploads/${category.image_path}`" alt="Default Image"
                        class="card-img-top" style="height: 250px; object-fit: cover;" />
                    <div class="card-body">
                        <h3 class="card-title">{{ category.name }}</h3>
                        <div class="category-buttons">
                            <router-link :to="'/edit-category/' + category.id" class="btn btn-secondary">Edit</router-link>
                            <button @click="toggleCategoryStatus(category)" class="btn"
                                :class="{ 'btn-success': category.status === 'Inactive', 'btn-danger': category.status === 'Active' }">
                                {{ category.status === 'Active' ? 'Disable' : 'Enable' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <p>No categories available.</p>
            </div>
        </div>
    </div>
</template>
  
<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
import axios from 'axios';

export default {
    name: 'AdminPage',
    data() {
        return {
            username: '',
            categories: [], // Array to store categories
        };
    },
    components: {
        AdminNavbar
    },
    mounted() {
        // Fetch the username from session storage or wherever you store it
        this.username = sessionStorage.getItem('username') || 'Admin';

        // Fetch categories from the backend
        this.fetchCategories();
    },
    methods: {
        fetchCategories() {
            const token = sessionStorage.getItem('access_token');
            axios.get('http://127.0.0.1:5000/admin/categories', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    this.categories = response.data.categories;
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                });
        },
        toggleCategoryStatus(category) {
            const token = sessionStorage.getItem('access_token');
            const newStatus = category.status === 'Active' ? 'Inactive' : 'Active';

            axios.patch(`http://127.0.0.1:5000/admin/categories/${category.id}`, { status: newStatus }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    // Update the status in the UI
                    category.status = newStatus;
                    console.log(response.data.message);
                })
                .catch(error => {
                    console.error('Error toggling category status:', error);
                });
        },
    },
};
</script>
  
<style scoped>
/* Add your styles here */
.container {
    max-width: 1276px;
    background: #f0f8ff;
    /* Light blue background color */
    padding: 20px;
    /* or any other preferred max-width */
}

.card {
    height: 100%;
    min-height: 400px;
    width: 300px;
    margin-left: 20px;
    margin-bottom: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-img-top {
    width: 100%;
    height: auto;
}

.category-buttons button {
    margin-left: 5px;
}
</style>

  