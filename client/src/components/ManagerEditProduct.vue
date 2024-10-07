<template>
  <div>
    <manager-navbar />
    <div class="container mt-5">
      <h2 class="text-center mb-4">Edit Product</h2>

      <form @submit.prevent="updateProduct" class="col-md-6 mx-auto">

        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" v-model="productData.name" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="stock">Stock:</label>
          <input type="number" v-model="productData.stock" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="price_per_unit">Price per Unit:</label>
          <input type="number" v-model="productData.price_per_unit" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="exp">Expiration Date:</label>
          <input type="date" v-model="productData.exp" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="mfg">Manufacturing Date:</label>
          <input type="date" v-model="productData.mfg" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="category_id">Category:</label>
          <select v-model="productData.category_id" class="form-control">
            <option v-for="category in productData.availableCategories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="image">Product Image:</label>
          <input type="file" ref="imageInput" @change="onImageChange" class="form-control" />
        </div>

        <p>Status: {{ productData.status }}</p>

        <button type="submit" class="btn btn-primary">Update Product</button>
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
  name: 'EditProductPage',
  data() {
    return {
      productData: {
        name: '',
        stock: 0,
        price_per_unit: 0,
        exp: '',
        mfg: '',
        category_id: 0,
        availableCategories: [],
        image: null, // To store the new image file
        status:''
      },
      successMessage: '',
      errorMessage: '',
    };
  },
  components: {
    ManagerNavbar,
  },
  mounted() {
    // Fetch the product details using the productId from the route params
    this.fetchAvailableCategories();
    const productId = this.$route.params.productId;
    this.fetchProductDetails(productId);
  },
  methods: {
    fetchAvailableCategories() {
      const token = sessionStorage.getItem('access_token');
      axios.get('http://127.0.0.1:5000/manager/categories', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          this.productData.availableCategories = response.data.categories || [];
        })
        .catch(error => {
          console.error('Error fetching available categories:', error);
        });
    },
    fetchProductDetails(productId) {
      const token = sessionStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/products/${productId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          // Set the data for form fields based on the response
          const product = response.data.product;
          this.productData.name = product.name;
          this.productData.stock = product.stock;
          this.productData.price_per_unit = product.price_per_unit;
          this.productData.exp = product.exp;
          this.productData.mfg = product.mfg;
          this.productData.status = product.status;
          this.productData.category_id = product.category_id;
        })
        .catch(error => {
          console.error('Error fetching product details:', error);
        });
    },
    onImageChange(event) {
      // Update productData.image with the selected image file
      this.productData.image = event.target.files[0];
    },
    updateProduct() {
      // Prepare form data
      const formData = new FormData();
      formData.append('name', this.productData.name);
      formData.append('stock', this.productData.stock);
      formData.append('price_per_unit', this.productData.price_per_unit);
      formData.append('exp', this.productData.exp);
      formData.append('mfg', this.productData.mfg);
      formData.append('category_id', this.productData.category_id);
      if (this.productData.image) {
        formData.append('image', this.productData.image, this.productData.image.name);
      }

      // Make the PUT request to update the product
      const token = sessionStorage.getItem('access_token');
      axios.put(`http://127.0.0.1:5000/edit-product/${this.$route.params.productId}`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      })
        .then(response => {
          this.successMessage = response.data.message;
          this.errorMessage = ''; // Clear any previous error message
          console.log(response.data);

          setTimeout(() => {
            this.$router.push('/manager/products');
          }, 1000);
        })
        .catch(error => {
          this.errorMessage = 'Error updating category. Please try again.';
          this.successMessage = ''; // Clear any previous success message
          console.error('Error updating category:', error);
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
  