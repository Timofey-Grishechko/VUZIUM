"""
Точка входа фичи workflow — центральной сущности CRM: реэкспорт router.
Workflow создаётся сразу с 14 этапами (DEFAULT_STAGES в service.py),
переход этапа пишет запись в StageTransition (история) и, отдельно,
запись в общий AuditLog (см. audit/). Список workflow фильтруется по
AccessScope пользователя (users/service.get_accessible_university_ids).
"""

from internal.feature.workflow.router import router

__all__ = ["router"]
