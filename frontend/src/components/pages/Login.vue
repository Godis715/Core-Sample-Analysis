<template>
<div>
    <form @submit.prevent="login">
        <h1>Sign in</h1>
        <div>
            <input required id="username" v-model="username" type="text" placeholder="User42" />
            <label for="username">Login</label>
        </div>

        <div>
            <input required id="password" v-model="password" type="password" placeholder="Password" />
            <label for="password">Password</label>
        </div>

        <button type="submit">Login</button>
    </form>
</div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            const user = {
                name: this.username,
                password: this.password 
            };

            console.log('Try login:');
            console.log('username: ' + info.name + ', password: ' + info.password);
            
            this.$store.dispatch('AUTH_REQUEST', user).then(() => {
                this.$router.push('/');
            });
        }
    }
};
</script>