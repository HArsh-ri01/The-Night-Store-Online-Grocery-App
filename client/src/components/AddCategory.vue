<template>
  <div>
    <admin-navbar />
    <div class="container mt-5">
      <h2 class="text-center mb-4">Add Category</h2>
      <form @submit.prevent="submitForm" class="col-md-6 mx-auto">
        <div class="form-group">
          <label for="categoryName">Category Name:</label>
          <input type="text" id="categoryName" v-model="categoryName" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="categoryImage">Category Image:</label>
          <input type="file" @change="handleFileChange" id="categoryImage" class="form-control" accept="image/*" required>
        </div>
        <button type="submit" class="btn btn-primary">Add Category</button>

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
import AdminNavbar from '@/components/AdminNavbar.vue';

export default {
  name: 'AddCategory',
  data() {
    return {
      categoryName: '',
      categoryImage: null,
      successMessage: '',
      errorMessage: '',
    };
  },
  components: {
    // components go here
    AdminNavbar
  },
  methods: {
    handleFileChange(event) {
      this.categoryImage = event.target.files[0];
    },
    submitForm() {
      // Retrieve the JWT token from wherever you have stored it (e.g., Vuex store)
      const token = sessionStorage.getItem('access_token');

      // Use FormData to send files
      const formData = new FormData();
      formData.append('name', this.categoryName);
      formData.append('image', this.categoryImage, this.categoryImage.name);

      axios.post('http://127.0.0.1:5000/add-category', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          this.successMessage = response.data.message;
          this.errorMessage = ''; // Clear any previous error message
          console.log(response.data);

          setTimeout(() => {
            this.$router.push('/adminpage');
          }, 1000);
        })
        .catch(error => {
          if (error.response && error.response.status === 422) {
            this.errorMessage = 'Unauthorized access. Please login and try again.';
            this.successMessage = ''; // Clear any previous success message
            console.error('Unauthorized access:', error);

            setTimeout(() => {
              this.$router.push('/login');
            }, 1000);
          }
          else {
            this.errorMessage = 'Error Adding Category. Please try again.';
            this.successMessage = ''; // Clear any previous success message
            console.error('Error adding category:', error);
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
    background: #f0f8ff;
    /* Light blue background color */
    padding: 20px;
}
.btn {
    margin-top: 20px;
    margin-left: 20px;
}
</style>