<template>
  <header>
    <nav>
      <ul>
        <li><router-link to="/">Главная</router-link></li>
        <li><router-link to="/catalog">За продуктами</router-link></li>
        <li><router-link to="/login">Вход</router-link></li>
        <li>
          <router-link to="/profile" class="profile-link">{{ username }}</router-link>
          <button @click="logout" class="logout-button">Выйти</button>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import EventBus from '../Refresh';

export default {
  name: 'HeaderPage',
  data() {
    return {
      username: localStorage.getItem('username') || '',
      isLoggedIn: !!localStorage.getItem('username'),
    };
  },
  created() {
    EventBus.on('username-updated', this.updateUsername);
    EventBus.on('userLoggedIn', this.LoggedIn);
    EventBus.on('userLoggedOut', this.LoggedOut);
  },
  beforeUnmount() {
    EventBus.off('username-updated', this.updateUsername);
    EventBus.off('userLoggedIn', this.LoggedIn);
    EventBus.off('userLoggedOut', this.LoggedOut);
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      this.username = '';
      this.isLoggedIn = false;
      EventBus.emit('userLoggedOut');
      this.$router.push('/login');
    },
    updateUsername(newUsername) {
      this.username = newUsername;
      localStorage.setItem('username', newUsername);
    },
    LoggedIn(username) {
      this.username = username;
      this.isLoggedIn = true;
      localStorage.setItem('username', username);
    },
    LoggedOut() {
      this.username = '';
      this.isLoggedIn = false;
    },
  },
};
</script>

<style scoped>
header {
  background-color: #3a3a3a;
  padding: 15px 20px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

nav ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

nav ul li {
  display: inline;
  margin: 0 15px;
}

nav ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

nav ul li a:hover {
  color: #757575;
}

.logout-button {
  background-color: #757575;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #757575;
}

.profile-link {
  margin-right: 10px;
}
</style>