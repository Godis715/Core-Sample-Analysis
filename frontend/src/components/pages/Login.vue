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

        <div>{{message}}</div>
    </form>
</div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            message: ''
        }
    },
    methods: {
        login() {
            const user = {
                username: this.username,
                password: this.password 
            };

            console.log('Try login:');
            console.log('username: ' + user.username + ', password: ' + user.password);
            
            this.$store.dispatch('AUTH_REQUEST', user).then(result => {
                if (result.ok) this.$router.push('/');
                else this.message = result.message;
            }).catch(err => {
                console.log(err);
            });
        }
    }
};
</script>