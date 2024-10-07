<template>
  <div>
    <user-navbar />
    <h2 class="mt-4">Your Orders</h2>
    <div class="container mt-3 text-center">
      <div v-if="orders.length === 0" class="mt-2">
        <h3>You have no orders yet.</h3>
      </div>
      <div v-else class="cardgrid row" >
        <div v-for="order in reversedOrders" :key="order.id" class="card">
          <!-- Order Card -->
          <!-- <div class="card"> -->
            <div class="card-body">
              <h5 class="card-title">Order ID: {{ order.id }}</h5>
              <p class="card-text">Order Date: {{ order.order_date }}</p>
              <p class="card-text">Total Amount: {{ order.total_price }}</p>
              <table>
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Product Price</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in order.order_items" :key="item.id">
                    <td>{{ item.product.name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ item.product.price_per_unit }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          <!-- </div> -->
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import UserNavbar from '@/components/UserNavbar.vue';

export default {
  name: 'UserOrder',
  data() {
    return {
      orders: [],
    };
  },
  mounted() {
    this.fetchOrders();
  },
  components: {
    UserNavbar,
  },
  computed: {
    reversedOrders() {
      // Return the orders array in reverse order
      return [...this.orders].reverse();
    },
  },
  methods: {
    fetchOrders() {
      const token = sessionStorage.getItem('access_token');
      axios
        .get('http://127.0.0.1:5000/user-orders', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(response => {
          this.orders = response.data.orders || [];
        })
        .catch(error => {
          console.error('Error fetching orders:', error);
        });
    },
  },
};
</script>
  
<style scoped>
.container {
  max-width: 1276px;
  background: #f0f8ff;
  /* Light blue background color */
  padding: 20px;
  /* or any other preferred max-width */
}
.card-grid {
  z-index: 500;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}
.card {
  height: 100%;
  min-height: 400px;
  width: 300px;
  margin-left: 20px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

h2 {
  font-size: 24px;
  font-weight: bold;
}

h5 {
  font-size: 18px;
  font-weight: bold;
}

p {
  font-size: 16px;
  margin: 8px 0;
}
</style>