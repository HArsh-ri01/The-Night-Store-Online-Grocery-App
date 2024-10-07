<template>
    <div>
        <ManagerNavbar />
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="mb-0">Manager Page</h2>
            <router-link to="/manager/add-category" class="btn btn-primary">Add Category</router-link>
        </div>
        <div class="container mt-4">
            <!-- Display categories -->
            <div v-if="categories.length > 0" class="cardgrid row">
                <div v-for="category in categories" :key="category.id" class="card">
                    <img :src="`http://127.0.0.1:5000/Uploads/${category.image_path}`" alt="Default Image"
                        class="card-img-top" style="height: 250px; object-fit: cover;" />
                    <div class="card-body">
                        <h3 class="card-title">{{ category.name }}</h3>
                        <p class="card-text">Status: {{ category.status }}</p>
                        <!-- Display products within the category -->
                        <div v-if="category.products && category.products.length > 0">
                            <div v-for="product in category.products" :key="product.id" class="product-tile">
                                <h4>{{ product.name }}</h4>
                                <p>Stock: {{ product.stock }}</p>
                                <p>Price Per Unit: {{ product.price_per_unit }}</p>
                                <!-- Add other product details as needed -->
                            </div>
                        </div>
                        <router-link :to="'manager/edit-category/' + category.id" class="btn btn-secondary btn-sm">Edit
                            Category</router-link>

                        <button @click="deleteCategory(category.id)" class="btn btn-danger btn-sm"
                            :disabled="category.status === 'Inactive'">{{ markdeleted(category) }}</button>
                        <button @click="addProduct(category.id)" class="btn btn-primary btn-sm">Add Product</button>
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
import ManagerNavbar from '@/components/ManagerNavbar.vue';
import axios from 'axios';

export default {
    name: 'ManagerPage',
    data() {
        return {
            categories: [],
        };
    },
    components: {
        ManagerNavbar,
    },
    mounted() {
        this.fetchCategories();
    },
    methods: {
        markdeleted(category) {
            return category.status === 'Inactive' ? 'Deleted' : 'Delete';
        },
        fetchCategories() {
            const token = sessionStorage.getItem('access_token');
            axios.get('http://127.0.0.1:5000/manager/categories', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    console.log('Categories response:', response.data);
                    this.categories = response.data.categories || []; // Ensure categories is always an array
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                });
        },
        addProduct(categoryId) {
            // Implement navigation to the AddProduct page with the selected category ID
            this.$router.push(`/add-product/${categoryId}`);
        },
        deleteCategory(categoryId) {
            if (confirm('Are you sure you want to delete this category?')) {
                const token = sessionStorage.getItem('access_token');
                axios.delete(`http://127.0.0.1:5000/manager/delete-category/${categoryId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                    .then(response => {
                        console.log(response.data.message);
                        // Optionally, update your UI to reflect the deleted category
                        this.fetchCategories();
                    })
                    .catch(error => {
                        console.error('Error deleting category:', error);
                        // Handle error, display error message, etc.
                    });
            }
        },
    },
    computed: {
        isLoggedIn() {
            // Check if the access_token is present in sessionStorage
            return sessionStorage.getItem('access_token') !== null;
        },
        isManager() {
            // Check if the user has the admin role 
            const userRoles = sessionStorage.getItem('roles');
            return userRoles && userRoles.includes('manager');
        },
    },
};
</script>
  
<style scoped>
/* Remove your existing styles here */

/* Add Bootstrap styles */
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

.product-tile {
    border: 1px solid #ddd;
    margin: 5px;
    padding: 5px;
}</style>
