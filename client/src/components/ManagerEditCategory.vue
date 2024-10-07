<template>
    <div>
        <manager-navbar />
        <div class="container mt-5">
            <h2 class="text-center mb-4">Edit Category</h2>

            <form @submit.prevent="updateCategory" class="col-md-6 mx-auto">
                <div class="form-group">
                    <label for="categoryName">Category Name:</label>
                    <input type="text" id="categoryName" v-model="categoryName" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="categoryImage">Category Image:</label>
                    <input type="file" id="categoryImage" ref="categoryImage" class="form-control" accept="image/*" />
                </div>

                <div class="form-group">
                    <label for="categoryStatus">Category Status:</label>
                    <select id="categoryStatus" v-model="categoryStatus" class="form-control" required>
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                    </select>
                </div>

                <button type="submit" class="btn btn-primary">Update Category</button>

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
import ManagerNavbar from '@/components/ManagerNavbar.vue';
import axios from 'axios';

export default {
    name: 'ManagerEditCategory',
    data() {
        return {
            categoryId: this.$route.params.categoryId,
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
    mounted() {
        // Fetch category details
        this.fetchCategoryDetails();
    },
    methods: {
        fetchCategoryDetails() {
            const token = sessionStorage.getItem('access_token');
            axios.get(`http://127.0.0.1:5000/categories/${this.categoryId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    const category = response.data.category;
                    this.categoryName = category.name;
                    this.categoryStatus = category.status;
                })
                .catch(error => {
                    console.error('Error fetching category details:', error);
                });
        },
        updateCategory() {
            const token = sessionStorage.getItem('access_token');
            const formData = new FormData();
            formData.append('name', this.categoryName);
            formData.append('status', this.categoryStatus);

            // Only append the image data if a new image is selected
            if (this.$refs.categoryImage.files.length > 0) {
                formData.append('image', this.$refs.categoryImage.files[0]);
            }

            axios.put(`http://127.0.0.1:5000/update-category/${this.categoryId}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
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
    background: #f0f8ff;
    /* Light blue background color */
    padding: 20px;
}

.btn {
    margin-top: 20px;
    margin-left: 20px;
}
</style>
