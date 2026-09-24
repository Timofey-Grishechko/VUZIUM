import { useState } from 'react'
import { Box, Typography, Grid, Paper, Chip, Stack, Button, CircularProgress } from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { useNavigate, useParams } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'

import StageStepper from '../features/workflow/components/StageStepper'
import StageDetailPanel from '../features/workflow/components/StageDetailPanel'
import { useWorkflow } from '../features/workflow/hooks/useWorkflow'
import { workflowApi } from '../api/workflow'
import type { StageStatus } from '../types/domain'

export default function WorkflowDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { data: workflow, isLoading } = useWorkflow(id)

  const [selectedStageId, setSelectedStageId] = useState<string | null>(null)

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (!workflow) {
    return (
      <Box>
        <Typography variant="h5">Workflow не найден</Typography>
        <Button sx={{ mt: 2 }} onClick={() => navigate('/workflows')}>
          Вернуться к списку
        </Button>
      </Box>
    )
  }

  const currentStage =
    workflow.stages.find((s) => s.id === selectedStageId) ??
    workflow.stages.find((s) => s.status === 'in_progress') ??
    workflow.stages[0]

  const handleTransition = async (stageId: string, newStatus: StageStatus) => {
    await workflowApi.transitionStage(workflow.id, stageId, newStatus, 'Переход из детальной')
    queryClient.invalidateQueries({ queryKey: ['workflow', workflow.id] })
  }

  return (
    <Box>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/workflows')} sx={{ mb: 2 }}>
        К канбану
      </Button>

      <Typography variant="h4" gutterBottom>
        {workflow.universityName}
      </Typography>
      <Stack direction="row" spacing={1} sx={{ mb: 3 }}>
        <Chip label={workflow.productName} color="primary" variant="outlined" />
        <Chip label={workflow.directionName} />
        <Chip label={`Менеджер: ${workflow.managerName}`} variant="outlined" />
      </Stack>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 5 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              14 этапов
            </Typography>
            <StageStepper
              stages={workflow.stages}
              selectedStageId={currentStage.id}
              onSelect={setSelectedStageId}
            />
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 7 }}>
          <StageDetailPanel
            workflowId={workflow.id}
            stage={currentStage}
            onTransition={handleTransition}
          />
        </Grid>
      </Grid>
    </Box>
  )
}
