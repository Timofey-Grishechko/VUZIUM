import { useState } from 'react'
import { Box, Typography, TextField, Stack, InputAdornment, CircularProgress } from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'
import { useNavigate } from 'react-router-dom'

import KanbanBoard from '../features/workflow/components/KanbanBoard'
import { useWorkflows } from '../features/workflow/hooks/useWorkflows'
import { useDebounce } from '../hooks/useDebounce'
import { workflowApi } from '../api/workflow'

export default function WorkflowsPage() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 300)

  const { data: workflows = [], isLoading } = useWorkflows({
    search: debouncedSearch || undefined,
  })

  const handleStageChange = async (
    workflowId: string,
    stageKey: string,
    newStatus: 'not_started' | 'in_progress' | 'completed' | 'overdue',
  ) => {
    const workflow = workflows.find((w) => w.id === workflowId)
    const stage = workflow?.stages.find((s) => s.key === stageKey)
    if (!stage) return
    await workflowApi.transitionStage(workflowId, stage.id, newStatus, 'Перетаскивание в канбане')
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Workflow
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Цикл взаимодействия с вузом по 14 этапам. Перетаскивайте карточки между колонками.
      </Typography>

      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <TextField
          placeholder="Поиск по вузу или продукту"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          size="small"
          sx={{ minWidth: 320 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon fontSize="small" />
                </InputAdornment>
              ),
            },
          }}
        />
      </Stack>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
          <CircularProgress />
        </Box>
      ) : (
        <KanbanBoard
          workflows={workflows}
          onCardClick={(id) => navigate(`/workflows/${id}`)}
          onStageChange={handleStageChange}
        />
      )}
    </Box>
  )
}
