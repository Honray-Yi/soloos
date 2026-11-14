"""Evidence-aware department briefs and cross-department operational priorities."""
from datetime import date
from decimal import Decimal

from .catalog import DEPARTMENTS
from .data import trusted
from .kpis import business_kpis
from .finance import money


def department_review(data, start, end, department='all'):
    if department != 'all' and department not in DEPARTMENTS:
        raise ValueError('Unknown department')
    metrics = business_kpis(data, start, end)
    entities = data.get('entities', [])
    confirmed = [row for row in entities if trusted(row)]
    overdue = [r['id'] for r in confirmed if r['record_type'] == 'Task' and r['status'] != 'done' and r['due_date'] < end]
    blocked = [r['id'] for r in confirmed if r['record_type'] in ('Task', 'Project') and r['status'] == 'blocked']
    pipeline = [r['id'] for r in confirmed if r['record_type'] == 'Customer' and r['stage'] in ('lead', 'qualified')]
    roles = DEPARTMENTS if department == 'all' else {department: DEPARTMENTS[department]}
    by_type = {kind: [row for row in confirmed if row['record_type'] == kind] for kind in ('Goal','Project','Task','Customer','Product','Campaign')}
    goal_progress = []
    for goal in by_type['Goal']:
        actual = metrics['financials'].get(goal['metric']) if goal['metric'] in ('revenue','expenses','profit') else metrics['metrics'].get(goal['metric'],{}).get('value')
        met = None if actual is None else (Decimal(actual) >= Decimal(goal['target']) if goal['direction'] == 'at_least' else Decimal(actual) <= Decimal(goal['target']))
        goal_progress.append({'id':goal['id'],'metric':goal['metric'],'actual':actual,'target':goal['target'],
                              'at_target':met,'due_date':goal['due_date'],'deadline_reached':goal['due_date']<=end})
    minor = data['company']['minor_units']
    facts = {
        'CEO': {'goal_progress': goal_progress, 'active_projects': [r['id'] for r in by_type['Project'] if r['status']=='active']},
        'CFO': {'cash_basis_financials':metrics['financials']},
        'CMO': {'campaigns': [{'id':r['id'],'channel':r['channel'],'status':r['status'],'budget':r['budget']} for r in by_type['Campaign']],
                'observed_campaign_budget': money(sum((Decimal(r['budget']) for r in by_type['Campaign']),Decimal(0)),minor)},
        'Sales': {'observed_pipeline_value': money(sum((Decimal(r['value']) for r in by_type['Customer'] if r['id'] in pipeline),Decimal(0)),minor),
                  'qualified_customer_ids':[r['id'] for r in by_type['Customer'] if r['stage']=='qualified']},
        'COO': {'overdue_tasks':overdue,'blocked_work':blocked},
        'CTO/Product': {'products':[{'id':r['id'],'status':r['status'],'unit_contribution':money(Decimal(r['price'])-Decimal(r['unit_cost']),minor)} for r in by_type['Product']], 'blocked_projects':[r['id'] for r in by_type['Project'] if r['status']=='blocked']},
        'HR/Partnership': {'utilization':metrics['metrics'].get('utilization',{'value':None,'status':'not_measured'}),
                           'observed_task_owners':sorted({r['owner'] for r in by_type['Task']}),
                           'partner_options':['defer work','reduce scope','evaluate a separately approved partner engagement']},
        'BI': {'financial_coverage_complete':metrics['financials']['complete'],
               'unavailable_metrics':[key for key,item in metrics['metrics'].items() if item['value'] is None],
               'unverified_record_ids':[r['id'] for r in entities if not trusted(r)]},
    }
    briefs = {}
    for role, (mandate, partners, prompt) in roles.items():
        briefs[role] = {'mandate': mandate, 'coordinate_with': partners, 'decision_prompt': prompt,
                       'findings': facts[role],
                       'evidence_ids': [r['id'] for r in confirmed],
                       'limits': ['Entity lists are snapshots, not historical event counts.', 'No inferred HR identity, contract authority or customer consent.']}
    priorities = []
    if not metrics['financials']['complete']:
        priorities.append({'departments': ['BI', 'CFO', 'CEO'], 'reason': 'Financial evidence is incomplete', 'action': 'Reconcile period coverage before committing spend.'})
    if overdue or blocked:
        priorities.append({'departments': ['COO', 'CTO/Product', 'Sales'], 'reason': 'Blocked or overdue delivery work', 'action': 'Resolve delivery constraints before promising additional capacity.', 'record_ids': sorted(set(overdue + blocked))})
    if pipeline and (overdue or blocked):
        priorities.append({'departments': ['Sales', 'COO', 'HR/Partnership'], 'reason': 'Pipeline demand overlaps delivery constraints', 'action': 'Evaluate timing or a scoped partner engagement before closing new work.'})
    return {'as_of': end, 'departments': briefs, 'kpis': metrics, 'overdue_task_ids': overdue,
            'blocked_record_ids': blocked, 'pipeline_ids': pipeline, 'priorities': priorities,
            'unverified_entity_ids': [r['id'] for r in entities if not trusted(r)], 'execution': 'proposal_only'}
