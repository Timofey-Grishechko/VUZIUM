"""
Расписание периодических задач (Celery beat).

Имена тасков ("integrations.sync_lms" и т.д.) — контракт с Backend-3.
Пока сами таски не реализованы в integrations/ и reports/, beat будет
пытаться их запускать и падать с "task not registered" — это ожидаемо
на этом этапе и не ломает worker/beat как процессы.
"""

from celery.schedules import crontab

BEAT_SCHEDULE: dict[str, dict] = {
    "sync-lms-every-15-min": {
        "task": "integrations.sync_lms",
        "schedule": crontab(minute="*/15"),
    },
    "sync-website-every-15-min": {
        "task": "integrations.sync_website",
        "schedule": crontab(minute="*/15"),
    },
    "cleanup-expired-reports-daily": {
        "task": "reports.cleanup_expired",
        "schedule": crontab(hour=3, minute=0),
    },
}
