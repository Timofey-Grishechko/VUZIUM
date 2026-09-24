import type { PaginatedResponse, PaginationParams } from '../types/api'
import type { University } from '../types/domain'

// === Мок-данные (потом заменим на apiClient.get('/universities')) ===
const MOCK_UNIVERSITIES: University[] = [
  { id: '1', name: 'МГУ им. М.В. Ломоносова', region: 'Москва', status: 'active', managerId: '2', responsibleFromVuz: 'Иванов И.И.' },
  { id: '2', name: 'СПбГУ', region: 'Санкт-Петербург', status: 'active', managerId: '2', responsibleFromVuz: 'Петров П.П.' },
  { id: '3', name: 'МФТИ', region: 'Московская область', status: 'active', managerId: '3', responsibleFromVuz: 'Сидоров С.С.' },
  { id: '4', name: 'НИУ ВШЭ', region: 'Москва', status: 'active', managerId: '2', responsibleFromVuz: 'Кузнецов К.К.' },
  { id: '5', name: 'ИТМО', region: 'Санкт-Петербург', status: 'active', managerId: '3', responsibleFromVuz: 'Смирнов А.А.' },
  { id: '6', name: 'НГУ', region: 'Новосибирск', status: 'inactive', managerId: '2', responsibleFromVuz: 'Волков В.В.' },
  { id: '7', name: 'ТГУ', region: 'Томск', status: 'active', managerId: '3', responsibleFromVuz: 'Морозов М.М.' },
  { id: '8', name: 'КФУ', region: 'Казань', status: 'active', managerId: '2', responsibleFromVuz: 'Новиков Н.Н.' },
  { id: '9', name: 'УрФУ', region: 'Екатеринбург', status: 'active', managerId: '3', responsibleFromVuz: 'Фёдоров Ф.Ф.' },
  { id: '10', name: 'ДВФУ', region: 'Владивосток', status: 'inactive', managerId: '2', responsibleFromVuz: 'Егоров Е.Е.' },
  { id: '11', name: 'СФУ', region: 'Красноярск', status: 'active', managerId: '3', responsibleFromVuz: 'Павлов П.П.' },
  { id: '12', name: 'ЮФУ', region: 'Ростов-на-Дону', status: 'active', managerId: '2', responsibleFromVuz: 'Соколов С.С.' },
]

export interface UniversityFilters extends PaginationParams {
  status?: 'active' | 'inactive'
  region?: string
}

export const catalogApi = {
  async getUniversities(
    filters: UniversityFilters = {},
  ): Promise<PaginatedResponse<University>> {
    // имитация запроса к серверу
    await new Promise((r) => setTimeout(r, 300))

    let items = [...MOCK_UNIVERSITIES]

    // поиск по названию
    if (filters.search) {
      const q = filters.search.toLowerCase()
      items = items.filter((u) => u.name.toLowerCase().includes(q))
    }

    // фильтр по статусу
    if (filters.status) {
      items = items.filter((u) => u.status === filters.status)
    }

    // фильтр по региону
    if (filters.region) {
      items = items.filter((u) => u.region === filters.region)
    }

    // пагинация
    const page = filters.page ?? 1
    const pageSize = filters.pageSize ?? 10
    const total = items.length
    const start = (page - 1) * pageSize
    const paged = items.slice(start, start + pageSize)

    return { items: paged, total, page, pageSize }
  },
}
