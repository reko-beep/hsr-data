from typing import List
from bs4 import BeautifulSoup
from hsr_client.backend.srs_backend import SRSBackend
import hsr_client.datamodels as models
from hsr_client.datamodels.material import MaterialCount

from  hsr_client.datamodels import trace
from hsr_client.errors import BackendError


def additional_info(trace_node):
    container =  trace_node.get("embedBuff") or trace_node.get("embedBonusSkill")
    if container is None:
        # TODO: log this, this might hint that the backend response structure has changed.
        raise ValueError("trace data doesn't have a additional info, TODO: fix this error message")
    return container


def parse_non_skill_traces(trace_nodes, traces=[], parent=None) -> List[trace.Trace]:
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
        unlock_prerequisite = trace.UnlockPrerequisite(
                trace=parent,
                level=info["levelReq"],
                ascension=additional_info(trace_node)["promotionReq"]
        )

        # prepare tht trace itself.
        if trace_node["type"] == 1:
            _trace = trace.BonusAbility(
                name=name,
                description=t_description,
                activation_mats=[],
                unlock_prerequisite=unlock_prerequisite
            )

        elif trace_node["type"] == 2:
            _trace = trace.StatBonus(
                name=name,
                description=t_description,
                activation_mats=[],
                unlock_prerequisite=unlock_prerequisite
            )
        
        else:
            raise BackendError("Invalid trace type(int) found: ", trace_node["type"])

        traces.append(_trace)

        # parse child traces
        children = trace_node.get("children")
        if children is not None or children != []:
            parse_non_skill_traces(children, traces, parent=_trace)


    return []

# def parse_skill_traces(raw_skills, srs_be: SRSBackend):
#     for raw_skill in raw_skills:
#         # name
#         skill_name = raw_skill['name']

#         # scaling: LevelScaling
        
#         desc_template = BeautifulSoup(
#             raw_skills["descHash"], features="lxml"
#         ).get_text()

#         template_params_all_levels = map(
#             lambda d: d['params'],
#             raw_skills["levelData"]
#         )

#         for level, level_data in raw_skills['levelData']:
#             template_params = level_data['params']
#             skill_desc = desc_template
            
#             for slot_no, template_param in enumerate(template_params, start=1):
#                 replace_text = f"#{slot_no}[i]"
#                 # print("replacing: " + replace_text + " with " + str(template_param) + " in " + ability_desc)
#                 skill_desc = skill_desc.replace(replace_text, str(template_param))

            

#             raw_matcounts =level_data['cost']

#             ascension_mats_per_level = []
#             for raw_matcount in raw_matcounts:
#                 mat_id = raw_matcount['id']

#                 from hsr_client.backend.srs_backend.parsers.material import parse_material
#                 mat = parse_material(mat_id, srs_be)
                
                
#                 mat_count = raw_matcount['count']

#                 ascension_mats_per_level.append(
#                     MaterialCount(
#                     material=mat,
#                     count = mat_count,
#                     )
#                 )



# def parse_traces(raw_character_data, srs_be: SRSBackend)  -> List[models.trace.Trace]:
#     non_skill_traces = []
#     parse_non_skill_traces(raw_character_data['skillTreePoints'], non_skill_traces)
#     skill_traces = parse_skill_traces(raw_character_data['skills'])

#     return [*non_skill_traces, *skill_traces]