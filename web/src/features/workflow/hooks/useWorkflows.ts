import { useQuery } from '@tanstack/react-query'
import { workflowApi } from '../../../api/workflow'
import type { WorkflowFilters } from '../../../api/workflow'

export function useWorkflows(filters: WorkflowFilters = {}) {
  return useQuery({
    queryKey: ['workflows', filters],
    queryFn: () => workflowApi.getWorkflows(filters),
    staleTime: 30_000,
  })
}
