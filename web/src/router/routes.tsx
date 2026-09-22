import { Navigate } from 'react-router-dom'
import type { RouteObject } from 'react-router-dom'

import AppLayout from '../components/layout/AppLayout.tsx'
import DashboardPage from '../pages/DashboardPage.tsx'
import LoginPage from '../pages/LoginPage.tsx'
import NotFoundPage from '../pages/NotFoundPage.tsx'

import { ProtectedRoute, RoleGuard } from './guards'

export const routes: RouteObject[] = [
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { path: '/', element: <DashboardPage /> },
          // Пример с ограничением по роли:
          // {
          //   element: <RoleGuard roles={['admin']} />,
          //   children: [{ path: '/admin/users', element: <AdminUsersPage /> }],
          // },
        ],
      },
    ],
  },
  {
    path: '/404',
    element: <NotFoundPage />,
  },
  {
    path: '*',
    element: <Navigate to="/404" replace />,
  },
]
