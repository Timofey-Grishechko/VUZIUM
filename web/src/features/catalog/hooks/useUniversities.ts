import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { catalogApi } from '../../../api/catalog'
import type { UniversityFilters } from '../../../api/catalog'

export function useUniversities(filters: UniversityFilters) {
  return useQuery({
    queryKey: ['universities', filters],
    queryFn: () => catalogApi.getUniversities(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  })
}
