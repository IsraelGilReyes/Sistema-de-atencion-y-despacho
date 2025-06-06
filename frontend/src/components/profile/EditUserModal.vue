<!--Modal para editar informacion del usuario-->
<template>
  <VbenModal
    v-model:visible="visible"
    title="Editar información del usuario"
    @confirm="handleConfirm"
    @cancel="visible = false"
  >
    <form class="space-y-4">
      <div>
        <label class="block">Nombre</label>
        <input
          v-model="editedUser.name"
          class="input"
          type="text"
          placeholder="Nombre"
        />
      </div>
      <div>
        <label class="block">Descripción</label>
        <input
          v-model="editedUser.description"
          class="input"
          type="text"
          placeholder="Descripción"
        />
      </div>
    </form>
  </VbenModal>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  visible: boolean;
  userData: {
    name: string;
    description: string;
  };
}>();

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'save', data: { name: string; description: string }): void;
}>();

const editedUser = ref({ name: '', description: '' });

watch(
  () => props.userData,
  (newVal) => {
    editedUser.value = { ...newVal };
  },
  { immediate: true }
);

watch(
  () => props.visible,
  (val) => {
    if (!val) editedUser.value = { ...props.userData };
  }
);

const visible = defineModel<boolean>('visible');

function handleConfirm() {
  emit('save', editedUser.value);
  emit('update:visible', false);
}
</script>

<style scoped>
.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
}
</style>
