<!-- UserPage.vue -->
<template>
    <div>
        <admin-navbar />
        <h2>User Management</h2>

        <!-- Display the list of users with 'Manager' role -->
        <div class="container mt-4">
            <div v-if="managerUsers.length > 0">
                <div v-for="user in managerUsers" :key="user.id" class="user-tile">
                    <div class="user-info">
                        <h3>{{ user.username }}</h3>
                        <p>Email: {{ user.email }}</p>
                        <p>Status: {{ user.status }}</p>
                        <button @click="activateUser(user.id)" class="btn btn-success" v-if="user.status === 'Not Active'">
                            Activate Manager
                        </button>
                        <button @click="DeactivateUser(user.id)" class="btn btn-danger" v-if="user.status === 'Active'">
                            Deactivate Manager
                        </button>
                    </div>
                </div>
            </div>
            <div v-else>
                <p>No users with 'Not Active' status or 'Manager' role.</p>
            </div>
        </div>
    </div>
</template>
  
<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
import axios from 'axios';

export default {
    name: 'UserPage',
    data() {
        return {
            managerUsers: [], // Array to store users with 'Manager' role
        };
    },
    computed: {
        isLoggedIn() {
            // Check if the access_token is present in sessionStorage
            return sessionStorage.getItem('access_token') !== null;
        },
        isAdmin() {
            // Check if the user has the admin role 
            const userRoles = sessionStorage.getItem('roles');
            return userRoles && userRoles.includes('manager');
        },
    },
    components: {
        AdminNavbar,
    },
    mounted() {
        this.fetchManagerUsers();
    },
    methods: {
        fetchManagerUsers() {
            const token = sessionStorage.getItem('access_token');
            axios.get('http://127.0.0.1:5000/users/manager', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    this.managerUsers = response.data.users;
                })
                .catch(error => {
                    console.error('Error fetching manager users:', error);
                });
        },
        activateUser(userId) {
            const token = sessionStorage.getItem('access_token');
            axios.put(`http://127.0.0.1:5000/activate-user/${userId}`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    console.log(response.data.message);
                    // Refresh the list of users after activation
                    this.fetchManagerUsers();
                })
                .catch(error => {
                    console.error('Error activating user:', error);
                });
        },
        DeactivateUser(userId) {
            const token = sessionStorage.getItem('access_token');
            axios.put(`http://127.0.0.1:5000/deactivate-user/${userId}`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
                .then(response => {
                    console.log(response.data.message);
                    // Refresh the list of users after deactivation
                    this.fetchManagerUsers();
                })
                .catch(error => {
                    console.error('Error deactivating user:', error);
                });
        },
    },
};
</script>
  
<style scoped>
/* Add your styles here */
.container {
    max-width: 1276px;
    background: #f0f8ff; /* Light blue background color */
    padding: 20px;
    /* or any other preferred max-width */
}
.user-tile {
    display: flex;
    border: 1px solid #ccc;
    margin: 10px;
    padding: 10px;
}

.user-info {
    flex: 1;
}
</style>
  