<template>
    <div>
        <ManagerNavbar />
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="mb-0">Product Page</h2>
        </div>
        <div class="container mt-4">
            <div v-for="(category, categoryName) in productsByCategory" :key="categoryName" class="cardgrid row">
                <h3 class="mb-3">{{ categoryName }}</h3>
                <div v-if="category.length === 0" class="col-md-3">
                    <p>Yet to add products to this category.</p>
                </div>
                <div v-else class="cardgrid row">
                    <div v-for="product in category" :key="product.id" class="card">
                        <img :src="`http://127.0.0.1:5000/Uploads/${product.image_path}`" alt="Product Image"
                            class="card-img-top" style="height: 250px; object-fit: cover;" />
                        <div class="card-body">
                            <h5 class="card-title">{{ product.name }}</h5>
                            <p class="card-text">Stock: {{ product.stock }}</p>
                            <p class="card-text">Price: {{ product.price_per_unit }}</p>
                            <p class="card-text">Exp: {{ product.exp }}</p>
                            <p class="card-text">Mfg: {{ product.mfg }}</p>
                            <p class="card-text">Status: {{ product.status }}</p>
                            <router-link :to="{ name: 'ManagerEditProduct', params: { productId: product.id } }">
                                <button class="btn btn-secondary">Edit</button>
                            </router-link>
                            <button @click="toggleProductStatus(product)" class="btn"
                                :class="{ 'btn-success': product.status === 'Inactive', 'btn-danger': product.status === 'Active' }">
                                {{ product.status === 'Active' ? 'Disable' : 'Enable' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="Object.keys(productsByCategory).length === 0">
                <p>No products found.</p>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import ManagerNavbar from '@/components/ManagerNavbar.vue';

export default {
    name: 'ProductPage',
    data() {
        return {
            productsByCategory: {},
        };
    },
    components: {
        ManagerNavbar,
    },
    mounted() {
        this.fetchProducts();
    },
    methods: {
        downloadCSV() {
            const token = sessionStorage.getItem('access_token');
            const apiUrl = 'http://127.0.0.1:5000/download/products/csv';

            axios.get(apiUrl, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                responseType: 'arraybuffer',
            })
                .then(response => {
                    // Create a Blob from the array buffer
                    const blob = new Blob([response.data], { type: 'text/csv' });

                    // Create a download link
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'products.csv';
                    document.body.appendChild(link);  // Append the link to the document body
                    link.click();

                    // Remove the link from the document body after the download
                    document.body.removeChild(link);

                    // Clean up
                    window.URL.revokeObjectURL(link.href);
                })
                .catch(error => {
                    console.error('Error downloading CSV:', error);
                });
        },
        fetchProducts() {
            const token = sessionStorage.getItem('access_token');
            axios.get('http://127.0.0.1:5000/products', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    this.productsByCategory = response.data.products_by_category || {};
                })
                .catch(error => {
                    console.error('Error fetching products:', error);
                });
        },
        toggleProductStatus(product) {
            const token = sessionStorage.getItem('access_token');
            const newStatus = product.status === 'Active' ? 'Inactive' : 'Active';

            axios.patch(`http://127.0.0.1:5000/products/${product.id}`, { status: newStatus }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    // Update the status in the UI
                    product.status = newStatus;
                    console.log(response.data.message);
                })
                .catch(error => {
                    console.error('Error toggling product status:', error);
                });
        },
    },
};
</script>
  
<style scoped>
.container {
    max-width: 1276px;
    background: #f0f8ff;
    /* Light blue background color */
    padding: 20px;
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
</style>
  