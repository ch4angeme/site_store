<template>
  <div class="profile-container">
    <h2>Профиль пользователя</h2>
    <div v-if="user" class="profile-info">
      <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
      <p><strong>Дата регистрации:</strong> {{ user.datareg }}</p>

      <div class="update-username">
        <input v-model="newUsername" placeholder="Введите новое имя" class="username-input" />
        <button @click="updateUsername" class="update-button">Изменить имя</button>
      </div>
    </div>
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>
    <div v-else class="loading-message">
      <p>Загрузка...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import EventBus from '../Refresh';

export default {
  data() {
    return {
      user: '',
      error: '',
      newUsername: '',
    };
  },
  async created() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://localhost:5000/api/users/user/profile', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.user = response.data;
      } catch (error) {
        this.handleError(error, 'Ошибка получения данных профиля');
      }
    },
    async updateUsername() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.put('http://localhost:5000/api/users/user/profile/update', {
          username: this.newUsername,
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Обновляем имя пользователя в локальном состоянии
        this.user.username = response.data.username;
        EventBus.emit('username-updated', this.user.username);
        this.newUsername = '';
        this.error = '';

        // Уведомление об успешном обновлении
        alert('Имя пользователя успешно обновлено на: ' + this.user.username);
      } catch (error) {
        this.handleError(error, 'Ошибка обновления имени пользователя');
      }
    },
    handleError(error, defaultMessage) {
      if (error.response && error.response.data) {
        this.error = error.response.data.message || defaultMessage;
      } else {
        this.error = 'Ошибка соединения с сервером';
      }

      // Уведомление об ошибке
      alert(this.error);
    },
  },
};
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

.profile-info {
  margin-bottom: 20px;
}

p {
  margin: 5px 0;
  color: #555;
}

.update-username {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.username-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
}

.update-button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.update-button:hover {
  background-color: #757575;
}

.error-message {
  color: #f44336;
  margin-top: 10px;
}

.loading-message {
  color: #999;
  margin-top: 10px;
}
</style>