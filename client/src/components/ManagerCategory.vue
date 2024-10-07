<template>
    <div>
        <!-- Manager-specific navigation or components if needed -->
        <ManagerNavbar />
        <div class="container mt-5">
            <h2 class="text-center mb-4">Add Category</h2>

            <form @submit.prevent="addCategory" class="col-md-6 mx-auto">
                <div class="form-group">
                    <label for="categoryName">Category Name:</label>
                    <input type="text" id="categoryName" v-model="categoryName" class="form-control" required>
                </div>

                <div class="form-group">
                    <label for="categoryImage">Category Image:</label>
                    <input type="file" @change="handleFileChange" id="categoryImage" class="form-control" accept="image/*"
                        required>
                </div>

                <div>
                    <label for="categoryStatus">Category Status:</label>
                    <select id="categoryStatus" v-model="categoryStatus" class="form-control" required>
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                    </select>
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
import ManagerNavbar from '@/components/ManagerNavbar.vue';

export default {
    data() {
        return {
            categoryName: '',
            categoryImage: null,
            categoryStatus: '',
            successMessage: '',
            errorMessage: '',
        };
    },
    components: {
        ManagerNavbar,
    },
    methods: {
        handleFileChange(event) {
            this.categoryImage = event.target.files[0];
        },
        addCategory() {
            const token = sessionStorage.getItem('access_token');

            const formData = new FormData();
            formData.append('name', this.categoryName);
            formData.append('image', this.categoryImage, this.categoryImage.name);
            formData.append('status', this.categoryStatus);

            axios.post('http://127.0.0.1:5000/manager/add-category', formData, {
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
                    this.errorMessage = 'Error Adding category. Please try again.';
                    this.successMessage = ''; // Clear any previous success message
                    console.error('Error Adding category:', error);
                });
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
  