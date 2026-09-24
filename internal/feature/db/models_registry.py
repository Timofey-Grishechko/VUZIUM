"""
Импортирует все модели фич, чтобы Base.metadata знала обо всех
таблицах — нужно Alembic'у для autogenerate (сам факт импорта
регистрирует класс в реестре SQLAlchemy, side-effect обязателен).

В env.py Alembic'а достаточно сделать:

    from internal.feature.db.models_registry import Base
    target_metadata = Base.metadata
"""

from internal.feature.db.base import Base

from internal.feature.audit.models import AuditLog  # noqa: F401
from internal.feature.catalog.models import (  # noqa: F401
    ITDirection,
    ITProduct,
    License,
    Responsible,
    University,
    Vendor,
)
from internal.feature.files.models import Attachment  # noqa: F401
from internal.feature.imports.models import CatalogImport, ImportMapping  # noqa: F401
from internal.feature.integrations.models import IntegrationSource, SyncLog  # noqa: F401
from internal.feature.reports.models import Report  # noqa: F401
from internal.feature.users.models import AccessScope, User  # noqa: F401
from internal.feature.workflow.models import Stage, StageTransition, Workflow  # noqa: F401

__all__ = ["Base"]
