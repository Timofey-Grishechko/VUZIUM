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
