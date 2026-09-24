import { Paper, Typography, Chip, Box } from '@mui/material'
import { useDraggable } from '@dnd-kit/core'
import { CSS } from '@dnd-kit/utilities'
import type { WorkflowExtended } from '../../../types/domain'

interface Props {
  workflow: WorkflowExtended
  onClick?: () => void
}

export default function WorkflowCard({ workflow, onClick }: Props) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: workflow.id,
    data: { workflow },
  })

  const style = {
    transform: CSS.Translate.toString(transform),
    opacity: isDragging ? 0.4 : 1,
    cursor: 'grab',
  }

  return (
    <Paper
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      onClick={onClick}
      sx={{
        p: 1.5,
        mb: 1,
        borderRadius: 2,
        border: '1px solid',
        borderColor: 'divider',
        '&:hover': { borderColor: 'primary.main', boxShadow: 2 },
      }}
    >
      <Typography
        variant="body2"
        sx={{ fontWeight: 600, mb: 0.5, fontSize: '0.85rem' }}
      >
        {workflow.universityName}
      </Typography>
      <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
        {workflow.productName}
      </Typography>
      <Box sx={{ mt: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Chip
          label={workflow.directionName}
          size="small"
          variant="outlined"
          color="primary"
          sx={{ fontSize: '0.7rem', height: 20 }}
        />
        <Typography variant="caption" color="text.secondary">
          {workflow.managerName.split(' ')[0]}
        </Typography>
      </Box>
    </Paper>
  )
}
