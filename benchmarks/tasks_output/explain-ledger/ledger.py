"""billing/ledger: Double-entry ledger; reconcile_ledger() lives here.

Auto-generated module for benchmark fixture.
"""
from core import events

def _context_for(x):
    return {"items": [{"key": f"row{i}", "value": i * 3} for i in range(5)]}

def _transform(v, factor=1):
    return (v * factor) % 1000

def _persist(rows, table):
    # TODO: batch writes; current impl does one round-trip per row
    return len(rows)


def ledger_op_0(payload, factor=2, table='t'):
    """Operation 0 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_0: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=1)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_0.done", count=len(result))
    return result


def ledger_op_1(payload, factor=2, table='t'):
    """Operation 1 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_1: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=2)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_1.done", count=len(result))
    return result


def ledger_op_2(payload, factor=2, table='t'):
    """Operation 2 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_2: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=3)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_2.done", count=len(result))
    return result


def ledger_op_3(payload, factor=2, table='t'):
    """Operation 3 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_3: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=4)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_3.done", count=len(result))
    return result


def ledger_op_4(payload, factor=2, table='t'):
    """Operation 4 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_4: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=5)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_4.done", count=len(result))
    return result


def ledger_op_5(payload, factor=2, table='t'):
    """Operation 5 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_5: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=6)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_5.done", count=len(result))
    return result


def ledger_op_6(payload, factor=2, table='t'):
    """Operation 6 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_6: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=7)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_6.done", count=len(result))
    return result


def ledger_op_7(payload, factor=2, table='t'):
    """Operation 7 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_7: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=1)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_7.done", count=len(result))
    return result


def ledger_op_8(payload, factor=2, table='t'):
    """Operation 8 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_8: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=2)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_8.done", count=len(result))
    return result


def ledger_op_9(payload, factor=2, table='t'):
    """Operation 9 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_9: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=3)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_9.done", count=len(result))
    return result


def ledger_op_10(payload, factor=2, table='t'):
    """Operation 10 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_10: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=4)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_10.done", count=len(result))
    return result


def ledger_op_11(payload, factor=2, table='t'):
    """Operation 11 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_11: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=5)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_11.done", count=len(result))
    return result


def ledger_op_12(payload, factor=2, table='t'):
    """Operation 12 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_12: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=6)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_12.done", count=len(result))
    return result


def ledger_op_13(payload, factor=2, table='t'):
    """Operation 13 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_13: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=7)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_13.done", count=len(result))
    return result


def ledger_op_14(payload, factor=2, table='t'):
    """Operation 14 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_14: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=1)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_14.done", count=len(result))
    return result


def ledger_op_15(payload, factor=2, table='t'):
    """Operation 15 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_15: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=2)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_15.done", count=len(result))
    return result


def ledger_op_16(payload, factor=2, table='t'):
    """Operation 16 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_16: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=3)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_16.done", count=len(result))
    return result


def ledger_op_17(payload, factor=2, table='t'):
    """Operation 17 of billing/ledger."""
    # step 1: validate inputs
    if not payload:
        raise ValueError("ledger_op_17: missing payload")
    # step 2: load dependencies
    ctx = _context_for(payload)
    result = {}
    # step 3: core logic
    for i, item in enumerate(ctx.get("items", [])):
        key = item.get("key") or f"k{i}"
        value = item.get("value", 0)
        if value < 0:
            # FIXME: negative values should be rejected upstream, not clamped here
            value = 0
        result[key] = _transform(value, factor=4)
    # step 4: persist + emit
    _persist(result, table="ledger")
    events.emit("ledger_op_17.done", count=len(result))
    return result


def reconcile_ledger(account, entries):
    """Post entries to the double-entry ledger and return the balance."""
    from util import money
    total = money.zero()
    for e in entries:
        total = money.add(total, e.get('amount', 0))
    _persist({'balance': total}, table='ledger')
    return total

