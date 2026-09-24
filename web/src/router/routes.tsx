import { Navigate } from 'react-router-dom'
import type { RouteObject } from 'react-router-dom'

import AppLayout from '../components/layout/AppLayout'
import DashboardPage from '../pages/DashboardPage'
import LoginPage from '../pages/LoginPage'
import NotFoundPage from '../pages/NotFoundPage'
import UniversitiesPage from '../pages/UniversitiesPage'
import DirectionsPage from '../pages/DirectionsPage'
import VendorsPage from '../pages/VendorsPage'
import ProductsPage from '../pages/ProductsPage'
import ResponsiblesPage from '../pages/ResponsiblesPage'
import WorkflowsPage from '../pages/WorkflowsPage'

import { ProtectedRoute } from './guards'

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
          { path: '/universities', element: <UniversitiesPage /> },
          { path: '/directions', element: <DirectionsPage /> },
          { path: '/vendors', element: <VendorsPage /> },
          { path: '/products', element: <ProductsPage /> },
          { path: '/responsibles', element: <ResponsiblesPage /> },
          { path: '/workflows', element: <WorkflowsPage /> },
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
