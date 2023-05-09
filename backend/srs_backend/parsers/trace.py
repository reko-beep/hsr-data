import datamodels as models


def get_trace_name(trace_node):
    container =  trace_node.get("embedBuff") or trace_node.get("embedBonusSkill")
    if container is None:
        # TODO: log this, this might hint that the backend response structure has changed.
        raise ValueError("trace data doesn't have a name.")
    return container["name"]


def get_trace_type(trace_node):
    # type 1: "Bonus Ability"
    # type 2: "Stat Bonus"
    raw_type = trace_node["type"]
    if raw_type == 1:
        return models.trace.Type.BONUS_ABILITY
    elif raw_type == 2:
        return models.trace.Type.STAT_BONUS
    else:
        raise ValueError(f"unknown type found in trace node: type = {raw_type}")

def parse_trace_data(trace_nodes, traces=[], parent=None) -> list[models.trace.Trace]:
    for trace_node in trace_nodes:
        
        # extract name
        name = get_trace_name(trace_node)
        # extract type
        type = get_trace_type(trace_node)

        # prepare unlock criteria
        unlock_criteria = models.trace.UnlockCriteria(
                trace=parent
        )

        _trace = models.trace.Trace(
            name=name,
            type=type,
            unlock_criteria=unlock_criteria
        )

        traces.append(_trace)

        # parse child traces
        children = trace_node.get("children")
        if children is not None:
            parse_trace_data(children, traces, parent=_trace)
