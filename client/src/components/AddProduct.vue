<template>
    <div>
        <ManagerNavbar />
        <div class="container mt-5">
            <h2 class="text-center mb-4">Add Product</h2>
            <form @submit.prevent="submitForm" class="col-md-6 mx-auto">
                <div class="form-group">
                    <label for="productName">Product Name:</label>
                    <input type="text" id="productName" v-model="productName" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="stock">Stock:</label>
                    <input type="number" id="stock" v-model="stock" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="pricePerUnit">Price Per Unit:</label>
                    <input type="number" id="pricePerUnit" v-model="pricePerUnit" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="exp">Expiration Date:</label>
                    <input type="date" id="exp" v-model="exp" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="mfg">Manufacturing Date:</label>
                    <input type="date" id="mfg" v-model="mfg" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="category">Category:</label>
                    <select id="category" v-model="category" class="form-control" required>
                        <!-- Populate with categories from your API -->
                        <option v-for="category in categories" :key="category.id" :value="category.id">
                            {{ category.name }}
                        </option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="productImage">Product Image:</label>
                    <input type="file" @change="handleFileChange" id="productImage" class="form-control" accept="image/*"
                        required>
                </div>
                <button type="submit" class="btn btn-primary">Add Product</button>

                <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
                    {{ successMessage }}
                </div>
                <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
                    {{ errorMessage }}
                </div>

            </form>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import ManagerNavbar from '@/components/ManagerNavbar.vue';

export default {
    name: 'AddProduct',
    data() {
        return {
            productName: '',
            stock: 0,
            pricePerUnit: 0,
            exp: '',
            mfg: '',
            category: '', // Selected category
            productImage: null,
            categories: [], // To store available categories
            successMessage: '',
            errorMessage: '',
        };
    },
    components: {
        ManagerNavbar,
    },
    mounted() {
        // Fetch categories from your API and populate the dropdown
        const token = sessionStorage.getItem('access_token');
        axios.get('http://127.0.0.1:5000/categories', {
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
    methods: {
        handleFileChange(event) {
            this.productImage = event.target.files[0];
        },
        submitForm() {
            // Retrieve the JWT token from wherever you have stored it (e.g., Vuex store)
            const token = sessionStorage.getItem('access_token');

            // Use FormData to send files
            const formData = new FormData();
            formData.append('name', this.productName);
            formData.append('stock', this.stock);
            formData.append('price_per_unit', this.pricePerUnit);
            formData.append('exp', this.exp);
            formData.append('mfg', this.mfg);
            formData.append('category_id', this.category);
            formData.append('image', this.productImage, this.productImage.name);

            axios.post(`http://127.0.0.1:5000/add-product/${this.category}`, formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    this.successMessage = response.data.message;
                    this.errorMessage = ''; // Clear any previous error message
                    console.log(response.data);

                    setTimeout(() => {
                        this.$router.push('/managerpage');
                    }, 1000);
                })
                .catch(error => {
                    if (error.response && error.response.status === 401) {
                        this.errorMessage = 'Unauthorized access. Please login and try again.';
                        this.successMessage = ''; // Clear any previous success message
                        console.error('Unauthorized access:', error);

                        setTimeout(() => {
                            this.$router.push('/login');
                        }, 1000);
                    } 
                    else {
                        this.errorMessage = 'Error Adding Products. Please try again.';
                        this.successMessage = ''; // Clear any previous success message
                        console.error('Error adding products:', error);
                    }
                });
        },
    },
};
</script>
  
<style scoped>
/* Add your styles here */
.container {
  margin-top: 100px;
  background-color: #f0f8ff;
  padding: 20px;
}

.btn {
  margin-top: 20px;
  margin-left: 20px;
}
</style>
  