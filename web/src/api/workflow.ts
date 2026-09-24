import type { StageExtended, StageKey, StageStatus, WorkflowExtended } from '../types/domain'
import { STAGE_LABELS, STAGE_ORDER } from '../types/domain'

// Генератор этапов для одного workflow
function buildStages(workflowId: string, completedCount: number): StageExtended[] {
  return STAGE_ORDER.map((key, index): StageExtended => {
    let status: StageStatus = 'not_started'
    if (index < completedCount) status = 'completed'
    else if (index === completedCount) status = 'in_progress'

    return {
      id: `${workflowId}-${index}`,
      workflowId,
      key,
      order: index,
      name: STAGE_LABELS[key],
      status,
      comment: status === 'completed' ? 'Этап завершён' : undefined,
    }
  })
}

const MOCK_WORKFLOWS: WorkflowExtended[] = [
  {
    id: '1',
    universityId: '1',
    universityName: 'МГУ им. М.В. Ломоносова',
    directionId: '3',
    directionName: 'Backend',
    productId: '1',
    productName: 'Яндекс Практикум Backend',
    managerId: '2',
    managerName: 'Коля Тестов',
    status: 'in_progress',
    createdAt: '2026-09-01',
    updatedAt: '2026-09-20',
    stages: buildStages('1', 5),
  },
  {
    id: '2',
    universityId: '2',
    universityName: 'СПбГУ',
    directionId: '4',
    directionName: 'Frontend',
    productId: '2',
    productName: 'Яндекс Практикум Frontend',
    managerId: '2',
    managerName: 'Коля Тестов',
    status: 'in_progress',
    createdAt: '2026-09-03',
    updatedAt: '2026-09-21',
    stages: buildStages('2', 9),
  },
  {
    id: '3',
    universityId: '3',
    universityName: 'МФТИ',
    directionId: '5',
    directionName: 'Data Science',
    productId: '3',
    productName: 'Сбер DS Academy',
    managerId: '3',
    managerName: 'Мария РТК',
    status: 'in_progress',
    createdAt: '2026-09-05',
    updatedAt: '2026-09-22',
    stages: buildStages('3', 2),
  },
  {
    id: '4',
    universityId: '4',
    universityName: 'НИУ ВШЭ',
    directionId: '6',
    directionName: 'Mobile',
    productId: '4',
    productName: 'VK Mobile Bootcamp',
    managerId: '2',
    managerName: 'Коля Тестов',
    status: 'completed',
    createdAt: '2026-08-15',
    updatedAt: '2026-09-15',
    stages: buildStages('4', 14),
  },
  {
    id: '5',
    universityId: '5',
    universityName: 'ИТМО',
    directionId: '1',
    directionName: 'DevOps',
    productId: '6',
    productName: 'RTK DevOps Platform',
    managerId: '3',
    managerName: 'Мария РТК',
    status: 'in_progress',
    createdAt: '2026-09-10',
    updatedAt: '2026-09-23',
    stages: buildStages('5', 7),
  },
  {
    id: '6',
    universityId: '6',
    universityName: 'НГУ',
    directionId: '7',
    directionName: 'Information Security',
    productId: '7',
    productName: 'Kaspersky Security',
    managerId: '2',
    managerName: 'Коля Тестов',
    status: 'not_started',
    createdAt: '2026-09-18',
    updatedAt: '2026-09-18',
    stages: buildStages('6', 0),
  },
]

export interface WorkflowFilters {
  search?: string
  managerId?: string
  directionId?: string
}

export const workflowApi = {
  async getWorkflows(filters: WorkflowFilters = {}): Promise<WorkflowExtended[]> {
    await new Promise((r) => setTimeout(r, 250))
    let items = [...MOCK_WORKFLOWS]
    if (filters.search) {
      const q = filters.search.toLowerCase()
      items = items.filter(
        (w) =>
          w.universityName.toLowerCase().includes(q) ||
          w.productName.toLowerCase().includes(q),
      )
    }
    if (filters.managerId) items = items.filter((w) => w.managerId === filters.managerId)
    if (filters.directionId) items = items.filter((w) => w.directionId === filters.directionId)
    return items
  },

  async getWorkflow(id: string): Promise<WorkflowExtended | null> {
    await new Promise((r) => setTimeout(r, 200))
    return MOCK_WORKFLOWS.find((w) => w.id === id) ?? null
  },

  async transitionStage(
    workflowId: string,
    stageId: string,
    toStatus: StageStatus,
    comment?: string,
  ): Promise<void> {
    await new Promise((r) => setTimeout(r, 300))
    // TODO: при подключении бэка — POST /workflows/{id}/stages/{stageId}/transition
    console.log('[mock] transition', { workflowId, stageId, toStatus, comment })
  },
}

// Экспортируем для использования в канбане
export { STAGE_ORDER, STAGE_LABELS }
export type { StageKey, StageStatus }
