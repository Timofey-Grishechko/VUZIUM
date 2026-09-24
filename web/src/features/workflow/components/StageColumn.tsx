import { Paper, Typography, Box } from '@mui/material'
import { useDroppable } from '@dnd-kit/core'
import type { WorkflowExtended, StageKey } from '../../../types/domain'
import { STAGE_LABELS } from '../../../types/domain'
import WorkflowCard from './WorkflowCard'

interface Props {
  stageKey: StageKey
  workflows: WorkflowExtended[]
  onCardClick: (id: string) => void
}

export default function StageColumn({ stageKey, workflows, onCardClick }: Props) {
  const { setNodeRef, isOver } = useDroppable({ id: stageKey })

  return (
    <Box
      sx={{
        minWidth: { xs: 200, md: 240 },
        width: { xs: 200, md: 240 },
        flexShrink: 0,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Box
        sx={{
          px: 1.5,
          py: 1,
          mb: 1,
          borderRadius: 1,
          bgcolor: 'grey.100',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Typography variant="caption" sx={{ fontWeight: 600 }}>
          {STAGE_LABELS[stageKey]}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {workflows.length}
        </Typography>
      </Box>

      <Paper
        ref={setNodeRef}
        elevation={0}
        sx={{
          p: 1,
          flexGrow: 1,
          minHeight: 200,
          bgcolor: isOver ? 'primary.50' : 'grey.50',
          border: '1px dashed',
          borderColor: isOver ? 'primary.main' : 'transparent',
          borderRadius: 1,
          transition: 'all 0.15s',
        }}
      >
        {workflows.map((w) => (
          <WorkflowCard
            key={w.id}
            workflow={w}
            onClick={() => onCardClick(w.id)}
          />
        ))}
      </Paper>
    </Box>
  )
}
