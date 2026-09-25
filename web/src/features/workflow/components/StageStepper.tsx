import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Typography,
  Chip,
} from '@mui/material'
import type { StageExtended } from '../../../types/domain'

interface Props {
  stages: StageExtended[]
  selectedStageId: string | null
  onSelect: (stageId: string) => void
}

const statusColor: Record<StageExtended['status'], 'default' | 'primary' | 'success' | 'error'> = {
  not_started: 'default',
  in_progress: 'primary',
  completed: 'success',
  overdue: 'error',
}

const statusLabel: Record<StageExtended['status'], string> = {
  not_started: 'Не начат',
  in_progress: 'В работе',
  completed: 'Завершён',
  overdue: 'Просрочен',
}

export default function StageStepper({ stages, selectedStageId, onSelect }: Props) {
  const activeStep = stages.findIndex((s) => s.id === selectedStageId)

  return (
    <Box sx={{ maxWidth: 400 }}>
      <Stepper activeStep={activeStep} orientation="vertical" nonLinear>
        {stages.map((stage) => (
          <Step key={stage.id} completed={stage.status === 'completed'}>
            <StepLabel
              onClick={() => onSelect(stage.id)}
              sx={{ cursor: 'pointer' }}
              optional={
                <Chip
                  label={statusLabel[stage.status]}
                  color={statusColor[stage.status]}
                  size="small"
                  variant="outlined"
                  sx={{ mt: 0.5 }}
                />
              }
            >
              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                {stage.name}
              </Typography>
            </StepLabel>
            <StepContent>
              <Typography variant="caption" color="text.secondary">
                {stage.comment ?? 'Нет комментария'}
              </Typography>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  )
}
