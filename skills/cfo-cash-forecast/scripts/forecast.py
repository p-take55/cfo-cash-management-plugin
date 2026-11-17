#!/usr/bin/env python3
"""Calculate dated, single-currency cash movements; never accesses a service."""
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext


def amount(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError('amounts must be decimal strings or integers, not null/float/bool')
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError('invalid amount') from error
    if not result.is_finite():
        raise ValueError('amount must be finite')
    if len(result.as_tuple().digits) > 24 or not -8 <= result.as_tuple().exponent <= 16:
        raise ValueError('amount exceeds supported precision')
    return result


def forecast(data):
    with localcontext() as context:
        context.prec = 80
        return _forecast(data)


def _forecast(data):
    start, end = date.fromisoformat(data['start']), date.fromisoformat(data['end'])
    if start > end:
        raise ValueError('start must not follow end')
    currency = data['currency']
    if not isinstance(currency, str) or not currency.strip():
        raise ValueError('currency is required')
    balance = amount(data['opening'])
    floor = None if data.get('floor') is None else amount(data['floor'])
    if floor is not None and floor < 0:
        raise ValueError('floor must be nonnegative')
    minimum = balance
    minimum_date = start.isoformat()
    first_negative = start.isoformat() if balance < 0 else None
    first_below_floor = start.isoformat() if floor is not None and balance < floor else None
    days, seen, excluded = {}, set(), []
    events = data['events']
    if not isinstance(events, list):
        raise ValueError('events must be an explicit list')
    for event in events:
        event_id = event['id']
        if not isinstance(event_id, str) or not event_id.strip() or event_id in seen:
            raise ValueError('event IDs must be nonempty and unique')
        seen.add(event_id)
        if event['currency'] != currency:
            raise ValueError('mixed currencies are not supported')
        if event['kind'] not in ('in', 'out'):
            raise ValueError('kind must be in or out')
        if event['status'] not in ('actual', 'scheduled', 'assumed'):
            raise ValueError('status must be actual, scheduled or assumed')
        day = date.fromisoformat(event['date'])
        value = amount(event['amount'])
        if value < 0:
            raise ValueError('amount must be nonnegative; use kind to specify direction')
        if not isinstance(event['source'], str) or not event['source'].strip():
            raise ValueError('source reference is required')
        if not start <= day <= end:
            excluded.append(event_id)
            continue
        bucket = days.setdefault(day, {'in': Decimal(0), 'out': Decimal(0), 'events': []})
        bucket[event['kind']] += value
        bucket['events'].append(event)
    rows = []
    unknown_order = []
    for day, bucket in sorted(days.items()):
        opening = balance
        balance += bucket['in'] - bucket['out']
        day_text = day.isoformat()
        if balance < minimum:
            minimum, minimum_date = balance, day_text
        if first_negative is None and balance < 0:
            first_negative = day_text
        if floor is not None and first_below_floor is None and balance < floor:
            first_below_floor = day_text
        if bucket['in'] > 0 and bucket['out'] > 0:
            unknown_order.append(day_text)
        rows.append({'date': day_text, 'opening': str(opening),
                     'in': str(bucket['in']), 'out': str(bucket['out']),
                     'closing': str(balance), 'events': bucket['events']})
    return {'currency': currency, 'start': start.isoformat(), 'end': end.isoformat(),
            'opening': str(amount(data['opening'])), 'closing': str(balance),
            'minimum_balance': str(minimum), 'minimum_date': minimum_date,
            'first_negative_date': first_negative, 'floor': None if floor is None else str(floor),
            'first_below_floor_date': first_below_floor,
            'maximum_floor_gap': None if floor is None else str(max(Decimal(0), floor - minimum)),
            'daily': rows, 'excluded_event_ids': excluded,
            'assumed_event_ids': [e['id'] for e in events if e['status'] == 'assumed' and e['id'] not in excluded],
            'intraday_order_unknown_dates': unknown_order,
            'scope': 'Opening and end-of-day balances only; input completeness is not verified.'}


def main():
    if len(sys.argv) != 2:
        raise ValueError('usage: python3 forecast.py INPUT.json')
    with open(sys.argv[1], encoding='utf-8') as source:
        data = json.load(source)
    print(json.dumps(forecast(data), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
