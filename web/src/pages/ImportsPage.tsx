import { useState } from 'react'
import {
  Box,
  Typography,
  Paper,
  Button,
  Stack,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  MenuItem,
  CircularProgress,
  Chip,
} from '@mui/material'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import { useNavigate } from 'react-router-dom'

import { importsApi, TARGET_FIELDS } from '../api/imports'
import type { ParsedFile, FieldMapping, ImportResult } from '../api/imports'

export default function ImportsPage() {
  const navigate = useNavigate()
  const [parsed, setParsed] = useState<ParsedFile | null>(null)
  const [mapping, setMapping] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [importing, setImporting] = useState(false)
  const [result, setResult] = useState<ImportResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setError(null)
    setResult(null)
    setLoading(true)
    try {
      const data = await importsApi.parseFile(file)
      if (data.columns.length === 0) {
        setError('В файле не найдено колонок или данных')
        return
      }
      setParsed(data)
      const autoMap: Record<string, string> = {}
      TARGET_FIELDS.forEach((f) => {
        const match = data.columns.find((c) =>
          c.toLowerCase().includes(f.label.toLowerCase().slice(0, 6)),
        )
        if (match) autoMap[f.key] = match
      })
      setMapping(autoMap)
    } catch (err) {
      setError('Не удалось прочитать файл. Проверьте формат xlsx или xls.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleImport = async () => {
    if (!parsed) return
    const mappingArr: FieldMapping[] = Object.entries(mapping)
      .filter(([, v]) => v)
      .map(([targetField, sourceColumn]) => ({ targetField, sourceColumn }))
    setImporting(true)
    try {
      const res = await importsApi.runImport(parsed, mappingArr)
      setResult(res)
    } finally {
      setImporting(false)
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Импорт данных
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Загрузка каталогов из файлов xls, xlsx с маппингом полей
      </Typography>

      {!parsed && (
        <Paper
          elevation={0}
          sx={{
            p: { xs: 3, md: 6 },
            border: '2px dashed',
            borderColor: 'divider',
            textAlign: 'center',
            borderRadius: 2,
          }}
        >
          <UploadFileIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            Загрузите файл xls или xlsx
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Перетащите файл или выберите вручную
          </Typography>
          <input
            type="file"
            accept=".xls,.xlsx"
            id="xlsx-input"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
          <label htmlFor="xlsx-input">
            <Button
              variant="contained"
              component="span"
              startIcon={<UploadFileIcon />}
              disabled={loading}
            >
              {loading ? 'Загрузка…' : 'Выбрать файл'}
            </Button>
          </label>
          {error && (
            <Alert severity="error" sx={{ mt: 3, textAlign: 'left' }}>
              {error}
            </Alert>
          )}
        </Paper>
      )}

      {parsed && !result && (
        <>
          <Paper
            elevation={0}
            sx={{ p: 2, mb: 3, border: '1px solid', borderColor: 'divider' }}
          >
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={2}
              sx={{ alignItems: { xs: 'flex-start', sm: 'center' }, justifyContent: 'space-between' }}
            >
              <Box>
                <Typography variant="subtitle1">{parsed.filename}</Typography>
                <Typography variant="caption" color="text.secondary">
                  Найдено колонок: {parsed.columns.length}, строк: {parsed.rows.length}
                </Typography>
              </Box>
              <Button
                size="small"
                onClick={() => {
                  setParsed(null)
                  setMapping({})
                }}
              >
                Другой файл
              </Button>
            </Stack>
          </Paper>

          <Typography variant="h6" gutterBottom>
            Маппинг полей
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Сопоставьте колонки из файла с полями системы. Обязательные поля помечены *
          </Typography>

          <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider' }}>
            <TableContainer>
              <Table sx={{ minWidth: 500 }}>
                <TableHead>
                  <TableRow>
                    <TableCell>Поле системы</TableCell>
                    <TableCell>Колонка в файле</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {TARGET_FIELDS.map((f) => (
                    <TableRow key={f.key}>
                      <TableCell>
                        {f.label}
                        {f.required && (
                          <Chip label="*" size="small" color="error" sx={{ ml: 1 }} />
                        )}
                      </TableCell>
                      <TableCell>
                        <TextField
                          select
                          size="small"
                          fullWidth
                          value={mapping[f.key] ?? ''}
                          onChange={(e) =>
                            setMapping({ ...mapping, [f.key]: e.target.value })
                          }
                        >
                          <MenuItem value="">— не использовать —</MenuItem>
                          {parsed.columns.map((c) => (
                            <MenuItem key={c} value={c}>
                              {c}
                            </MenuItem>
                          ))}
                        </TextField>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
            Предпросмотр ({Math.min(5, parsed.rows.length)} из {parsed.rows.length})
          </Typography>
          <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider' }}>
            <TableContainer>
              <Table size="small" sx={{ minWidth: 600 }}>
                <TableHead>
                  <TableRow>
                    {parsed.columns.map((c) => (
                      <TableCell key={c}>{c}</TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {parsed.rows.slice(0, 5).map((row, i) => (
                    <TableRow key={i}>
                      {parsed.columns.map((c) => (
                        <TableCell key={c}>{String(row[c] ?? '')}</TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            sx={{ mt: 3 }}
          >
            <Button
              variant="contained"
              onClick={handleImport}
              disabled={importing}
              startIcon={
                importing ? <CircularProgress size={18} color="inherit" /> : undefined
              }
            >
              {importing ? 'Импортируем…' : 'Запустить импорт'}
            </Button>
            <Button variant="outlined" onClick={() => setParsed(null)}>
              Отмена
            </Button>
          </Stack>
        </>
      )}

      {result && (
        <Paper
          elevation={0}
          sx={{ p: { xs: 2, md: 3 }, border: '1px solid', borderColor: 'divider' }}
        >
          <Stack direction="row" spacing={2} sx={{ alignItems: 'center', mb: 2 }}>
            <CheckCircleIcon color="success" fontSize="large" />
            <Typography variant="h6">Импорт завершён</Typography>
          </Stack>

          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={{ xs: 1, sm: 3 }}
            sx={{ mb: 3 }}
          >
            <Box>
              <Typography variant="caption" color="text.secondary">
                Всего строк
              </Typography>
              <Typography variant="h5">{result.total}</Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Создано
              </Typography>
              <Typography variant="h5" color="success.main">
                {result.created}
              </Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Обновлено
              </Typography>
              <Typography variant="h5" color="primary.main">
                {result.updated}
              </Typography>
            </Box>
            <Box>
              <Typography variant="caption" color="text.secondary">
                С предупреждениями
              </Typography>
              <Typography variant="h5" color="warning.main">
                {result.errors.length}
              </Typography>
            </Box>
          </Stack>

          {result.errors.length > 0 && (
            <>
              <Typography variant="subtitle2" gutterBottom>
                Предупреждения
              </Typography>
              {result.errors.map((e, i) => (
                <Alert severity="warning" key={i} sx={{ mb: 1 }}>
                  Строка {e.row}: {e.message}
                </Alert>
              ))}
            </>
          )}

          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            sx={{ mt: 3 }}
          >
            <Button variant="contained" onClick={() => navigate('/universities')}>
              К каталогу вузов
            </Button>
            <Button
              variant="outlined"
              onClick={() => {
                setParsed(null)
                setResult(null)
                setMapping({})
              }}
            >
              Импортировать ещё
            </Button>
          </Stack>
        </Paper>
      )}
    </Box>
  )
}
