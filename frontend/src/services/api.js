import axios from 'axios'
import router from '@/router'

const api = axios.create({
    baseURL: 'http://localhost:8000',  //Asegúrate que coincide con el puerto de Django
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true // Importante para cookies HttpOnly
})

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            // Redirigir al login si no está autenticado
            router.push('/auth/login')
        }
        return Promise.reject(error)
    }
)

export const authAPI = {
    async login(credentials) {
        try {
            const response = await api.post('/api/auth/login/', credentials)
            return response.data
        } catch (error) {
            throw {
                message: error.response?.data?.message || 'Error al iniciar sesión',
                status: error.response?.status
            }
        }
    },

    async logout() {
        try {
            const response = await api.post('/api/auth/logout/')
            return response.data
        } catch (error) {
            throw {
                message: error.response?.data?.message || 'Error al cerrar sesión',
                status: error.response?.status
            }
        }
    },

    async getUserInfo() {
        try {
            const response = await api.get('/api/auth/info/')
            return response.data.user
        } catch (error) {
            throw {
                message: error.response?.data?.message || 'Error al obtener información del usuario',
                status: error.response?.status
            }
        }
    }
}

export const userAPI = {
    async getUsers() {
        const response = await api.get('/api/auth/list/')
        return response.data
    },

    async createUser(userData) {
        const response = await api.post('/api/auth/create/', userData)
        return response.data
    }
}

export const roleAPI = {
    async getRoles() {
        const response = await api.get('/api/auth/roles/')
        return response.data
    },

    async createRole(roleData) {
        const response = await api.post('/api/auth/roles/create/', roleData)
        return response.data
    },

    async getUserRoles() {
        const response = await api.get('/api/auth/roles/user/')
        return response.data
    },

    async assignRole(roleAssignment) {
        const response = await api.post('/api/auth/roles/assign/', roleAssignment)
        return response.data
    }
}

export default api