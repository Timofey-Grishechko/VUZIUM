import * as XLSX from 'xlsx'

export interface ParsedFile {
  columns: string[]
  rows: Record<string, unknown>[]
  filename: string
}

export interface FieldMapping {
  targetField: string
  sourceColumn: string
}

export const TARGET_FIELDS: { key: string; label: string; required?: boolean }[] = [
  { key: 'universityName', label: 'Название ВУЗа', required: true },
  { key: 'vendor', label: 'Вендор' },
  { key: 'product', label: 'ПО' },
  { key: 'contractNumber', label: 'Номер договора' },
  { key: 'licenseSignedAt', label: 'Подписание лицензии' },
  { key: 'licenseExpiresAt', label: 'Срок действия лицензии (год)' },
  { key: 'transferStatus', label: 'Статус по передаче' },
  { key: 'managerFio', label: 'ФИО Менеджера' },
  { key: 'responsibleFromVuz', label: 'Ответственные от ВУЗа' },
  { key: 'comment', label: 'Комментарий' },
]

export interface ImportResult {
  total: number
  created: number
  updated: number
  errors: { row: number; message: string }[]
}

export const importsApi = {
  async parseFile(file: File): Promise<ParsedFile> {
    const buffer = await file.arrayBuffer()
    const workbook = XLSX.read(buffer, { type: 'array' })
    const sheetName = workbook.SheetNames[0]
    const sheet = workbook.Sheets[sheetName]
    const rows = XLSX.utils.sheet_to_json<Record<string, unknown>>(sheet, { defval: '' })
    const columns = rows.length > 0 ? Object.keys(rows[0]) : []
    return { columns, rows, filename: file.name }
  },

  async runImport(
    parsed: ParsedFile,
    mapping: FieldMapping[],
  ): Promise<ImportResult> {
    await new Promise((r) => setTimeout(r, 1500))
    console.log('[mock import]', { mapping })
    return {
      total: parsed.rows.length,
      created: parsed.rows.length - 1,
      updated: 1,
      errors: [
        { row: 2, message: 'Вуз с таким названием уже существует — запись обновлена' },
      ],
    }
  },
}
