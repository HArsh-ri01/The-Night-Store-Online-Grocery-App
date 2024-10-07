<template>
    <div>
        <user-navbar />
        <h2>Your Cart</h2>
        <div class="container mt-3">
            <div class="row">
                <div v-for="product in cart" :key="product.id" class="col-md-3">
                    <!-- Product Card -->
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{{ product.name }}</h5>
                            <p class="card-text">Price Per Unit: {{ product.price_per_unit }}</p>
                            <p class="card-text">Quantity: {{ product.quantity }}</p>
                            <p class="card-text">Total: {{ product.total_price }}</p>
                            <div class="division">
                                <template v-if="product.stock > 0">
                                    <button @click="updateCart(product.product_id, product.quantity - 1)"
                                        :disabled="product.quantity <= 1" class="btn btn-sm btn-outline-secondary">
                                        -
                                    </button>
                                    <span class="quantity">{{ product.quantity }}</span>
                                    <button @click="updateCart(product.product_id, product.quantity + 1)"
                                        :disabled="product.quantity >= product.stock" class="btn btn-sm btn-outline-secondary">
                                        +
                                    </button>
                                </template>
                            </div>
                            <button @click="removeFromCart(product.product_id)" class="btn btn-danger">Remove</button>
                        </div>
                    </div>
                </div>

                <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
                    {{ successMessage }}
                </div>
                <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
                    {{ errorMessage }}
                </div>

                <h3>Total Amount: {{ totalAmount }}</h3>
            </div>
            <button @click="placeOrder" class="btn btn-primary">Place Order</button>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import UserNavbar from '@/components/UserNavbar.vue';

export default {
    name: 'UserCart',
    data() {
        return {
            cart: [],
            successMessage: '',
            errorMessage: '',
        };
    },
    computed: {
        totalAmount() {
            return this.cart.reduce((total, product) => total + product.total_price, 0);
        },
    },
    mounted() {
        this.fetchCart();
    },
    components: {
        UserNavbar,
    },
    methods: {
        fetchCart() {
            const token = sessionStorage.getItem('access_token');
            axios
                .get('http://127.0.0.1:5000/cart', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                .then(response => {
                    this.cart = response.data.cart || [];
                })
                .catch(error => {
                    console.error('Error fetching cart:', error);
                });
        },
        removeFromCart(productId) {
            const token = sessionStorage.getItem('access_token');
            axios
                .delete(`http://127.0.0.1:5000/remove-from-cart/${productId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                .then(() => {
                    this.fetchCart();
                })
                .catch(error => {
                    console.error('Error removing product from cart:', error);
                });
        },
        updateCart(productId, quantity) {
            const token = sessionStorage.getItem('access_token');
            const existingProduct = this.cart.find(product => product.product_id === productId);  // Corrected line
            const newQuantity = quantity > existingProduct.stock ? existingProduct.stock : quantity;

            axios
                .put(
                    `http://127.0.0.1:5000/update-cart-quantity/${productId}`,
                    {
                        quantity: newQuantity,
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                .then(() => {
                    this.fetchCart();
                })
                .catch(error => {
                    console.error('Error updating product quantity:', error);
                });
        },
        placeOrder() {
            const token = sessionStorage.getItem('access_token');
            axios
                .post(
                    'http://127.0.0.1:5000/place-order',
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                .then(response => {
                    this.successMessage = response.data.message;
                    this.errorMessage = ''; // Clear any previous error message
                    console.log(response.data);
                    this.fetchCart();
                    
                })
                .catch(error => {
                    this.errorMessage = 'Please add products to proceed :) ';
                    this.successMessage = ''; // Clear any previous success message
                    console.error('Error updating order:', error);
                    this.fetchCart();
                });
        },
    },
};
</script>

<style scoped>
.container {
    max-width: 1276px;
    background: #f0f8ff; /* Light blue background color */
    padding: 20px;
    /* or any other preferred max-width */
}
.card {
  height: 100%;
  width: 300px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.division {
    margin-bottom: 0.5rem;
}
</style>
  