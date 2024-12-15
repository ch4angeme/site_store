<template>
  <div>
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Имя пользователя" required />
      <input type="password" v-model="password" placeholder="Пароль" required />
      <button type="submit">Войти</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
    <p>Еще не зарегистрированы?</p>
    <router-link to="/registration">Зарегистрироваться</router-link>
  </div>
</template>

<script>
import axios from 'axios';
import EventBus from '../Refresh';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/api/users/user/login', {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('username', this.username);
        EventBus.emit('userLoggedIn', this.username);
        this.$router.push('/');
      } catch (error) {
        this.errorMessage = error.response.data.message || 'Ошибка входа';
      }
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: auto;
}

input {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #757575;
}

p {
  margin: 10px 0;
}

router-link {
  color: #3a3a3a;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}
</style>