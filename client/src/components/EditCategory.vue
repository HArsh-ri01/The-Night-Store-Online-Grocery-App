<template>
    <div>
        <admin-navbar />
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
import AdminNavbar from '@/components/AdminNavbar.vue';
import axios from 'axios';

export default {
    name: 'EditCategory',
    data() {
        return {
            categoryId: this.$route.params.categoryId,
            categoryName: '',
            categoryImage: null,
            successMessage: '',
            errorMessage: '',
        };
    },
    components: {
        AdminNavbar,
    },
    mounted() {
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
                })
                .catch(error => {
                    console.error('Error fetching category details:', error);
                });
        },
        updateCategory() {
            const token = sessionStorage.getItem('access_token');
            const formData = new FormData();
            formData.append('name', this.categoryName);

            if (this.$refs.categoryImage.files.length > 0) {
                formData.append('image', this.$refs.categoryImage.files[0]);
            }

            axios.put(`http://127.0.0.1:5000/edit-category/${this.categoryId}`, formData, {
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
                        this.errorMessage = 'Error Updateing Category. Please try again.';
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
  