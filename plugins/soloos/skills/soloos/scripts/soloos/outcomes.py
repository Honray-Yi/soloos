"""Compare a logged decision against a named, independently supplied observation."""
from decimal import Decimal, InvalidOperation
from .data import fingerprint, trusted, validate
from .records import validate_record, record


def evaluate(decision, data, metric, start, end, target, direction='at_least'):
    validate_record(decision)
    validate(data)
    if decision['record_type'] != 'Decision' or decision['company_id'] != data['company']['id']:
        raise ValueError('Decision must belong to this company')
    if direction not in ('at_least', 'at_most'):
        raise ValueError('Direction must be at_least or at_most')
    try:
        goal = Decimal(target)
    except InvalidOperation as exc:
        raise ValueError('Target must be a finite decimal') from exc
    if not goal.is_finite(): raise ValueError('Target must be finite')
    observations = [r for r in data.get('measurements', []) if r['metric'] == metric and r['start'] == start and r['end'] == end]
    observation = observations[0] if observations else None
    result = {'decision_id': decision['id'], 'company_id': data['company']['id'], 'metric': metric,
              'start': start, 'end': end, 'target': str(goal), 'direction': direction, 'actual': None,
              'assessment': 'insufficient_evidence', 'provenance': ['decision:sha256:' + fingerprint(decision), 'dataset:sha256:' + fingerprint(data)],
              'caveat': 'The user-selected evaluation criterion is not proof of a precommitted target or causal impact.'}
    if observation and trusted(observation) and trusted(data['company']):
        actual = Decimal(observation['value'])
        passed = actual >= goal if direction == 'at_least' else actual <= goal
        result.update(actual=str(actual), unit=observation['unit'], assessment='met' if passed else 'not_met')
    result['id'] = 'outcome-' + fingerprint(result)
    return record('Outcome', data, result, 'confirmed' if result['actual'] is not None else 'estimate')
