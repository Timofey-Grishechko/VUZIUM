export type WorkflowStatus =
  | 'not_started'
  | 'in_progress'
  | 'completed'
  | 'overdue'

export interface University {
  id: string
  name: string
  region?: string
  status: 'active' | 'inactive'
  managerId?: string
  responsibleFromVuz?: string
  comment?: string
}

export interface Vendor {
  id: string
  name: string
}

export interface ITDirection {
  id: string
  name: string
}

export interface ITProduct {
  id: string
  vendorId: string
  directionId: string
  name: string
  description?: string
}

export interface License {
  id: string
  productId: string
  universityId: string
  contractNumber: string
  signedAt: string
  expiresAt: string
  transferStatus: string
}

export interface Responsible {
  id: string
  universityId: string
  fio: string
  email?: string
  phone?: string
  side: 'school' | 'vuz'
}

export interface Stage {
  id: string
  workflowId: string
  order: number
  name: string
  status: WorkflowStatus
  assigneeId?: string
  deadline?: string
  comment?: string
}

export interface StageTransition {
  id: string
  stageId: string
  fromStatus: WorkflowStatus
  toStatus: WorkflowStatus
  userId: string
  comment?: string
  createdAt: string
}

export interface Attachment {
  id: string
  stageId: string
  filename: string
  mime: string
  size: number
  url: string
  uploadedBy: string
  createdAt: string
}

export interface Workflow {
  id: string
  universityId: string
  directionId: string
  productId: string
  managerId: string
  status: WorkflowStatus
  createdAt: string
  updatedAt: string
  stages: Stage[]
  
}

// === Этапы workflow (14 шагов из ТЗ) ===
export type StageKey =
  | 'contacts'
  | 'communication'
  | 'meeting'
  | 'documents_exchange'
  | 'documents_correction'
  | 'documents_signing'
  | 'materials_transfer'
  | 'product_implementation'
  | 'teachers_training'
  | 'program_update'
  | 'classes'
  | 'docs_actualization'
  | 'teachers_upskilling'
  | 'control'

export const STAGE_LABELS: Record<StageKey, string> = {
  contacts: 'Поиск контактов',
  communication: 'Коммуникация с вузом',
  meeting: 'Организация встречи',
  documents_exchange: 'Обмен документами',
  documents_correction: 'Корректировка документов',
  documents_signing: 'Подписание документов',
  materials_transfer: 'Передача материалов',
  product_implementation: 'Внедрение продукта',
  teachers_training: 'Обучение преподавателей',
  program_update: 'Актуализация программы',
  classes: 'Ведение занятий',
  docs_actualization: 'Актуализация документации',
  teachers_upskilling: 'Повышение квалификации',
  control: 'Контроль исполнения',
}

export const STAGE_ORDER: StageKey[] = [
  'contacts',
  'communication',
  'meeting',
  'documents_exchange',
  'documents_correction',
  'documents_signing',
  'materials_transfer',
  'product_implementation',
  'teachers_training',
  'program_update',
  'classes',
  'docs_actualization',
  'teachers_upskilling',
  'control',
]

// Статус по этапу: не начат / в работе / завершён / просрочен
export type StageStatus = 'not_started' | 'in_progress' | 'completed' | 'overdue'

// Расширенный Stage с ключом этапа
export interface StageExtended extends Stage {
  key: StageKey
  status: StageStatus
}

// Расширенный Workflow с массивом из 14 этапов
export interface WorkflowExtended extends Omit<Workflow, 'stages'> {
  universityName: string
  directionName: string
  productName: string
  managerName: string
  stages: StageExtended[]
}
