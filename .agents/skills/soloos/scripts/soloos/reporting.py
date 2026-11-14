"""Weekly management report with explicit gaps and reproducible evidence."""

from .finance import calculate
from .records import record


def weekly_report(data, start, end, recorded_at=None):
    kpis = calculate(data, start, end)
    if kpis["days"] != 7:
        raise ValueError("Weekly reports require exactly seven inclusive calendar days")
    priorities = ["Founder: reconcile incomplete evidence before making spending commitments."] if not kpis["complete"] else [
        "Founder: compare the period with a longer baseline before changing recurring spending.",
        "Founder: verify upcoming obligations and cash availability before approving a budget proposal.",
    ]
    payload = {"cadence": "weekly", "company_name": data["company"]["name"], "kpis": kpis, "priorities": priorities}
    return record("Report", data, payload, "estimate", recorded_at)


def markdown(report):
    payload, meta = report["payload"], report["metadata"]
    k = payload["kpis"]
    def show(key):
        return k[key] if k[key] is not None else "Unavailable"
    # Escape user-supplied names so they cannot inject HTML or extra Markdown rows.
    import html
    name = html.escape(payload["company_name"]).replace("\n", " ").replace("\r", " ").replace("|", "\\|")
    lines = [f"# SoloOS weekly executive report — {name}", "",
             f"Period: {k['start']} through {k['end']} (inclusive); timezone: {k['timezone']}.",
             f"Currency: {k['currency']}. Accounting basis: cash. Complete actuals: {k['complete']}.",
             f"Synthetic data: {report['synthetic']}. Generated: {meta['recorded_at']}.", "",
             "| Metric | Value |", "| --- | ---: |",
             f"| Revenue, net of refunds | {show('revenue')} |",
             f"| Expenses, net of refunds | {show('expenses')} |",
             f"| Cash-basis profit | {show('profit')} |",
             f"| Estimated runway, months | {show('runway_months')} |", "",
             f"Runway status: {k['runway_status']}.", "", "## Evidence and limitations", ""]
    lines.extend("- " + warning for warning in k["warnings"])
    if not k["complete"]:
        lines.append(f"- Partial observed totals (not full-period KPIs): {k['observed']}")
    lines += ["", "## Proposed priorities", ""] + ["- " + item for item in payload["priorities"]]
    lines += ["", "No external action was executed.", "", f"Report ID: {report['id']}",
              f"Provenance: {meta['provenance'][0]}", ""]
    return "\n".join(lines)
