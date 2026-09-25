import { useQuery } from '@tanstack/react-query'
import { workflowApi } from '../../../api/workflow'

export function useWorkflow(id: string | undefined) {
  return useQuery({
    queryKey: ['workflow', id],
    queryFn: () => workflowApi.getWorkflow(id!),
    enabled: !!id,
  })
}
