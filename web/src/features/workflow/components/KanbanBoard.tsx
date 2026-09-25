import { DndContext, PointerSensor, useSensor, useSensors } from '@dnd-kit/core'
import type { DragEndEvent } from '@dnd-kit/core'
import { Box } from '@mui/material'
import type { StageKey, WorkflowExtended, StageStatus } from '../../../types/domain'
import { STAGE_ORDER } from '../../../types/domain'
import StageColumn from './StageColumn'

interface Props {
  workflows: WorkflowExtended[]
  onCardClick: (id: string) => void
  onStageChange: (
    workflowId: string,
    stageKey: StageKey,
    newStatus: StageStatus,
  ) => void
}

export default function KanbanBoard({ workflows, onCardClick, onStageChange }: Props) {
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
  )

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event
    if (!over) return

    const workflowId = String(active.id)
    const targetStageKey = over.id as StageKey
    if (!STAGE_ORDER.includes(targetStageKey)) return

    // Находим workflow и его текущий этап
    const workflow = workflows.find((w) => w.id === workflowId)
    if (!workflow) return

    const currentStageKey = workflow.stages.find((s) => s.status === 'in_progress')?.key
    if (currentStageKey === targetStageKey) return

    console.log('[kanban] moving', workflowId, 'from', currentStageKey, 'to', targetStageKey)
    onStageChange(workflowId, targetStageKey, 'in_progress')
  }

  return (
    <DndContext sensors={sensors} onDragEnd={handleDragEnd}>
      <Box
        sx={{
          display: 'flex',
          gap: 2,
          overflowX: 'auto',
          pb: 2,
          minHeight: 400,
        }}
      >
        {STAGE_ORDER.map((stageKey) => {
          const stageWorkflows = workflows.filter((w) => {
            // workflow "находится" в колонке, если его текущий этап == stageKey
            const current = w.stages.find((s) => s.status === 'in_progress')
            return current?.key === stageKey
          })

          return (
            <StageColumn
              key={stageKey}
              stageKey={stageKey}
              workflows={stageWorkflows}
              onCardClick={onCardClick}
            />
          )
        })}
      </Box>
    </DndContext>
  )
}
