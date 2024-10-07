<!-- Home.vue -->
<template>
    <div>
        <navbar />
        <div class="container">
            <!-- Home content goes here -->
            <h1>Welcome to The Night Store</h1>
        </div>
    </div>
</template>
  
<script>
import Navbar from '@/components/Navbar.vue';

export default {
    name: 'HomePage',
    components: {
        Navbar
    }
};
</script>
  