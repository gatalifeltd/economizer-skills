#!/usr/bin/env python3
"""Generate a synthetic ~150k-token codebase fixture for the heavy multi-turn benchmark.

Deterministic (fixed strings, no RNG seeding needed for reproducibility of size).
The repo is plausible-looking Python with long modules, cross-references, a few
TODO/FIXME markers, and a traceable "payment -> ledger" flow — chosen to tempt a
verbose agent into quoting large chunks (which is exactly what the economy rules
suppress). Run:  python3 generate.py
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "codebase")

MODULES = {
    "api/gateway": ("HTTP gateway: routes inbound requests to services.", 14),
    "api/auth": ("Authentication and session handling.", 10),
    "billing/charge": ("Charge orchestration; entry point charge_customer().", 16),
    "billing/ledger": ("Double-entry ledger; reconcile_ledger() lives here.", 18),
    "billing/invoice": ("Invoice generation and PDF rendering.", 12),
    "payments/provider": ("Payment provider adapters (stripe-like).", 16),
    "payments/retry": ("Retry/backoff logic for failed charges.", 10),
    "payments/webhook": ("Inbound webhook verification + dispatch.", 12),
    "core/config": ("Config loading and feature flags.", 8),
    "core/events": ("Internal event bus.", 10),
    "core/cache": ("LRU + TTL caches.", 12),
    "store/repo": ("Repository pattern over the DB.", 16),
    "store/migrations": ("Schema migrations.", 10),
    "util/dates": ("Date parsing/formatting helpers.", 8),
    "util/money": ("Decimal money type and rounding.", 10),
    "workers/scheduler": ("Background job scheduler.", 12),
    "workers/dispatch": ("Job dispatch + worker pool.", 12),
    "report/metrics": ("Metrics aggregation for dashboards.", 14),
}

FUNC_BODY = '''\
def {name}({args}):
    """{doc}"""
    # step 1: validate inputs
    if not {arg0}:
        raise ValueError("{name}: missing {arg0}")
    # step 2: load dependencies
    ctx = _context_for({arg0})
    result = {{}}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{{i}}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor={factor})
    # step 4: persist + emit
    _persist(result, table="{table}")
    events.emit("{name}.done", count=len(result))
    return result
'''

HELPERS = '''\
def _context_for(x):
    return {"items": [{"key": f"row{i}", "value": i * 3} for i in range(5)]}

def _transform(v, factor=1):
    return (v * factor) % 1000

def _persist(rows, table):
    # TODO: batch writes; current impl does one round-trip per row
    return len(rows)
'''


def make_module(path, doc, nfuncs):
    head = f'"""{path}: {doc}\n\nAuto-generated module for benchmark fixture.\n"""\n'
    head += "from core import events\n\n" + HELPERS + "\n\n"
    tail = path.split("/")[-1]
    funcs = []
    for i in range(nfuncs):
        name = f"{tail}_op_{i}"
        args = "payload, factor=2, table='t'"
        funcs.append(FUNC_BODY.format(
            name=name, args=args, arg0="payload", doc=f"Operation {i} of {path}.",
            factor=(i % 7) + 1, table=tail))
    # cross-reference hook to make tracing meaningful
    if path == "billing/charge":
        funcs.append(
            "def charge_customer(customer_id, amount):\n"
            '    """Public entrypoint: charge a customer and post to the ledger."""\n'
            "    from billing import ledger\n"
            "    from payments import provider, retry\n"
            "    txn = retry.with_backoff(lambda: provider.capture(customer_id, amount))\n"
            "    return ledger.reconcile_ledger(customer_id, [txn])\n")
    if path == "billing/ledger":
        funcs.append(
            "def reconcile_ledger(account, entries):\n"
            '    """Post entries to the double-entry ledger and return the balance."""\n'
            "    from util import money\n"
            "    total = money.zero()\n"
            "    for e in entries:\n"
            "        total = money.add(total, e.get('amount', 0))\n"
            "    _persist({'balance': total}, table='ledger')\n"
            "    return total\n")
    return head + "\n\n".join(funcs) + "\n"


def main():
    nfiles = nchars = 0
    for path, (doc, nfuncs) in MODULES.items():
        full = os.path.join(ROOT, "src", path + ".py")
        os.makedirs(os.path.dirname(full), exist_ok=True)
        content = make_module(path, doc, nfuncs)
        open(full, "w").write(content)
        nfiles += 1
        nchars += len(content)
    # a big verbose log to tempt dumping
    log = "\n".join(
        f"2026-06-1{(i//900)%10}T12:{(i//60)%60:02d}:{i%60:02d}Z "
        f"{'ERROR' if i % 137 == 0 else 'INFO'} [svc{i%9}] "
        f"request {i} handled in {i%400}ms trace={i*7%99999}"
        for i in range(4000))
    open(os.path.join(ROOT, "var", "app.log"), "w") if False else None
    os.makedirs(os.path.join(ROOT, "var"), exist_ok=True)
    open(os.path.join(ROOT, "var", "app.log"), "w").write(log + "\n")
    nfiles += 1; nchars += len(log)
    print(f"generated {nfiles} files, ~{nchars:,} chars (~{nchars//4:,} tokens est.)")


if __name__ == "__main__":
    main()
