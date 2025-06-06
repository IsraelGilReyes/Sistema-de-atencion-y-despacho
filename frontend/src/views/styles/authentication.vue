<script setup lang="ts">
import type { ToolbarType } from './types';

import { preferences, usePreferences } from '@vben/preferences';

import { Copyright } from '../basic/copyright';
import AuthenticationFormView from './form.vue';
import SloganIcon from './icons/slogan.vue';
import Toolbar from './toolbar.vue';

interface Props {
  appName?: string;
  logo?: string;
  pageTitle?: string;
  pageDescription?: string;
  sloganImage?: string;
  toolbar?: boolean;
  copyright?: boolean;
  toolbarList?: ToolbarType[];
  clickLogo?: () => void;
}

withDefaults(defineProps<Props>(), {
  appName: '',
  copyright: true,
  logo: '',
  pageDescription: '',
  pageTitle: '',
  sloganImage: '',
  toolbar: true,
  toolbarList: () => ['color', 'language', 'layout', 'theme'],
  clickLogo: () => {},
});

const { authPanelCenter, authPanelLeft, authPanelRight, isDark } =
  usePreferences();
</script>

<template>
  <div
    :class="[isDark ? 'dark' : '']"
    class="min-h-screen w-full select-none overflow-x-hidden"
  >
    <!-- 头部 Logo 和应用名称 -->
    <div
      v-if="logo || appName"
      class="absolute left-0 top-0 z-10 flex flex-1"
      @click="clickLogo"
    >
      <div
        class="text-foreground lg:text-foreground ml-4 mt-4 flex flex-1 items-center sm:left-6 sm:top-6"
      >
        <img v-if="logo" :alt="appName" :src="logo" class="mr-2" width="42" />
        <p v-if="appName" class="m-0 text-xl font-medium">
          {{ appName }}
        </p>
      </div>
    </div>

    <!-- Pantalla de bienvenida con login arriba -->
    <div v-if="!authPanelCenter" class="relative w-full flex-1 block">
      <div class="auth-welcome-bg min-h-screen w-full flex flex-col items-center pt-12">
        <div class="login-background absolute left-0 top-0 size-full"></div>
        <div class="w-full flex justify-center relative z-10">
          <AuthenticationFormView
            class="md:bg-background shadow-primary/5 shadow-float w-full max-w-md rounded-3xl pb-12"
          >
            <template v-if="copyright" #copyright>
              <slot name="copyright">
                <Copyright
                  v-if="preferences.copyright.enable"
                  v-bind="preferences.copyright"
                />
              </slot>
            </template>
          </AuthenticationFormView>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-background {
  background: transparent;
  filter: none;
}

.dark {
  .login-background {
    background: linear-gradient(
      154deg,
rgba(23, 22, 29, 0.08) 30%,
      hsl(var(--primary) / 20%) 48%,
rgba(9, 9, 59, 0.08) 64%
    );
    filter: blur(100px);
  }
}

.auth-welcome-bg {
  min-height: 100vh;
  min-width: 100vw;
  background: linear-gradient(135deg,rgb(15, 18, 19) 0%, #2c5364 50%,rgb(3, 15, 18) 100%);
  /* Fondo degradado azul profesional */
}
</style>
