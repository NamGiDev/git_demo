export interface Task {
  id?: number // ID autogenerado (opcional al crear)
  title: string
  description: string
  is_completed: boolean
}
