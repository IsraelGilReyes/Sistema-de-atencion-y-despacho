import AuthService from '@/services/auth.service';

export const auth = {
    namespaced: true,
    state: {
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            state.isAuthenticated = !!user;
        },
        SET_LOADING(state, loading) {
            state.loading = loading;
        },
        SET_ERROR(state, error) {
            state.error = error;
        },
        CLEAR_ERROR(state) {
            state.error = null;
        }
    },
    actions: {
        async login({ commit }, { username, password }) {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');
            try {
                const response = await AuthService.login(username, password);
                commit('SET_USER', response.user);
                return response;
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            } finally {
                commit('SET_LOADING', false);
            }
        },

        async logout({ commit }) {
            try {
                await AuthService.logout();
                commit('SET_USER', null);
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            }
        },

        async getUserInfo({ commit }) {
            try {
                const user = await AuthService.getUserInfo();
                commit('SET_USER', user);
                return user;
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            }
        },

        clearError({ commit }) {
            commit('CLEAR_ERROR');
        }
    },
    getters: {
        isAuthenticated: state => state.isAuthenticated,
        currentUser: state => state.user,
        loading: state => state.loading,
        error: state => state.error
    }
}; 