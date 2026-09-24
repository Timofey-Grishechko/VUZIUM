import { catalogApi } from './catalog'
import { workflowApi } from './workflow'

export type ReportFormat = 'xlsx' | 'xls' | 'pdf'

export interface ReportFilters {
  dateFrom?: string
  dateTo?: string
  universityId?: string
  directionId?: string
  productId?: string
  managerId?: string
}

export interface ReportColumn {
  key: string
  label: string
  selected: boolean
}

export const DEFAULT_COLUMNS: ReportColumn[] = [
  { key: 'university', label: 'Вуз', selected: true },
  { key: 'direction', label: 'ИТ-направление', selected: true },
  { key: 'product', label: 'ИТ-продукт', selected: true },
  { key: 'status', label: 'Статус', selected: true },
  { key: 'manager', label: 'Ответственный', selected: true },
  { key: 'createdAt', label: 'Дата создания', selected: false },
  { key: 'updatedAt', label: 'Дата обновления', selected: false },
]

export interface GeneratedReport {
  id: string
  createdAt: string
  format: ReportFormat
  filename: string
  size: number
  status: 'ready' | 'processing' | 'error'
}

// Мок-хранилище отчётов
const MOCK_REPORTS: GeneratedReport[] = [
  {
    id: '1',
    createdAt: '2026-09-20 14:30',
    format: 'xlsx',
    filename: 'report_2026-09-20.xlsx',
    size: 24800,
    status: 'ready',
  },
  {
    id: '2',
    createdAt: '2026-09-22 09:15',
    format: 'pdf',
    filename: 'report_2026-09-22.pdf',
    size: 51200,
    status: 'ready',
  },
]

export const reportsApi = {
  async generateReport(
    filters: ReportFilters,
    columns: ReportColumn[],
    format: ReportFormat,
  ): Promise<GeneratedReport> {
    // Имитация запроса на бэк и работы Celery
    await new Promise((r) => setTimeout(r, 1500))

    // Собираем данные для отчёта (моки — просто логируем)
    const [workflows] = await Promise.all([workflowApi.getWorkflows()])
    console.log('[mock report]', { filters, columns, format, workflows })

    const newReport: GeneratedReport = {
      id: String(Date.now()),
      createdAt: new Date().toLocaleString('ru-RU'),
      format,
      filename: `report_${Date.now()}.${format}`,
      size: 30000 + Math.random() * 50000,
      status: 'ready',
    }
    MOCK_REPORTS.unshift(newReport)
    return newReport
  },

  async getReportHistory(): Promise<GeneratedReport[]> {
    await new Promise((r) => setTimeout(r, 200))
    return [...MOCK_REPORTS]
  },

  // Универсальный метод получения справочников для фильтров
  async getFilterOptions() {
    const [universities, directions, products] = await Promise.all([
      catalogApi.getUniversities({ pageSize: 100 }),
      catalogApi.getDirections(),
      catalogApi.getProducts(),
    ])
    return {
      universities: universities.items,
      directions,
      products,
    }
  },
}
