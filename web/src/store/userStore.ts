import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Role, User } from '../types/user'

interface UserState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  setUser: (user: User | null) => void
  setToken: (token: string | null) => void
  logout: () => void
  hasRole: (roles: Role[]) => boolean
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      setUser: (user) => set({ user, isAuthenticated: !!user }),

      setToken: (token) => {
        set({ token })
        if (token) localStorage.setItem('access_token', token)
        else localStorage.removeItem('access_token')
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false })
        localStorage.removeItem('access_token')
      },

      hasRole: (roles) => {
        const user = get().user
        return user ? roles.includes(user.role) : false
      },
    }),
    {
      name: 'user-store',
    },
  ),
)
