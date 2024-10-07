<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
        <div class="card p-5" style="max-width: 1000px; width: 100%; margin-top: 100px;">
            <button @click="goToHome" class="btn btn-secondary btn-lg ml-2">Home</button>
            <h1 class="mb-4" style="font-size: 38px;">Sign Up</h1>
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label for="username" style="font-size: 28px;">Username:</label>
                    <input type="text" id="username" v-model="username" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="email" style="font-size: 28px;">Email:</label>
                    <input type="email" id="email" v-model="email" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="password" style="font-size: 28px;">Password:</label>
                    <input type="password" id="password" v-model="password" class="form-control" required>
                </div>
                <div class="form-group">
                    <label for="role" style="font-size: 28px;">Role:</label>
                    <select id="role" v-model="role" class="form-control" required>
                        <option value="user">User</option>
                        <option value="manager">Manager</option>
                    </select>
                </div>
                <div class="text-center mt-4">
                    <button type="submit" class="btn btn-primary btn-lg mr-2">Sign Up</button>
                    <router-link to="/login" class="btn btn-primary btn-lg d-inline-block">Login</router-link>
                </div>
            </form>
            <div v-if="signupSuccess" class="alert alert-success mt-4" role="alert" style="font-size: 18px;">
                Successfully signed up!
            </div>
            <div v-if="signupError" class="alert alert-danger mt-4" role="alert" style="font-size: 18px;">
                {{ signupErrorMessage }}
            </div>
        </div>
    </div>
</template>
  
  
<script>
export default {
    name: 'signupUser',
    data() {
        return {
            username: '',
            email: '',
            password: '',
            role: '', // Added role property
            signupSuccess: false,
            signupError: false,
            signupErrorMessage: ''
        };
    },
    methods: {
        submitForm() {
            const userData = {
                username: this.username,
                email: this.email,
                password: this.password,
                role: this.role // Include role in the submitted data
            };

            fetch('http://127.0.0.1:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Signup response:', data);

                    if (data.message === "Username already exists" || data.message === "Email already exists") {
                        this.signupSuccess = false;
                        this.signupError = true;
                        this.signupErrorMessage = data.message;
                    }
                    else {
                        this.signupSuccess = true;
                        this.signupError = false;
                        this.signupErrorMessage = '';
                        // Clear any existing error message
                    }
                })
                .catch(error => {
                    console.error('Signup error:', error);

                    this.signupSuccess = false;
                    this.signupError = true;
                    this.signupErrorMessage = 'An error occurred during signup';
                });
        },
        goToHome() {
            this.$router.push('/');
        }
    }
};
</script>



