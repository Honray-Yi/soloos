"""Extended command registration keeps the baseline CLI backward compatible."""
import json
from pathlib import Path

from .catalog import TEMPLATES, DEPARTMENTS
from .data import load, _unique_object
from .forecast import cash_forecast
from .kpis import business_kpis
from .management import department_review
from .outcomes import evaluate
from .periods import CADENCES
from .reporting import executive_report, markdown
from .storage import Store

COMMANDS = {'template','departments','business-kpis','review','report','forecast','store-put','store-get','history','outcome'}


def read_json(path):
    def invalid(value): raise ValueError('Non-finite JSON number: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=_unique_object, parse_constant=invalid)


def register(subs):
    template = subs.add_parser('template', help='Show required inputs and formulas for a business model')
    template.add_argument('business_type', choices=sorted(TEMPLATES))
    subs.add_parser('departments', help='Show the eight management departments')
    for name in ('business-kpis','review','forecast'):
        command = subs.add_parser(name)
        command.add_argument('data')
        command.add_argument('--start', required=True)
        command.add_argument('--end', required=True)
        command.add_argument('--out')
        if name == 'review': command.add_argument('--department', default='all', choices=['all', *DEPARTMENTS])
        if name == 'forecast':
            command.add_argument('--months', type=int, default=3)
            command.add_argument('--revenue-growth', default='0')
            command.add_argument('--expense-growth', default='0')
    report = subs.add_parser('report')
    report.add_argument('data')
    report.add_argument('--cadence', required=True, choices=CADENCES)
    report.add_argument('--anchor', required=True)
    report.add_argument('--format', choices=('json','markdown'), default='markdown')
    report.add_argument('--out')
    for name in ('store-put','store-get','history'):
        command = subs.add_parser(name)
        command.add_argument('--db', required=True)
        command.add_argument('--out')
        if name == 'store-put': command.add_argument('data')
        if name == 'store-get': command.add_argument('digest')
        if name == 'history': command.add_argument('--company-id')
    outcome = subs.add_parser('outcome')
    outcome.add_argument('decision')
    outcome.add_argument('data')
    for arg in ('metric','start','end','target'): outcome.add_argument('--' + arg, required=True)
    outcome.add_argument('--direction', choices=('at_least','at_most'), default='at_least')
    outcome.add_argument('--out')


def dispatch(args):
    cmd = args.command
    if cmd == 'template': return {'business_type': args.business_type, 'metrics': TEMPLATES[args.business_type]}
    if cmd == 'departments': return {key: {'mandate': value[0], 'coordinate_with': value[1], 'decision_prompt': value[2]} for key, value in DEPARTMENTS.items()}
    if cmd == 'store-put': return {'digest': Store(args.db).put(read_json(args.data)), 'storage': args.db}
    if cmd == 'store-get': return Store(args.db).get(args.digest)
    if cmd == 'history': return Store(args.db).history(args.company_id)
    data = load(args.data)
    if cmd == 'business-kpis': return business_kpis(data, args.start, args.end)
    if cmd == 'review': return department_review(data, args.start, args.end, args.department)
    if cmd == 'forecast': return cash_forecast(data, args.start, args.end, args.months, args.revenue_growth, args.expense_growth)
    if cmd == 'report':
        report = executive_report(data, args.cadence, args.anchor)
        return markdown(report) if args.format == 'markdown' else report
    if cmd == 'outcome': return evaluate(read_json(args.decision), data, args.metric, args.start, args.end, args.target, args.direction)
    raise ValueError('Unsupported command')
