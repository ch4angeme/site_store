<template>
  <div class="product-container">
    <h2>Продукты</h2>
    <button @click="toggleCart" class="toggle-cart-button">{{ showCart ? 'Скрыть корзину' : 'Показать корзину' }}</button>

    <div v-if="showCart" class="cart">
      <h3>Корзина</h3>
      <ul>
        <li v-for="item in cartItems" :key="item.product_id" class="cart-item">
          {{ item.name }} - {{ item.price }} руб. (Количество: {{ item.quantity }})
          <button @click="removeFromCart(item.product_id)" class="remove-button">Удалить</button>
        </li>
      </ul>
      <p v-if="cartItems.length === 0">Корзина пуста.</p>
    </div>

    <div class="product-list-container">
      <ul class="product-list">
        <li v-for="product in products" :key="product.id" @click="openProductModal(product)" class="product-item">
          {{ product.name }} - {{ product.price }} руб.
          <button @click.stop="addToCart(product.id)" class="add-to-cart-button">Добавить в корзину</button>
        </li>
      </ul>
    </div>

    <div v-if="isModalOpen" class="overlay" @click="closeProductModal"></div>
    <div v-if="isModalOpen" class="modal" @click.stop>
      <h2>{{ selectedProduct.name }}</h2>
      <p>{{ selectedProduct.description }}</p>
      <p>Цена: {{ selectedProduct.price }} руб.</p>
      <p>Описание: {{ selectedProduct.about }}</p>
      <button @click="closeProductModal" class="close-modal-button">Закрыть</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
      cartItems: [],
      showCart: false,
      isModalOpen: false,
      selectedProduct: {},
    };
  },
  async created() {
    await this.fetchProducts();
    await this.fetchCart();
  },
  methods: {
    async fetchProducts() {
      const response = await axios.get('http://localhost:5000/api/all_products');
      this.products = response.data.results;
    },
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
        console.error('Ошибка получения корзины', error);
      }
    },
    async addToCart(productId) {
      const token = localStorage.getItem('access_token');
      try {
        await axios.post('http://localhost:5000/api/cart/add', { product_id: productId }, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        await this.fetchCart();
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
        await this.fetchCart();
      } catch (error) {
        alert('Ошибка удаления товара из корзины');
      }
    },
    toggleCart() {
      this.showCart = !this.showCart;
    },
    openProductModal(product) {
      this.selectedProduct = product;
      this.isModalOpen = true;
    },
    closeProductModal() {
      this.isModalOpen = false;
      this.selectedProduct = {};
    },
  },
};
</script>

<style scoped>
.product-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center; /* Центрируем текст внутри контейнера */
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

.toggle-cart-button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 20px;
}

.toggle-cart-button:hover {
  background-color: #757575;
}

.cart {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 5px 0;
}

.remove-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remove-button:hover {
  background-color: #d32f2f;
}

.product-list-container {
  display: flex;
  justify-content: center; /* Центрируем список продуктов */
  margin-top: 20px; /* Отступ сверху для списка продуктов */
}

.product-list {
  display: flex;
  flex-wrap: wrap;
  list-style-type: none;
  padding: 0;
  justify-content: center; /* Центрируем элементы списка внутри контейнера */
}

.product-item {
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
  text-align: center;
  cursor: pointer;
  background-color: #fff;
  transition: box-shadow 0.3s ease;
}

.product-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.add-to-cart-button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-to-cart-button:hover {
  background-color: #757575;
}

/* Стили для модального окна */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
  z-index: 101;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.close-modal-button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.close-modal-button:hover {
  background-color: #757575;
}
</style>
