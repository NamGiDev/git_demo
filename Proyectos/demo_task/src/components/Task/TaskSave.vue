<script setup lang="ts">
import type { Task } from '@/models/task' // <-- CAMBIO: Artista por Task
import http from '@/plugins/axios'
import { Button, Dialog, InputText, Textarea, Checkbox } from 'primevue' // Agregamos Checkbox
import { computed, ref, watch } from 'vue'

// CAMBIO: ENDPOINT a 'tasks' o 'tareas'
const ENDPOINT = 'tasks'

const props = defineProps({
  mostrar: Boolean,
  task: {
    // <-- CAMBIO: 'artista' por 'task'
    type: Object as () => Task,
    default: () => ({ is_completed: false }) as Task, // Inicializamos is_completed
  },
  modoEdicion: Boolean,
})
const emit = defineEmits(['guardar', 'close'])

const dialogVisible = computed({
  get: () => props.mostrar,
  set: (value) => {
    if (!value) emit('close')
  },
})

const task = ref<Task>({ ...props.task }) // <-- CAMBIO: 'artista' por 'task'
watch(
  () => props.task, // <-- CAMBIO: 'props.artista' por 'props.task'
  (newVal) => {
    task.value = { ...newVal }
  },
)

async function handleSave() {
  try {
    const body = {
      title: task.value.title, // <-- CAMBIO: nombre por title
      description: task.value.description, // <-- CAMBIO: nacionalidad/fotografia por description
      is_completed: task.value.is_completed, // <-- NUEVO: campo de estado
    }

    if (props.modoEdicion) {
      await http.patch(`${ENDPOINT}/${task.value.id}/`, body) // PATCH
    } else {
      await http.post(`${ENDPOINT}/`, body) // POST
    }

    emit('guardar')
    task.value = {} as Task
    dialogVisible.value = false
  } catch (error: any) {
    if (error.response && error.response.data) {
      console.error('Detalle del Error de Django:', error.response.data)
      alert('Error al guardar: Verifique la consola para detalles.')
    } else {
      alert('Error desconocido al guardar.')
    }
  }
}
</script>

<template>
  <div class="card flex justify-center">
    <Dialog
      v-model:visible="dialogVisible"
      :header="props.modoEdicion ? 'Editar Tarea' : 'Crear Tarea'"
      style="width: 25rem"
    >
      <div class="flex items-center gap-4 mb-4">
        <label for="title" class="font-semibold w-3">Título</label>
        <InputText id="title" v-model="task.title" class="flex-auto" autocomplete="off" autofocus />
      </div>

      <div class="flex items-center gap-4 mb-4">
        <label for="description" class="font-semibold w-3">Descripción</label>
        <Textarea
          id="description"
          v-model="task.description"
          class="flex-auto"
          autocomplete="off"
          rows="4"
        />
      </div>

      <div class="flex items-center gap-4 mb-4">
        <label for="completed" class="font-semibold w-3">Completada</label>
        <Checkbox id="completed" v-model="task.is_completed" :binary="true" />
      </div>

      <div class="flex justify-end gap-2">
        <Button
          type="button"
          label="Cancelar"
          icon="pi pi-times"
          severity="secondary"
          @click="dialogVisible = false"
        ></Button>
        <Button type="button" label="Guardar" icon="pi pi-save" @click="handleSave"></Button>
      </div>
    </Dialog>
  </div>
</template>
