import type { Role, User } from '../../types/user'

export interface LoginOptions {
  role: Role
}

export interface AuthProvider {
  isAuthenticated: boolean
  login: (options: LoginOptions) => Promise<User>
  logout: () => Promise<void>
  getCurrentUser: () => Promise<User | null>
}

// === Мок-реализация ===
// Позже заменим на KeycloakAuthProvider без изменения интерфейса.
const demoUsers: Record<Role, User> = {
  user: {
    id: '1',
    keycloakId: 'demo-user',
    fio: 'Иван Пользователь',
    email: 'user@rtk.ru',
    role: 'user',
    active: true,
    universityIds: [],
  },
  manager: {
    id: '2',
    keycloakId: 'demo-manager',
    fio: 'Коля Тестов',
    email: 'manager@rtk.ru',
    role: 'manager',
    active: true,
    universityIds: [],
  },
  admin: {
    id: '3',
    keycloakId: 'demo-admin',
    fio: 'Админ Системы',
    email: 'admin@rtk.ru',
    role: 'admin',
    active: true,
    universityIds: [],
  },
}

export const mockAuthProvider: AuthProvider = {
  isAuthenticated: false,

  async login({ role }: LoginOptions): Promise<User> {
    // имитация сетевого запроса
    await new Promise((resolve) => setTimeout(resolve, 500))
    return demoUsers[role]
  },

  async logout(): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, 200))
  },

  async getCurrentUser(): Promise<User | null> {
    return null
  },
}

export const authProvider: AuthProvider = mockAuthProvider
