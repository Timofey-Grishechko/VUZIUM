import { useState } from 'react'
import {
  Box,
  Typography,
  Button,
  Stack,
  Divider,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Chip,
} from '@mui/material'
import AttachFileIcon from '@mui/icons-material/AttachFile'
import DeleteIcon from '@mui/icons-material/Delete'
import ArrowForwardIcon from '@mui/icons-material/ArrowForward'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import DownloadIcon from '@mui/icons-material/Download'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

import { workflowApi } from '../../../api/workflow'
import type { Attachment } from '../../../api/workflow'
import type { StageExtended, StageStatus } from '../../../types/domain'

interface Props {
  workflowId: string
  stage: StageExtended
  onTransition: (stageId: string, newStatus: StageStatus) => void
}

export default function StageDetailPanel({ workflowId, stage, onTransition }: Props) {
  const queryClient = useQueryClient()
  const [comment, setComment] = useState('')
  const [file, setFile] = useState<File | null>(null)

  const { data: attachments = [] } = useQuery({
    queryKey: ['attachments', stage.id],
    queryFn: () => workflowApi.getAttachments(stage.id),
  })

  const uploadMutation = useMutation({
    mutationFn: (f: File) => workflowApi.uploadAttachment(stage.id, f),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attachments', stage.id] })
      setFile(null)
    },
  })

  const handleUpload = () => {
    if (file) uploadMutation.mutate(file)
  }

  const canMoveForward = stage.status !== 'completed'
  const canMoveBack = stage.status === 'completed' || stage.status === 'in_progress'

  return (
    <Box sx={{ p: 3, bgcolor: 'background.paper', borderRadius: 2, border: '1px solid', borderColor: 'divider' }}>
      <Typography variant="h6" gutterBottom>
        {stage.name}
      </Typography>

      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip label={stage.status === 'completed' ? 'Завершён' : stage.status === 'in_progress' ? 'В работе' : 'Не начат'} size="small" color={stage.status === 'completed' ? 'success' : stage.status === 'in_progress' ? 'primary' : 'default'} />
      </Stack>

      <Divider sx={{ my: 2 }} />

      <Typography variant="subtitle2" gutterBottom>
        Комментарий
      </Typography>
      <TextField
        multiline
        rows={2}
        fullWidth
        size="small"
        placeholder="Добавить комментарий к этапу…"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        sx={{ mb: 2 }}
      />

      <Divider sx={{ my: 2 }} />

      <Typography variant="subtitle2" gutterBottom>
        Вложения ({attachments.length})
      </Typography>

      <List dense>
        {attachments.map((a: Attachment) => (
          <ListItem
            key={a.id}
            secondaryAction={
              <IconButton edge="end" size="small">
                <DownloadIcon fontSize="small" />
              </IconButton>
            }
          >
            <ListItemIcon sx={{ minWidth: 32 }}>
              <AttachFileIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText
              primary={a.filename}
              secondary={`${(a.size / 1024).toFixed(0)} КБ · ${a.uploadedAt}`}
            />
          </ListItem>
        ))}
        {attachments.length === 0 && (
          <Typography variant="caption" color="text.secondary">
            Файлов пока нет
          </Typography>
        )}
      </List>

      <Box sx={{ mt: 2 }}>
        <input
          type="file"
          id={`file-${stage.id}`}
          style={{ display: 'none' }}
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <label htmlFor={`file-${stage.id}`}>
          <Button component="span" size="small" startIcon={<AttachFileIcon />}>
            Прикрепить файл
          </Button>
        </label>
        {file && (
          <Stack direction="row" spacing={1} sx={{ mt: 1, alignItems: 'center' }}>
            <Typography variant="caption">{file.name}</Typography>
            <Button size="small" onClick={handleUpload} disabled={uploadMutation.isPending}>
              Загрузить
            </Button>
            <IconButton size="small" onClick={() => setFile(null)}>
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Stack>
        )}
      </Box>

      <Divider sx={{ my: 2 }} />

      <Stack direction="row" spacing={1}>
        {canMoveBack && (
          <Button
            variant="outlined"
            size="small"
            startIcon={<ArrowBackIcon />}
            onClick={() => onTransition(stage.id, 'in_progress')}
          >
            Назад
          </Button>
        )}
        {canMoveForward && (
          <Button
            variant="contained"
            size="small"
            endIcon={<ArrowForwardIcon />}
            onClick={() => onTransition(stage.id, 'completed')}
          >
            Завершить этап
          </Button>
        )}
      </Stack>
    </Box>
  )
}
