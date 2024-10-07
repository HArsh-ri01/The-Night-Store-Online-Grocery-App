<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">The Night Store</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
                <router-link to="/login" class="btn btn-outline-primary">Login</router-link>
            </div>
        </div>
    </nav>
</template>
  
<script>
export default {
    // Navbar component logic goes here
    name: 'NavBar'
};
</script>
  
<style>
/* Navbar component styles go here */
</style>