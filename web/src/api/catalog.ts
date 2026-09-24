import type { PaginatedResponse, PaginationParams } from '../types/api'
import type {
  ITDirection,
  ITProduct,
  Responsible,
  University,
  Vendor,
} from '../types/domain'

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

const MOCK_DIRECTIONS: ITDirection[] = [
  { id: '1', name: 'DevOps' },
  { id: '2', name: 'QA' },
  { id: '3', name: 'Backend' },
  { id: '4', name: 'Frontend' },
  { id: '5', name: 'Data Science' },
  { id: '6', name: 'Mobile' },
  { id: '7', name: 'Information Security' },
]

const MOCK_VENDORS: Vendor[] = [
  { id: '1', name: 'Яндекс' },
  { id: '2', name: 'Сбер' },
  { id: '3', name: 'VK' },
  { id: '4', name: '1С' },
  { id: '5', name: 'Ростелеком' },
  { id: '6', name: 'Лаборатория Касперского' },
]

const MOCK_PRODUCTS: ITProduct[] = [
  { id: '1', vendorId: '1', directionId: '3', name: 'Яндекс Практикум Backend', description: 'Курс по backend-разработке' },
  { id: '2', vendorId: '1', directionId: '4', name: 'Яндекс Практикум Frontend' },
  { id: '3', vendorId: '2', directionId: '5', name: 'Сбер DS Academy' },
  { id: '4', vendorId: '3', directionId: '6', name: 'VK Mobile Bootcamp' },
  { id: '5', vendorId: '4', directionId: '3', name: '1С Разработчик' },
  { id: '6', vendorId: '5', directionId: '1', name: 'RTK DevOps Platform' },
  { id: '7', vendorId: '6', directionId: '7', name: 'Kaspersky Security' },
]

const MOCK_RESPONSIBLES: Responsible[] = [
  { id: '1', universityId: '1', fio: 'Иванов И.И.', email: 'ivanov@msu.ru', side: 'vuz' },
  { id: '2', universityId: '2', fio: 'Петров П.П.', email: 'petrov@spbu.ru', side: 'vuz' },
  { id: '3', universityId: '3', fio: 'Сидоров С.С.', email: 'sidorov@mipt.ru', side: 'vuz' },
  { id: '4', universityId: '1', fio: 'Коля Тестов', email: 'kolya@rtk.ru', side: 'school' },
  { id: '5', universityId: '2', fio: 'Мария РТК', email: 'maria@rtk.ru', side: 'school' },
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
  // === Directions ===
  async getDirections(): Promise<ITDirection[]> {
    await new Promise((r) => setTimeout(r, 200))
    return MOCK_DIRECTIONS
  },

  // === Vendors ===
  async getVendors(): Promise<Vendor[]> {
    await new Promise((r) => setTimeout(r, 200))
    return MOCK_VENDORS
  },

  // === Products ===
  async getProducts(): Promise<ITProduct[]> {
    await new Promise((r) => setTimeout(r, 200))
    return MOCK_PRODUCTS
  },

  // === Responsibles ===
  async getResponsibles(): Promise<Responsible[]> {
    await new Promise((r) => setTimeout(r, 200))
    return MOCK_RESPONSIBLES
  },  
}
