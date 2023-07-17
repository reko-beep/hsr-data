from typing import Generator
from collections import defaultdict
import data_query.shared_data.shared_var as SharedVar


def trace_namedskills(content) -> dict:
    traces_data: list = content.get("skillTreePoints")
    named_traceslist = []
    for index, data in enumerate(traces_data):
        trace_skill = data.get("embedBonusSkill")
        children1 = data.get("children")
        if trace_skill is None:
            continue
        name = trace_skill.get("name")
        deschash = trace_skill.get("descHash")
        level_data = trace_skill.get("levelData")
        for data in level_data:
            level = data.get("level")
            params = data.get("params")
        output = "trace"
        readable_deschash = SharedVar.readable_descHash(
            name, params, deschash, level, output
        )
        readable_deschash_punctuations = SharedVar.correct_punctuations(
            readable_deschash
        )
        named_traceslist.append((readable_deschash_punctuations, children1))
    return named_traceslist


def trace_embedbuffs(named_skills):
    embedskill_buffs = defaultdict(list)
    for data in named_skills:
        name: str = data[0]
        infos: list = data[1]  # list with length 1 :)
        for info in infos:
            childrens: dict = info
            embed_buff0 = childrens.get("embedBuff")
            embedskill_buffs[name] += [embed_buff0]
            children1 = childrens.get("children")
            for data1 in children1:
                embed_buff1 = data1.get("embedBuff")
                embedskill_buffs[name] += [embed_buff1]
                children2 = data1.get("children")
                if len(children2) == 0:
                    embed_buff2 = None
                for data2 in children2:
                    embed_buff2 = data2.get("embedBuff")
                    embedskill_buffs[name] += [embed_buff2]
    return dict(embedskill_buffs)


def skilltree_points(content) -> Generator[dict, None, None]:
    traces_data: list = content["skillTreePoints"]
    for data in traces_data:
        yield data


def skilltreepoints_embedbuff_children0(content):  # detached embed buffs
    skilltree = skilltree_points(content)
    for data in skilltree:
        embedBuff0 = data.get("embedBuff")
        if embedBuff0 is None:
            continue
        yield embedBuff0
