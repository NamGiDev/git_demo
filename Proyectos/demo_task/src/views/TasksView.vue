<script setup lang="ts">
// <-- CAMBIO: ArtistaList/Save por TaskList/Save
import { ref } from 'vue'
import TaskList from '@/components/Task/TaskList.vue'
import TaskSave from '@/components/Task/TaskSave.vue'
import { Button } from 'primevue'
import type { Task } from '@/models/task'

const mostrarDialog = ref(false)
// <-- CAMBIO: artistaListRef por taskListRef, ArtistaList por TaskList
const taskListRef = ref<typeof TaskList | null>(null)
// <-- CAMBIO: artistaEdit por taskEdit, any por Task
const taskEdit = ref<Task | null>(null)

function handleCreate() {
  taskEdit.value = null // <-- CAMBIO
  mostrarDialog.value = true
}

function handleEdit(task: Task) {
  // <-- CAMBIO: recibe Task
  taskEdit.value = task // <-- CAMBIO
  mostrarDialog.value = true
}

function handleCloseDialog() {
  mostrarDialog.value = false
}

function handleGuardar() {
  // Llama al método 'obtenerLista' expuesto por TaskList.vue
  taskListRef.value?.obtenerLista()
}
</script>

<template>
  <div class="mx-2 mt-6 md:m-7">
    <h2>Gestión de Tareas</h2>
    <Button label="Crear Nueva Tarea" icon="pi pi-plus" @click="handleCreate" />

    <TaskList ref="taskListRef" @edit="handleEdit" />

    <TaskSave
      :mostrar="mostrarDialog"
      :task="taskEdit"
      :modoEdicion="!!taskEdit"
      @guardar="handleGuardar"
      @close="handleCloseDialog"
    />
  </div>
</template>
