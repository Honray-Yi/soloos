"""SoloOS CLI: local by default, external writes behind scoped explicit opt-in."""

import argparse
import json
import sys
import sqlite3
from jsonschema.exceptions import ValidationError
from . import commands
from . import action_commands

from .data import load, save_new
from .decisions import marketing_budget
from .finance import calculate
from .onboarding import demo, initialize
from .reporting import markdown, weekly_report
from .routing import route


def parser():
    root = argparse.ArgumentParser(description="SoloOS — local business intelligence and authorized operations")
    subs = root.add_subparsers(dest="command", required=True)
    commands.register(subs)
    action_commands.register(subs)
    subs.add_parser("capabilities", help="Describe CLI capabilities, not host or connector permissions")
    routing = subs.add_parser("route", help="Route an explicit intent label")
    routing.add_argument("intent")
    init = subs.add_parser("init", help="Create a profile with unknown financials, or a fictional demo")
    init.add_argument("--demo", action="store_true")
    init.add_argument("--name")
    init.add_argument("--business-type", default="custom")
    init.add_argument("--currency")
    init.add_argument("--timezone")
    init.add_argument("--minor-units", type=int, default=2)
    init.add_argument("--start")
    init.add_argument("--end")
    init.add_argument("--out", required=True)
    check = subs.add_parser("validate")
    check.add_argument("data")
    for name in ("kpis", "weekly-report", "marketing-budget"):
        command = subs.add_parser(name)
        command.add_argument("data")
        command.add_argument("--start", required=True)
        command.add_argument("--end", required=True)
        command.add_argument("--out")
        if name == "weekly-report":
            command.add_argument("--format", choices=("json", "markdown"), default="markdown")
        if name == "marketing-budget":
            command.add_argument("--monthly-increase", required=True)
            command.add_argument("--contribution-margin")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command in action_commands.COMMANDS:
            result = action_commands.dispatch(args)
        elif args.command in commands.COMMANDS:
            result = commands.dispatch(args)
        elif args.command == "capabilities":
            result = {"python": sys.version.split()[0], "local_json": True,
                      "weekly_reporting": True, "external_execution": False,
                      "connectors": ["github.create_issue (optional; scoped approvals and credentials required)"], "scheduler": False, "sqlite_adapter": True,
                      "report_cadences": list(commands.CADENCES), "business_templates": list(commands.TEMPLATES),
                      "host_capabilities": "not inspected"}
        elif args.command == "route":
            result = route(args.intent)
        elif args.command == "init":
            if args.demo:
                if any((args.name, args.currency, args.timezone, args.start, args.end)):
                    raise ValueError("Demo has fixed synthetic inputs; do not combine --demo with profile fields")
                result = demo()
            else:
                if not all((args.name, args.currency, args.timezone, args.start, args.end)):
                    raise ValueError("Profile initialization requires --name, --currency, --timezone, --start and --end")
                result = initialize(args.name, args.business_type, args.currency, args.timezone,
                                    args.minor_units, args.start, args.end)
        else:
            data = load(args.data)
            if args.command == "validate":
                result = {"schema_valid": True, "fact_verification": "not performed", "transactions": len(data["transactions"])}
            elif args.command == "kpis":
                result = calculate(data, args.start, args.end)
            elif args.command == "weekly-report":
                result = weekly_report(data, args.start, args.end)
                if args.format == "markdown":
                    result = markdown(result)
            elif args.command == "marketing-budget":
                result = marketing_budget(data, args.start, args.end, args.monthly_increase, args.contribution_margin)
        output = result if isinstance(result, str) else json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if getattr(args, "out", None):
            save_new(args.out, output)
            print(f"Saved {args.out}")
        else:
            print(output, end="" if output.endswith("\n") else "\n")
        return 0
    except (ValueError, OSError, sqlite3.Error, ValidationError, RuntimeError) as exc:
        print(f"SoloOS error: {exc}", file=sys.stderr)
        return 2
