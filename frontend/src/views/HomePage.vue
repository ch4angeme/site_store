<template>
  <div class="home-page">
    <h1 class="welcome-title">Добро пожаловать в наш магазин!</h1>
    <h6 class="info-message">
      Ваши данные передаются в ФСБ <span class="emoji">😀</span>
    </h6>

    <section class="intro">
      <p class="intro-text">
        Мы предлагаем широкий ассортимент товаров, от продуктов питания до бытовой техники.
        У нас вы найдете все необходимое по доступным ценам!
      </p>
      <router-link to="/catalog" class="shop-button">Перейти в каталог</router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: white;
  text-align: center;
  font-family: 'Arial', sans-serif;
}

.welcome-title {
  font-size: 3rem;
  color: #333;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.info-message {
  font-size: 1.2rem;
  color: #555;
  margin-top: 0;
}

.intro {
  margin: 20px 0;
}

.intro-text {
  font-size: 1.2rem;
  color: #666;
  max-width: 600px;
  margin-bottom: 20px;
}

.shop-button {
  background-color: #333; /* Зеленый цвет */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.shop-button:hover {
  background-color: #555; /* Темнее при наведении */
}
</style>
