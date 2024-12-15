<template>
  <div>
    <h2>Корзина</h2>
    <ul>
      <li v-for="item in cartItems" :key="item.product_id">
        {{ item.name }} - {{ item.price }} руб. (Количество: {{ item.quantity }})
        <button @click="removeFromCart(item.product_id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      cartItems: [],
    };
  },
  async created() {
    await this.fetchCart();
  },
  methods: {
    async fetchCart() {
      const token = localStorage.getItem('access_token');
      try {
        const response = await axios.get('http://localhost:5000/api/cart', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.cartItems = response.data.cart;
      } catch (error) {
        alert('Вы не авторизованы');
      }
    },
    async removeFromCart(productId) {
      const token = localStorage.getItem('access_token');
      try {
        await axios.delete(`http://localhost:5000/api/cart/remove/${productId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        await this.fetchCart(); // Обновляем корзину после удаления
      } catch (error) {
        alert('Ошибка удаления товара из корзины');
      }
    },
  },
};
</script>

<style scoped>
.cart {
  border: 1px solid #ccc;
  padding: 10px;
  position: absolute;
  top: 50px; /* Позиция корзины */
  right: 20px; /* Позиция корзины */
  background-color: white;
  z-index: 1000; /* Чтобы корзина была поверх других элементов */
}
</style>