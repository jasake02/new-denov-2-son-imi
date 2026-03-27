from __future__ import annotations

from typing import Iterable


def normalize_order_value(value) -> int | None:
    if value in (None, "", 0, "0"):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _name_key(teacher) -> tuple[str, str, int]:
    last_name = (getattr(teacher, "last_name", "") or "").strip().lower()
    first_name = (getattr(teacher, "first_name", "") or "").strip().lower()
    teacher_id = getattr(teacher, "id", 0) or 0
    return (last_name, first_name, teacher_id)


def sort_teachers_for_display(teachers: Iterable, mode: str = "all") -> list:
    teachers = list(teachers)

    def sort_key(teacher):
        all_order = normalize_order_value(getattr(teacher, "display_order", None))
        category_order = normalize_order_value(getattr(teacher, "category_display_order", None))

        if mode == "category":
            primary = category_order if category_order is not None else all_order
            secondary = all_order
        else:
            primary = all_order
            secondary = category_order

        return (
            primary is None,
            primary if primary is not None else 10**9,
            secondary is None,
            secondary if secondary is not None else 10**9,
            *_name_key(teacher),
        )

    return sorted(teachers, key=sort_key)


def build_effective_order_map(teachers: Iterable, mode: str = "all") -> dict[int, int]:
    ordered_teachers = sort_teachers_for_display(teachers, mode=mode)
    effective_orders: dict[int, int] = {}
    last_order = 0

    for teacher in ordered_teachers:
        all_order = normalize_order_value(getattr(teacher, "display_order", None))
        category_order = normalize_order_value(getattr(teacher, "category_display_order", None))

        if mode == "category":
            requested = category_order if category_order is not None else all_order
        else:
            requested = all_order

        if requested is not None and requested > last_order:
            effective = requested
        else:
            effective = last_order + 1

        teacher_id = getattr(teacher, "id", None)
        if teacher_id is not None:
            effective_orders[teacher_id] = effective
        last_order = effective

    return effective_orders
