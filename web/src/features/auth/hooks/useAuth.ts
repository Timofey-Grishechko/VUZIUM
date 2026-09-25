import { useCallback, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authProvider } from '../authProvider'
import { useUserStore } from '../../../store/userStore'
import type { Role } from '../../../types/user'

export function useAuth() {
  const navigate = useNavigate()
  const setUser = useUserStore((s) => s.setUser)
  const setToken = useUserStore((s) => s.setToken)
  const logoutStore = useUserStore((s) => s.logout)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const login = useCallback(
    async (role: Role) => {
      setLoading(true)
      setError(null)
      try {
        const user = await authProvider.login({ role })
        setUser(user)
        setToken('mock-token-' + user.id)
        navigate('/', { replace: true })
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Ошибка входа')
      } finally {
        setLoading(false)
      }
    },
    [navigate, setUser, setToken],
  )

  const logout = useCallback(async () => {
    await authProvider.logout()
    logoutStore()
    navigate('/login', { replace: true })
  }, [navigate, logoutStore])

  return { login, logout, loading, error }
}
