<template>
    <div>
        <admin-navbar />
        <h2>Request Management</h2>
        <div class="container mt-4">
            <div v-if = "pendingCategoryChanges.length > 0" class="row">
                <div v-for="categoryChange in pendingCategoryChanges" :key="categoryChange.id" class="col-md-3">
                    <div class="info">
                        <p>{{ categoryChange.name }}</p>
                        <p>{{ categoryChange.action }}</p>
                        <button @click="approveCategoryChange(categoryChange.id)" class="btn btn-success">Approve</button>
                        <button @click="rejectCategoryChange(categoryChange.id)" class="btn btn-light">Reject</button>
                    </div>
                </div>
            </div>
            <div v-else>
                <p>No pending category changes found.</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import AdminNavbar from '@/components/AdminNavbar.vue';

export default {
    data() {
        return {
            pendingCategoryChanges: [], // Data property for pending changes
        };
    },
    components: {
        AdminNavbar,
    },
    methods: {
        async fetchPendingCategoryChanges() {
            try {
                const token = sessionStorage.getItem('access_token');
                const response = await axios.get('http://127.0.0.1:5000/admin/pending-category-changes', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                // Assuming the server returns an array of pending changes
                this.pendingCategoryChanges = response.data.pendingCategoryChanges;
            } catch (error) {
                console.error('Error fetching pending category changes:', error);
                // Handle error, display error message, etc.
            }
        },
        async approveCategoryChange(changeId) {
            try {
                const token = sessionStorage.getItem('access_token');
                await axios.put(`http://127.0.0.1:5000/admin/approve-category-change/${changeId}`, null, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // Remove the approved change from the list
                this.pendingCategoryChanges = this.pendingCategoryChanges.filter(change => change.id !== changeId);
            } catch (error) {
                console.error('Error approving category change:', error);
                // Handle error, display error message, etc.
            }
        },
        async rejectCategoryChange(changeId) {
            try {
                const token = sessionStorage.getItem('access_token');
                await axios.put(`http://127.0.0.1:5000/admin/reject-category-change/${changeId}`, null, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                // Remove the rejected change from the list
                this.pendingCategoryChanges = this.pendingCategoryChanges.filter(change => change.id !== changeId);
            } catch (error) {
                console.error('Error rejecting category change:', error);
                // Handle error, display error message, etc.
            }
        },
    },
    created() {
        // Fetch pending category changes when the component is created
        this.fetchPendingCategoryChanges();
    },
};
</script>

<style scoped>
.container {
    max-width: 1276px;
    background: #f0f8ff; /* Light blue background color */
    padding: 20px;
    /* or any other preferred max-width */
}
.tile {
    display: flex;
    border: 1px solid #ccc;
    margin: 10px;
    padding: 10px;
}

.info {
    flex: 1;
}
</style>
