"""Interactive approval commands are separate from proposal and execution."""
import json
import sys

from .actions import Journal, execute_action, propose
from .commands import read_json
from .connectors import GitHubIssues
from .data import fingerprint

COMMANDS = {'action-propose','action-approve','action-execute','audit'}


def register(subs):
    proposal = subs.add_parser('action-propose', help='Prepare a proposal without contacting GitHub')
    for flag in ('company-id','target','title','body-file'): proposal.add_argument('--'+flag,required=True)
    proposal.add_argument('--out')
    for name in ('action-approve','action-execute'):
        command = subs.add_parser(name)
        command.add_argument('action')
        command.add_argument('--journal',required=True)
        if name == 'action-approve':
            command.add_argument('--actor',required=True)
            command.add_argument('--scope',choices=('external_write','high_risk'),required=True)
            command.add_argument('--minutes',type=int,default=15)
        else:
            command.add_argument('--approval-id')
            command.add_argument('--high-risk-approval-id')
            command.add_argument('--execute',action='store_true',help='Opt into the reviewed external write; default is dry-run')
        command.add_argument('--out')
    audit = subs.add_parser('audit')
    audit.add_argument('--journal',required=True)
    audit.add_argument('--out')


def dispatch(args):
    from pathlib import Path
    if args.command == 'action-propose':
        return propose(args.company_id,args.target,args.title,Path(args.body_file).read_text(encoding='utf-8'))
    if args.command == 'audit': return Journal(args.journal).events()
    action = read_json(args.action)
    journal = Journal(args.journal)
    if args.command == 'action-approve':
        if not sys.stdin.isatty(): raise PermissionError('Approval requires an interactive human terminal; produce a proposal in this host instead')
        print(json.dumps(action,indent=2),file=sys.stderr)
        expected = 'APPROVE '+args.scope+' '+fingerprint(action)
        print('Review the exact target and full content. Type '+expected+' to approve:',file=sys.stderr)
        token = journal.approve(action,args.actor,args.scope,input(),args.minutes)
        return {'approval_id':token,'scope':args.scope,'expires_in_minutes':args.minutes}
    return execute_action(action,journal,GitHubIssues(),args.approval_id,args.high_risk_approval_id,args.execute)
