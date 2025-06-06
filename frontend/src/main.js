import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store' // Si estás usando Vuex o Pinia

// Importar Element Plus y sus estilos
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import locale from 'element-plus/lib/locale/lang/es' // Para español

// Configuración de axios para la conexión con Django
import axios from 'axios'
import VueAxios from 'vue-axios'

// Configuración global de axios
axios.defaults.baseURL = 'http://localhost:8000' // URL de tu backend Django
axios.defaults.withCredentials = true // Para manejar cookies de sesión si es necesario

// Crear la aplicación Vue
const app = createApp(App)

// Configurar plugins
app.use(ElementPlus, { locale })
app.use(VueAxios, axios)
app.provide('axios', app.config.globalProperties.axios) // Hacer axios disponible en la composición API
app.use(router)
app.use(store) // Si estás usando Vuex o Pinia

// Montar la aplicación
app.mount('#app')

// Configuración global de interceptores (opcional)
axios.interceptors.request.use(config => {
  // Añadir token de autenticación a cada petición
  const token = localStorage.getItem('token')
  if (token) {
    //usar esto si estás usando JWT:
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axios.interceptors.response.use(
  response => response,
  error => {
    // Manejar errores globales
    if (error.response.status === 401) {
      // Redirigir a login si no está autenticado
      router.push('/aunth/login')
    }
    return Promise.reject(error)
  }
)