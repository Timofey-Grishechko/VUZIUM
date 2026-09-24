import { useQuery } from '@tanstack/react-query'
import { adminApi } from '../../../api/admin'

export function useUsers() {
  return useQuery({
    queryKey: ['admin-users'],
    queryFn: () => adminApi.getUsers(),
    staleTime: 30_000,
  })
}
