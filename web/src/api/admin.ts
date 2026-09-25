import type { Role, User } from '../types/user'

// Мок-данные пользователей
const MOCK_USERS: User[] = [
  {
    id: '1',
    keycloakId: 'u-1',
    fio: 'Коля Тестов',
    email: 'kolya@rtk.ru',
    role: 'manager',
    active: true,
    universityIds: ['1', '2', '4'],
  },
  {
    id: '2',
    keycloakId: 'u-2',
    fio: 'Мария РТК',
    email: 'maria@rtk.ru',
    role: 'manager',
    active: true,
    universityIds: ['3', '5'],
  },
  {
    id: '3',
    keycloakId: 'u-3',
    fio: 'Иван Пользователь',
    email: 'ivan@rtk.ru',
    role: 'user',
    active: true,
    universityIds: ['1'],
  },
  {
    id: '4',
    keycloakId: 'u-4',
    fio: 'Админ Системы',
    email: 'admin@rtk.ru',
    role: 'admin',
    active: true,
    universityIds: [],
  },
  {
    id: '5',
    keycloakId: 'u-5',
    fio: 'Пётр Ушедший',
    email: 'petr@rtk.ru',
    role: 'user',
    active: false,
    universityIds: [],
  },
]

export const adminApi = {
  async getUsers(): Promise<User[]> {
    await new Promise((r) => setTimeout(r, 200))
    return [...MOCK_USERS]
  },

  async updateUserRole(userId: string, role: Role): Promise<void> {
    await new Promise((r) => setTimeout(r, 300))
    const user = MOCK_USERS.find((u) => u.id === userId)
    if (user) user.role = role
  },

  async toggleUserActive(userId: string): Promise<void> {
    await new Promise((r) => setTimeout(r, 300))
    const user = MOCK_USERS.find((u) => u.id === userId)
    if (user) user.active = !user.active
  },

  async updateAccessScope(userId: string, universityIds: string[]): Promise<void> {
    await new Promise((r) => setTimeout(r, 300))
    const user = MOCK_USERS.find((u) => u.id === userId)
    if (user) user.universityIds = universityIds
  },
}
