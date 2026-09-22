export type Role = 'user' | 'manager' | 'admin'

export interface User {
  id: string
  keycloakId: string
  fio: string
  email: string
  role: Role
  active: boolean
  universityIds: string[]
}
