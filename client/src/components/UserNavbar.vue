<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">The Night Store</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link to="/user/dashboard" class="nav-link" aria-current="page">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/user/cart" class="nav-link">Cart</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/user/orders" class="nav-link">Orders</router-link>
                    </li>
                    <li class="nav-item">
                        <button @click="logout" class="nav-link">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
  
<script>
export default {
    name: 'UserNavbar',
    methods: {
        logout() {
            // Clear user authentication state 
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('roles');
            this.$router.push('/');
            console.log('User logged out');
        },
        toggleSidebar() {
            document.getElementById('offcanvasSidebar').classList.toggle('show');
    }
    },
};
</script>
  
<style scoped>
/* Add your custom styles here */
/* Feel free to customize the styles based on your design preferences */
.navbar-link {
    text-decoration: none;
    color: #007bff;
}

.btn-outline-primary {
    color: #007bff;
    border-color: #007bff;
}

.btn-outline-primary:hover {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
}
</style>
  