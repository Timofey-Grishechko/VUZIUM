from __future__ import annotations

from internal.core.errors import ValidationError

# target_field -> человекочитаемая подпись поля из ТЗ
TARGET_FIELDS: dict[str, str] = {
    "university_name": "Название ВУЗа",
    "vendor": "Вендор",
    "product": "ПО",
    "contract_number": "Номер договора",
    "license_signed_at": "Подписание лицензии",
    "license_expires_year": "Срок действия лицензии (год)",
    "transfer_status": "Статус по передаче",
    "manager_fio": "ФИО менеджера",
    "responsible_persons": "Ответственные от ВУЗа",
    "comment": "Комментарий",
}

REQUIRED_FIELDS = {
    "university_name",
    "vendor",
    "product",
    "contract_number",
    "license_signed_at",
    "license_expires_year",
    "transfer_status",
}


def validate_mapping(mapping: dict[str, str]) -> None:
    """mapping: {target_field: имя_колонки_в_файле}."""
    unknown = set(mapping) - set(TARGET_FIELDS)
    if unknown:
        raise ValidationError(
            "Unknown target fields in mapping",
            details={"unknown": sorted(unknown), "allowed": sorted(TARGET_FIELDS)},
        )

    missing = REQUIRED_FIELDS - set(mapping)
    if missing:
        raise ValidationError(
            "Missing required field mapping",
            details={"missing": sorted(missing)},
        )
