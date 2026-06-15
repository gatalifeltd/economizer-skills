import decimal

def _load(account):
    return []

def reconcile_ledger(account, entries):
    total = decimal.Decimal(0)
    for e in entries:
        total += e.amount
    return total
