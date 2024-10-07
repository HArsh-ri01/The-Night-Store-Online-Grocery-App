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
                        <router-link to="/adminpage" class="nav-link" aria-current="page">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/categorychanges" class="nav-link">Requests</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/userspage" class="nav-link">Managers</router-link>
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
    name: 'AdminNavbar',
    methods: {
        logout() {
            // Clear user authentication state 
            sessionStorage.removeItem('access_token');
            sessionStorage.removeItem('roles');
            this.$router.push('/');
        },
        toggleSidebar() {
            document.getElementById('offcanvasSidebar').classList.toggle('show');
        },
    }
};
</script>