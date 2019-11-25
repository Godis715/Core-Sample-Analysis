<template>
<div id="login-main">
    <h1 align="center">Sign in</h1>
    <hr>
    <span>Use login and password, which provided your system administrator.</span>
    <form
        id="signin-form"
        v-on:submit.prevent="login"
    >
        <div>
            <input 
                id="username"
                v-model="username"
                type="text"
                required
                placeholder="User42"
            />
            <label for="username">Login</label>
        </div>

        <div>
            <input
                id="password"
                v-model="password"
                type="password"
                required
                placeholder="Password"
            />
            <label for="password">Password</label>
        </div>

        <div class="err-message">{{message}}</div>

        <button
            class="usual"
            type="submit"
        >Login</button>
    </form>
</div>
</template>

<style>
    #login-main {
        max-width: 400px;
        margin: 2em auto;
        padding: 1em;
        border: 1.3px solid lightgray;
        background-color: white;
    }

    #signin-form {
        margin-top: 1em;
        display: flex;
        flex-direction: column;
    }

    #login-main > hr {
        border: none;
        border-bottom: 1px solid lightgray;
    }

    #signin-form > button[type="submit"] {
        margin-top: 1em;
        font-size: 1em;
        font-weight: 600;
    }

    #signin-form input[type="text"],
    #signin-form input[type="password"] {
        font-size: 1em;
        margin-bottom: 5px;
    }

    .err-message {
        color: brown;
        white-space: pre;
        margin-top: 1em;
    }
</style>

<script>
export default {
    name: "Login",
    data() {
        return {
            username: "",
            password: "",
            message: " "
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
            
            var authRequest = this.$store.dispatch('AUTH_REQUEST', user).then(result => {
                if (result.ok) this.$router.push('/');
                else {
                    if (result.err.response.status === 401) {
                        this.message = "Incorrect login or password.";
                    } else {
                        this.message = "Some errors occured. Try again later."
                    }
                }
            }).catch(err => {
                console.log(err);
            });

            this.load(authRequest);
        },

        load(somePromise) {
            this.$root.$emit('start-loading', somePromise);
        }
    }
};
</script>