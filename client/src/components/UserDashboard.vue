<template>
    <div>
        <user-navbar />
        <h2>Welcome {{ username }}!</h2>

        <!-- Search Bar -->
        <div class="d-flex align-items-center mb-2">
            <template>
                <input v-model="searchTerm" type="text" placeholder="Search by category or product name"
                    class="form-control form-control-sm mr-2 hover-darken" @keyup.enter="fetchCategories"
                    style="width: 800px; margin-right: 10px; margin-left: 100px" />
            </template>
            <div class="filters dropdown btn-group" role="group">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton"
                    data-bs-toggle="dropdown" aria-expanded="false">
                    Filter Options
                </button>

                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <div class="form-group">
                        <label for="priceFilter">Price Range:</label>
                        <input type="number" v-model="minPrice" placeholder="Min Price" />
                        <input type="number" v-model="maxPrice" placeholder="Max Price" />
                    </div>
                    <div class="form-group">
                        <label for="mfgFilter">Manufacturing Date:</label>
                        <input type="date" v-model="mfgDate" />
                    </div>
                    <div class="form-group">
                        <label for="expFilter">Expiry Date:</label>
                        <input type="date" v-model="expDate" />
                    </div>
                    <button @click="applyFilters" class="btn btn-primary">Apply Filters</button>
                    <button @click="clearFilters" class="btn btn-secondary">Clear Filters</button>
                </div>
            </div>
        </div>

        <!-- Display Products or Categories based on search -->
        <div class="container mt-5">
            <div v-if="searchTerm" class=" cardgrid row">
                <div v-for="product in products" :key="product.id" class="card">
                    <!-- Product Card -->
                    <img :src="`http://127.0.0.1:5000/Uploads/${product.image_path}`" alt="Product Image"
                        class="card-img-top" style="height: 200px; object-fit: cover;" />
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <template v-if="product.stock === 0">
                            <p class="card-text" style="color: red;">Out of Stock</p>
                        </template>
                        <template v-else-if="product.stock <= 10">
                            <p class="card-text" style="color: orange;">Only {{ product.stock }} left in stock</p>
                            <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                            <p class="card-text">Exp: {{ product.exp }}</p>
                            <p class="card-text">Mfg: {{ product.mfg }}</p>
                            <button @click="buyNow(product)" class="btn btn-primary">Buy</button>
                            <button @click="addToCart(product)" class="btn btn-secondary">Add to Cart</button>
                        </template>
                        <template v-else>
                            <p class="card-text">Stock: {{ product.stock }}</p>
                            <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                            <p class="card-text">Exp: {{ product.exp }}</p>
                            <p class="card-text">Mfg: {{ product.mfg }}</p>
                            <button @click="buyNow(product)" class="btn btn-primary">Buy</button>
                            <button @click="addToCart(product)" class="btn btn-secondary">Add to Cart</button>
                        </template>
                    </div>
                </div>
            </div>

            <div v-else-if="minPrice || maxPrice || mfgDate || expDate" class=" cardgrid row">
                <div v-for="product in products1" :key="product.id" class="card">
                    <!-- Product Card -->
                    <img :src="`http://127.0.0.1:5000/Uploads/${product.image_path}`" alt="Product Image"
                        class="card-img-top" style="height: 200px; object-fit: cover;" />
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <template v-if="product.stock === 0">
                            <p class="card-text" style="color: red;">Out of Stock</p>
                        </template>
                        <template v-else-if="product.stock <= 10">
                            <p class="card-text" style="color: orange;">Only {{ product.stock }} left in stock</p>
                            <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                            <p class="card-text">Exp: {{ product.exp }}</p>
                            <p class="card-text">Mfg: {{ product.mfg }}</p>
                            <button @click="buyNow(product)" class="btn btn-primary">Buy</button>
                            <button @click="addToCart(product)" class="btn btn-secondary">Add to Cart</button>
                        </template>
                        <template v-else>
                            <p class="card-text">Stock: {{ product.stock }}</p>
                            <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                            <p class="card-text">Exp: {{ product.exp }}</p>
                            <p class="card-text">Mfg: {{ product.mfg }}</p>
                            <button @click="buyNow(product)" class="btn btn-primary">Buy</button>
                            <button @click="addToCart(product)" class="btn btn-secondary">Add to Cart</button>
                        </template>
                    </div>
                </div>
            </div>

            <div v-else>
                <div v-for="category in categories" :key="category.id" class="mb-2">
                    <!-- Category Card -->
                    <h3>{{ category.name }}</h3>
                    <div class=" cardgrid row">
                        <!-- Product Cards for each category -->
                        <div v-for="product in category.products" :key="product.id" class="card">
                            <img :src="`http://127.0.0.1:5000/Uploads/${product.image_path}`" alt="Product Image"
                                class="card-img-top" style="height: 250px; object-fit: cover;" />
                            <div class="card-body">
                                <h5 class="card-title">{{ product.name }}</h5>
                                <template v-if="product.stock === 0">
                                    <p class="card-text" style="color: red;">Out of Stock</p>
                                </template>
                                <template v-else-if="product.stock <= 10">
                                    <p class="card-text" style="color: orange;">Only {{ product.stock }} left in stock</p>
                                    <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                                    <p class="card-text">Exp: {{ product.exp }}</p>
                                    <p class="card-text">Mfg: {{ product.mfg }}</p>
                                    <button @click="buyNow(product)" class="btn btn-primary">Buy</button>
                                    <button @click="addToCart(product)" class="btn btn-secondary">Add to Cart</button>
                                </template>
                                <template v-else>
                                    <p class="card-text">Stock: {{ product.stock }}</p>
                                    <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                                    <p class="card-text">Exp: {{ product.exp }}</p>
                                    <p class="card-text">Mfg: {{ product.mfg }}</p>
                                    <button @click="buyNow(product)" class="btn btn-primary">Buy</button>
                                    <button @click="addToCart(product)" class="btn btn-secondary">Add to Cart</button>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import UserNavbar from '@/components/UserNavbar.vue';

export default {
    name: 'UserDashboard',
    data() {
        return {
            username: sessionStorage.getItem('username'),
            categories: [],
            products: [],
            products1: [],
            searchTerm: '',
            minPrice: '',
            maxPrice: '',
            mfgDate: '',
            expDate: '',
        };
    },
    mounted() {
        this.fetchAll();
    },
    components: {
        UserNavbar,
    },
    methods: {
        fetchAll() {
            const token = sessionStorage.getItem('access_token');
            axios
                .get('http://127.0.0.1:5000/user-dashboard', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                .then(response => {
                    this.categories = response.data.categories || [];
                    this.products = response.data.products || [];
                })
                .catch(error => {
                    console.error('Error fetching categories and products:', error);
                });
        },
        fetchCategories() {
            const token = sessionStorage.getItem('access_token');
            axios
                .get('http://127.0.0.1:5000/user-dashboard', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    params: {
                        searchTerm: this.searchTerm,
                    },
                })
                .then(response => {
                    if (this.searchTerm) {
                        this.products = response.data.products || [];
                        this.categories = []; // Clear categories when a search term is provided
                    } else {
                        this.fetchAll();
                    }
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                });
        },
        applyFilters() {
            console.log('Applying filters...');
            console.log('Data before filters:', this.products);

            const token = sessionStorage.getItem('access_token');
            axios
                .get('http://127.0.0.1:5000/apply-filters', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    params: {
                        minPrice: this.minPrice,
                        maxPrice: this.maxPrice,
                        mfgDate: this.mfgDate,
                        expDate: this.expDate,
                    },
                })
                .then(response => {
                    if (this.minPrice || this.maxPrice || this.mfgDate || this.expDate) {
                        const responseData = response.data;
                        this.products1 = responseData.products;
                        console.log('Data after filters:', this.products);
                    } else {
                        this.fetchAll();
                    }
                })
                .catch(error => {
                    console.error('Error applying filters:', error);
                });
        },
        clearFilters() {
            // Clear filter options
            this.minPrice = '';
            this.maxPrice = '';
            this.mfgDate = '';
            this.expDate = '';

            // Fetch all categories and products
            this.fetchAll();
        },
        buyNow(product) {
            const token = sessionStorage.getItem('access_token');
            const product_id = product.id;
            const quantity = 1;
            axios
                .post(
                    'http://127.0.0.1:5000/add-to-cart',
                    {
                        product_id: product_id,
                        quantity: quantity,
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                .then(() => {
                    // Redirect to the cart page
                    this.$router.push('/user/cart');
                })
                .catch(error => {
                    console.error('Error adding product to cart:', error.response.data.error);
                });
        },
        addToCart(product) {
            const token = sessionStorage.getItem('access_token');
            const product_id = product.id;
            const quantity = 1;
            axios
                .post(
                    'http://127.0.0.1:5000/add-to-cart',
                    {
                        product_id: product_id,
                        quantity: quantity,
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                .catch(error => {
                    console.error('Error adding product to cart:', error.response.data.error);
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
}
.hover-darken:hover {
    background-color: #a09292;
    color: #fff;
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

.card-body {
    margin: 10px;
    min-height: 200px;
}

.form-control-sm {
    height: 30px;
}

/* Position the dropdown next to the search bar */
.dropdown {
    margin-left: 10px;
}

h2 {
    font-size: 24px;
    font-weight: bold;
}

h5 {
    font-size: 18px;
    font-weight: bold;
}

p {
    font-size: 16px;
    margin: 8px 0;
}
</style>
  