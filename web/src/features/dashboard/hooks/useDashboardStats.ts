import { useQuery } from '@tanstack/react-query'
import { workflowApi } from '../../../api/workflow'
import { catalogApi } from '../../../api/catalog'

export interface DashboardStats {
  totalUniversities: number
  activeWorkflows: number
  completedWorkflows: number
  overdueStages: number
  workflowsByStatus: { name: string; value: number }[]
  workflowsByDirection: { name: string; value: number }[]
  workflowDynamics: { date: string; count: number }[]
}

export function useDashboardStats() {
  return useQuery<DashboardStats>({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const [universities, workflows] = await Promise.all([
        catalogApi.getUniversities({ pageSize: 100 }),
        workflowApi.getWorkflows(),
      ])

      // Считаем метрики
      const activeWorkflows = workflows.filter(
        (w) => w.status === 'in_progress',
      ).length
      const completedWorkflows = workflows.filter(
        (w) => w.status === 'completed',
      ).length
      const overdueStages = workflows.filter((w) =>
        w.stages.some((s) => s.status === 'overdue'),
      ).length

      // Распределение по статусам
      const statusMap = new Map<string, number>()
      workflows.forEach((w) => {
        const label =
          w.status === 'in_progress'
            ? 'В работе'
            : w.status === 'completed'
              ? 'Завершён'
              : w.status === 'not_started'
                ? 'Не начат'
                : 'Просрочен'
        statusMap.set(label, (statusMap.get(label) ?? 0) + 1)
      })
      const workflowsByStatus = Array.from(statusMap.entries()).map(
        ([name, value]) => ({ name, value }),
      )

      // Распределение по направлениям
      const directionMap = new Map<string, number>()
      workflows.forEach((w) => {
        directionMap.set(
          w.directionName,
          (directionMap.get(w.directionName) ?? 0) + 1,
        )
      })
      const workflowsByDirection = Array.from(directionMap.entries()).map(
        ([name, value]) => ({ name, value }),
      )

      // Динамика за последние 8 недель (мок)
      const workflowDynamics = [
        { date: '01.09', count: 2 },
        { date: '08.09', count: 4 },
        { date: '15.09', count: 5 },
        { date: '22.09', count: 7 },
        { date: '29.09', count: 9 },
        { date: '06.10', count: 11 },
        { date: '13.10', count: 13 },
        { date: '20.10', count: 15 },
      ]

      return {
        totalUniversities: universities.total,
        activeWorkflows,
        completedWorkflows,
        overdueStages,
        workflowsByStatus,
        workflowsByDirection,
        workflowDynamics,
      }
    },
    staleTime: 60_000,
  })
}
