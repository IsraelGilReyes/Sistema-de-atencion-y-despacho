<!--Modales-->
<script lang="ts" setup>
import type { NotificationItem } from '@vben/layouts';

import { computed, ref, watch } from 'vue';

import { AuthenticationLoginExpiredModal } from '@vben/common-ui';
import { VBEN_DOC_URL, VBEN_GITHUB_URL } from '@vben/constants';
import { useWatermark } from '@vben/hooks';
import { MdiAccount, CircleHelp, MdiGithub, MdiShieldCheck, MdiSquareEditOutline } from '@vben/icons';
import {
  BasicLayout,
  LockScreen,
  Notification, 
  UserDropdown,
} from '@vben/layouts';
import { preferences } from '@vben/preferences';
import { useAccessStore, useUserStore } from '@vben/stores';
import { openWindow } from '@vben/utils';

import { $t } from '#/locales';
import { useAuthStore } from '#/store';
import LoginForm from '#/views/_core/authentication/login.vue';

// Estado del modal personalizado de Información
const mostrarModalInformacion = ref(false);
const mostrarModalActualizarContrasena = ref(false);


const notifications = ref<NotificationItem[]>([
  {
    avatar: 'https://avatar.vercel.sh/vercel.svg?text=VB',
    date: '3小时前',
    isRead: true,
    message: '描述信息描述信息描述信息',
    title: '收到了 14 份新周报',
  },
  {
    avatar: 'https://avatar.vercel.sh/1',
    date: '刚刚',
    isRead: false,
    message: '描述信息描述信息描述信息',
    title: '朱偏右 回复了你',
  },
  {
    avatar: 'https://avatar.vercel.sh/1',
    date: '2024-01-01',
    isRead: false,
    message: '描述信息描述信息描述信息',
    title: '曲丽丽 评论了你',
  },
  {
    avatar: 'https://avatar.vercel.sh/satori',
    date: '1天前',
    isRead: false,
    message: '描述信息描述信息描述信息',
    title: '代办提醒',
  },
]);

const userStore = useUserStore();
const authStore = useAuthStore();
const accessStore = useAccessStore();
const { destroyWatermark, updateWatermark } = useWatermark();
const showDot = computed(() =>
  notifications.value.some((item) => !item.isRead),
);

const menus = computed(() => [
 {
    handler: () => {
      mostrarModalInformacion.value = true;
    },
    icon: MdiAccount,
    text: $t('Perfil'),
  },
  {
    handler: () => {
      mostrarModalActualizarContrasena.value = true;
    },
    icon: MdiShieldCheck,
    text: 'Contraseña',
  },
  {
    handler: () => {
      openWindow(`${VBEN_GITHUB_URL}/issues`, {
        target: '_blank',
      });
    },
    icon: MdiSquareEditOutline,
    text: $t('Editar Perfil'),
  },
]);

const avatar = computed(() => {
  return userStore.userInfo?.avatar ?? preferences.app.defaultAvatar;
});

async function handleLogout() {
  await authStore.logout(false);
}

function handleNoticeClear() {
  notifications.value = [];
}

function handleMakeAll() {
  notifications.value.forEach((item) => (item.isRead = true));
}
watch(
  () => preferences.app.watermark,
  async (enable) => {
    if (enable) {
      await updateWatermark({
        content: `${userStore.userInfo?.username} - ${userStore.userInfo?.realName}`,
      });
    } else {
      destroyWatermark();
    }
  },
  {
    immediate: true,
  },
);
</script>

<template>
  <BasicLayout @clear-preferences-and-logout="handleLogout">
    <template #user-dropdown>
      <UserDropdown
        :avatar
        :menus
        :text="userStore.userInfo?.realName"
        description="marilyn.lucero@gmail.com"
        tag-text="Pro"
        @logout="handleLogout"
      />
    </template>
    <template #notification>
      <Notification
        :dot="showDot"
        :notifications="notifications"
        @clear="handleNoticeClear"
        @make-all="handleMakeAll"
      />
    </template>
    <template #extra>
      <AuthenticationLoginExpiredModal
        v-model:open="accessStore.loginExpired"
        :avatar
      >
        <LoginForm />
      </AuthenticationLoginExpiredModal>
<!--Modal de informacion-->
  <!--Modal de informacion-->
<div
  v-if="mostrarModalInformacion"
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
>
  <div class="bg-[#1e1e2f] p-6 rounded-lg shadow-lg w-[90%] max-w-md text-center text-white">
    <img
      :src="userStore.userInfo?.avatar ?? preferences.app.defaultAvatar"
      alt="Avatar del usuario"
      class="w-24 h-24 rounded-full mx-auto mb-4 border-4 border-blue-500"
    />

    <h2 class="text-2xl font-bold mb-4">Mi Perfil</h2>

    <div class="space-y-2 text-left text-gray-200">
      <p><span class="font-semibold">Nombre completo:</span> {{ userStore.userInfo?.realName }}</p>
      <p><span class="font-semibold">Correo electrónico:</span> {{ userStore.userInfo?.email ?? 'marilyn.lucero@gmail.com' }}</p>
      <p><span class="font-semibold">Número de teléfono:</span> {{ userStore.userInfo?.phone ?? 'No registrado' }}</p>
      <p><span class="font-semibold">Rol:</span> {{ userStore.userInfo?.role ?? 'Usuario' }}</p>
    </div>

    <div class="mt-6 text-right">
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        @click="mostrarModalInformacion = false"
      >
        Cerrar
      </button>
    </div>
  </div>
</div>


<!-- Modal Actualizar Contraseña -->
<!-- Modal Actualizar Contraseña -->
<div
  v-if="mostrarModalActualizarContrasena"
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
>
  <div class="bg-[#1e1e2f] p-6 rounded-lg shadow-lg w-[90%] max-w-md text-white">
    <h2 class="text-2xl font-bold mb-6 text-center">Actualizar Contraseña</h2>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-300 mb-1">Contraseña actual</label>
        <input
          type="password"
          placeholder="Contraseña actual"
          class="w-full bg-[#2e2e40] text-white border border-gray-600 rounded px-3 py-2 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-300 mb-1">Nueva contraseña</label>
        <input
          type="password"
          placeholder="Nueva contraseña"
          class="w-full bg-[#2e2e40] text-white border border-gray-600 rounded px-3 py-2 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-300 mb-1">Confirmar contraseña</label>
        <input
          type="password"
          placeholder="Confirmar nueva contraseña"
          class="w-full bg-[#2e2e40] text-white border border-gray-600 rounded px-3 py-2 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div class="text-right mt-4">
        <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
          Guardar Cambios
        </button>
      </div>

      <div class="text-center mt-2">
        <a href="#" class="text-blue-400 hover:underline text-sm">Olvidé mi contraseña</a>
      </div>
    </div>

    <div class="text-right mt-6">
      <button
        class="text-sm text-gray-400 hover:text-white transition"
        @click="mostrarModalActualizarContrasena = false"
      >
        Cerrar
      </button>
    </div>
  </div>
</div>


    </template>
    <template #lock-screen>
      <LockScreen :avatar @to-login="handleLogout" />
    </template>
  </BasicLayout>
</template>
