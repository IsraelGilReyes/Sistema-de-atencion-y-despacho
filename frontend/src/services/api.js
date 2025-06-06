import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000',  //Asegúrate que coincide con el puerto de Django
    headers: {
        'Content-Type': 'application/json',
    }
})

// Interceptor para añadir token a las peticiones
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Token ${token}`
    }
    return config
})

export default {
    login(credentials) {
        return api.post('/autenticacion/api/login/', credentials)
    },
    // Añade más endpoints según necesites
}