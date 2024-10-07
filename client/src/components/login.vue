<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card p-5" style="max-width: 1000px; width: 100%; margin-top: -100px;">
      <h1 class="mb-4" style="font-size: 38px;">Login</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="username" style="font-size: 28px;">Username:</label>
          <input type="text" id="username" class="form-control" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="password" style="font-size: 28px;">Password:</label>
          <input type="password" id="password" class="form-control" v-model="password" required>
        </div>
        <div class="text-center mt-4">
          <button type="submit" class="btn btn-primary btn-lg">Login</button>
          <router-link to="/register" class="btn btn-primary btn-lg ml-2">Register</router-link>
        </div>
      </form>
      <div v-if="loggedIn" class="alert alert-success mt-4" role="alert" style="font-size: 18px;">
        Successfully logged in as {{ username }}!
      </div>
      <div v-if="error" class="alert alert-danger mt-4" role="alert" style="font-size: 18px;">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'loginUser',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loggedIn: false
    };
  },
  methods: {
    submitForm() {
      const userData = {
        username: this.username,
        password: this.password
      };

      axios
        .post('http://127.0.0.1:5000/login', userData)
        .then(response => {
          console.log(response.data);

          const { username, roles, access_token } = response.data;

          const userRoles = Array.isArray(roles) ? roles : [];
          sessionStorage.setItem('access_token', access_token);
          sessionStorage.setItem('username', username);
          sessionStorage.setItem('roles', JSON.stringify(userRoles));

          this.loggedIn = true;
          this.error = ''; // Clear any previous errors

          setTimeout(() => {
            console.log('User Roles:', userRoles);
            if (userRoles.includes('admin')) {
              this.$router.push('/adminpage');
            } else if (userRoles.includes('manager')) {
              this.$router.push('/managerpage');
            } else {
              this.$router.push('/user/dashboard');
            }
          }, 1000); // Redirect after a 1-second delay
        })
        .catch(error => {
          // Error handling
          if (error.response) {
            console.error('Error status:', error.response.status);
            console.error('Error message:', error.response.data.error);
            this.error = 'Invalid username or password';
          } else if (error.request) {
            console.error('No response received..:', error.request);
            this.error = 'No response received';
          } else {
            console.error('Error setting up the request:', error.message);
            this.error = 'An error occurred';
          }
        });
    }
  }
};
</script>

<style>
.error {
  color: red;
  margin-top: 10px;
}

.alert {
  margin-top: 10px;
}
</style>
