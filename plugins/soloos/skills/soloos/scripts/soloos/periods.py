"""Inclusive calendar reporting windows in company-local dates."""
import calendar
from datetime import date, timedelta
import re

CADENCES = ('daily', 'weekly', 'monthly', 'quarterly', 'annual')


def period(cadence, anchor):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', anchor):
        raise ValueError('Anchor must be YYYY-MM-DD')
    day = date.fromisoformat(anchor)
    if cadence == 'daily':
        first = last = day
    elif cadence == 'weekly':
        first = day - timedelta(days=day.weekday())
        last = first + timedelta(days=6)
    elif cadence == 'monthly':
        first = day.replace(day=1)
        last = day.replace(day=calendar.monthrange(day.year, day.month)[1])
    elif cadence == 'quarterly':
        month = ((day.month - 1) // 3) * 3 + 1
        first = date(day.year, month, 1)
        last = date(day.year, month + 2, calendar.monthrange(day.year, month + 2)[1])
    elif cadence == 'annual':
        first, last = date(day.year, 1, 1), date(day.year, 12, 31)
    else:
        raise ValueError('Unknown report cadence')
    return first.isoformat(), last.isoformat()
