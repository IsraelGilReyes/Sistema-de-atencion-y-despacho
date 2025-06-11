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
import { authAPI } from './services/api'

// Configuración global de axios
axios.defaults.baseURL = 'http://localhost:8000' // URL del backend Django
axios.defaults.withCredentials = true // Necesario para cookies HttpOnly

// Variables para manejar la renovación de tokens
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error)
        } else {
            prom.resolve()
        }
    })
    failedQueue = []
}

// Interceptor de respuestas
axios.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        // Si el error es 401 y no hemos intentado renovar el token
        if (error.response?.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                // Si ya estamos renovando el token, añadir a la cola
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject })
                }).then(() => {
                    return axios(originalRequest)
                }).catch(err => {
                    return Promise.reject(err)
                })
            }

            originalRequest._retry = true
            isRefreshing = true

            try {
                // Intentar renovar el token
                await authAPI.refreshToken()
                processQueue(null)
                return axios(originalRequest)
            } catch (refreshError) {
                processQueue(refreshError)
                // Si falla la renovación, redirigir al login
                router.push('/auth/login')
                return Promise.reject(refreshError)
            } finally {
                isRefreshing = false
            }
        }

        return Promise.reject(error)
    }
)

// Crear la aplicación Vue
const app = createApp(App)

// Configurar plugins
app.use(ElementPlus, { locale })
app.use(VueAxios, axios)
app.use(router)
app.use(store) // Si estás usando Vuex o Pinia

// Montar la aplicación
app.mount('#app')