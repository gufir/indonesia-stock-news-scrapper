<template>
    <header>
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
          <!-- Navbar Brand -->
          <router-link class="navbar-brand" to="/">
            News App</router-link>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
  
          <!-- Navbar Links -->
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <!-- Home Link -->
              <li class="nav-item">
                <router-link
                  class="nav-link"
                  to="/"
                  active-class="active-link"
                >Home</router-link>
              </li>
  
              <!-- Category with Popup Menu -->
              <li class="nav-item position-relative">
                <button
                  class="nav-link btn btn-link text-white"
                  @click="toggleCategoryPopup"
                  @blur="hideCategoryPopup"
                >
                  Category
                </button>
                <div
                  v-if="showCategoryPopup"
                  class="popup-menu"
                  tabindex="0"
                  @blur="hideCategoryPopup"
                >
                  <ul>
                    <li><router-link to="/category/technology">Technology</router-link></li>
                    <li><router-link to="/category/finance">Finance</router-link></li>
                    <li><router-link to="/category/healthcare">Healthcare</router-link></li>
                  </ul>
                </div>
              </li>
  
              <!-- About Link -->
              <li class="nav-item">
                <router-link
                  class="nav-link"
                  to="/about"
                  active-class="active-link"
                >About</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "Header",
    data() {
      return {
        showCategoryPopup: false, // Controls the visibility of the popup
      };
    },
    methods: {
      toggleCategoryPopup() {
        this.showCategoryPopup = !this.showCategoryPopup;
      },
      hideCategoryPopup() {
        // Delay hiding to allow a click on the popup itself
        setTimeout(() => {
          this.showCategoryPopup = false;
        }, 200);
      },
    },
  });
  </script>
  
  <style scoped>
  /* Styling for the popup menu with dark theme */
  .popup-menu {
    position: absolute;
    top: 100%; /* Align below the button */
    left: 0;
    z-index: 10;
    background-color: #343a40; /* Dark background */
    border: 1px solid #495057; /* Darker border */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    padding: 10px;
    width: 200px;
    color: #ffffff; /* White text */
  }
  
  .popup-menu ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  
  .popup-menu ul li {
    padding: 8px 10px;
  }
  
  .popup-menu ul li a {
    text-decoration: none;
    color: #ffffff; /* White text for links */
  }
  
  .popup-menu ul li a:hover {
    text-decoration: underline;
    color: #ffc107; /* Golden hover effect */
  }
  
  /* Navbar horizontal alignment */
  .navbar-nav {
    display: flex;
    gap: 20px; /* Space between items */
  }
  
  /* Active link styling */
  .active-link {
    color: #ffc107; /* Golden color for the active link */
    font-weight: bold;
  }

  .icon {
  width: 32px;  /* Ubah ukuran */
  height: 32px;
  margin-right: 8px;

}
  </style>