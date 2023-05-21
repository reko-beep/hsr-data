from bs4 import BeautifulSoup
import hsr_client.datamodels as models




def additional_info(trace_node):
    container =  trace_node.get("embedBuff") or trace_node.get("embedBonusSkill")
    if container is None:
        # TODO: log this, this might hint that the backend response structure has changed.
        raise ValueError("trace data doesn't have a additional info, TODO: fix this error message")
    return container


def parse_traces(trace_nodes, traces=[], parent=None) -> list[models.trace.Trace]:
    for trace_node in trace_nodes:
        
        info = additional_info(trace_node)

        # extract name
        name = info["name"]

        # prepare description
        t_description =  info.get("descHash")

        if t_description is not None:
            t_description = BeautifulSoup(t_description, features='lxml').get_text()
            template_params = info['levelData'][0]['params']

            for slot_no, template_param in enumerate(template_params, start=1):
                replace_text = f"#{slot_no}[i]"
                t_description = t_description.replace(replace_text, str(template_param))

        else:
            desc_name = BeautifulSoup(info['statusList'][0]["key"], features='lxml').get_text()
            desc_value = str(info['statusList'][0]["value"] * 100)
            t_description = f"{desc_name}: {desc_value}"



        # prepare unlock preprequisite
        unlock_prerequisite = models.trace.UnlockPrerequisite(
                trace=parent,
                level=info["levelReq"],
                ascension=additional_info(trace_node)["promotionReq"]
        )

        # prepare tht trace itself.
        if trace_node["type"] == 1:
            _trace = models.trace.BonusAbility(
                name=name,
                description=t_description,
                activation_mats=[],
                unlock_prerequisite=unlock_prerequisite
            )

        elif trace_node["type"] == 2:
            _trace = models.trace.StatBonus(
                name=name,
                description=t_description,
                activation_mats=[],
                unlock_prerequisite=unlock_prerequisite
            )

        traces.append(_trace)

        # parse child traces
        children = trace_node.get("children")
        if children is not None:
            parse_traces(children, traces, parent=_trace)
