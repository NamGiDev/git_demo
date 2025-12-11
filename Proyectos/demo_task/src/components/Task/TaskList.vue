<script setup lang="ts">
import type { Task } from '@/models/task'
import http from '@/plugins/axios'
import { Button, Dialog, InputGroup, InputGroupAddon, InputText, Checkbox } from 'primevue'
import { computed, onMounted, ref } from 'vue'

// CAMBIO: ENDPOINT a 'tasks' o 'tareas'
const ENDPOINT = 'tasks'
const tasks = ref<Task[]>([]) // <-- CAMBIO: 'artistas' por 'tasks'
const taskDelete = ref<Task | null>(null) // <-- CAMBIO
const mostrarConfirmDialog = ref<boolean>(false)
const busqueda = ref<string>('')
const emit = defineEmits(['edit'])

const tasksFiltradas = computed(() => {
  // <-- CAMBIO
  // Filtramos por título o descripción
  return tasks.value.filter(
    (task) =>
      task.title.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      task.description.toLowerCase().includes(busqueda.value.toLowerCase()),
  )
})

async function obtenerLista() {
  // La API de Django devuelve una lista plana, la asignamos directamente
  tasks.value = await http.get(ENDPOINT).then((response) => response.data)
}

function emitirEdicion(task: Task) {
  // <-- CAMBIO
  emit('edit', task)
}

function mostrarEliminarConfirm(task: Task) {
  // <-- CAMBIO
  taskDelete.value = task // <-- CAMBIO
  mostrarConfirmDialog.value = true
}

async function eliminar() {
  await http.delete(`${ENDPOINT}/${taskDelete.value?.id}/`)
  obtenerLista()
  mostrarConfirmDialog.value = false
}

// NUEVO: Función para actualizar el estado al cambiar el checkbox
async function toggleCompletion(task: Task) {
  // Llama al PATCH con el estado invertido
  await http.patch(`${ENDPOINT}/${task.id}/`, { is_completed: !task.is_completed })
  obtenerLista()
}

onMounted(() => {
  obtenerLista()
})
defineExpose({ obtenerLista })
</script>

<template>
  <div>
    <div class="col-7 pl-0 mt-3">
      <InputGroup>
        <InputGroupAddon><i class="pi pi-search"></i></InputGroupAddon>
        <InputText v-model="busqueda" type="text" placeholder="Buscar por título o descripción" />
      </InputGroup>
    </div>

    <table class="w-full mt-4">
      <thead>
        <tr>
          <th>Estado</th>
          <th>Título</th>
          <th>Descripción</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasksFiltradas" :key="task.id">
          <td>
            <Checkbox :model-value="task.is_completed" @change="toggleCompletion(task)" />
          </td>
          <td :class="{ 'line-through text-gray-500': task.is_completed }">{{ task.title }}</td>
          <td :class="{ 'line-through text-gray-500': task.is_completed }">
            {{ task.description }}
          </td>
          <td>
            <Button icon="pi pi-pencil" aria-label="Editar" text @click="emitirEdicion(task)" />

            <Button
              icon="pi pi-trash"
              aria-label="Eliminar"
              text
              @click="mostrarEliminarConfirm(task)"
            />
          </td>
        </tr>
        <tr v-if="tasksFiltradas.length === 0">
          <td colspan="4" class="text-center">No se encontraron tareas.</td>
        </tr>
      </tbody>
    </table>

    <Dialog
      v-model:visible="mostrarConfirmDialog"
      header="Confirmar Eliminación"
      :style="{ width: '25rem' }"
    >
      <p>¿Estás seguro de que deseas eliminar la tarea **{{ taskDelete?.title }}**?</p>
      <div class="flex justify-end gap-2">
        <Button
          type="button"
          label="Cancelar"
          severity="secondary"
          @click="mostrarConfirmDialog = false"
        />
        <Button type="button" label="Eliminar" severity="danger" @click="eliminar" />
      </div>
    </Dialog>
  </div>
</template>
