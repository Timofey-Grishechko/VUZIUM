import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useUserStore } from '../store/userStore'
import type { Role } from '../types/user'

interface RoleGuardProps {
  roles: Role[]
}

export function ProtectedRoute() {
  const isAuthenticated = useUserStore((s) => s.isAuthenticated)
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <Outlet />
}

export function RoleGuard({ roles }: RoleGuardProps) {
  const hasRole = useUserStore((s) => s.hasRole)

  if (!hasRole(roles)) {
    return <Navigate to="/" replace />
  }

  return <Outlet />
}
