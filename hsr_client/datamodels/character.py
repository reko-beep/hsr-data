from pydantic import BaseModel, validator, Field, Extra
from typing import Optional
from hsr_client.routes import IMAGE_ROUTE, AUDIO_ROUTE
from hsr_client.constants import Item, _RelicTypes
from hsr_client.datamodels.searchItem import SearchItem

class DamageType(BaseModel):

    id : int
    iconPath : Optional[str] 
    color : Optional[str] 
    name : Optional[str]
    rarity: Optional[int] 

    @validator('iconPath', pre=True)
    def get_icon_path(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)
        return ''



class BaseType(BaseModel):

    id : int
    iconPath : Optional[str] 
    altIconPath : Optional[str]
    color : Optional[str] 
    rarity: Optional[int] 
    name : Optional[str]

    @validator('iconPath', pre=True)
    def get_icon_path(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)
        return ''


class LevelData(BaseModel):

    promotion : int
    max : int  = Field(alias='maxLevel')
    base_atk : float = Field(alias='attackBase')
    add_atk : float = Field(alias='attackAdd')
    base_hp : float = Field(alias='hpBase')
    add_hp : float = Field(alias='hpAdd')
    base_def : float = Field(alias='defenseBase')
    add_def : float = Field(alias='defenseAdd')
    crit_rate : float = Field(alias='crate')
    crit_damage : float = Field(alias='cdmg')
    aggro : int 
    base_speed : int = Field(alias='speedBase')
    add_speed : int = Field(alias='speedAdd')
    cost : list[SearchItem]

    @validator('cost', pre=True)
    def get_materials(cls, v):

        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(SearchItem(**item))
        return list_

class Rank(BaseModel):
    id : int
    iconPath : str
    artPath : str
    description : str = Field(alias='descHash')
    params : list[int]

    @validator('iconPath', pre=True)
    def get_icon_path(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)
        return ''

    @validator('artPath', pre=True)
    def get_art_path(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)
        return ''

class SkillLevel(BaseModel):
    level : int
    params : list[int]
    req_level : int = Field(alias='levelReq')
    req_promotion : int = Field(alias='promotionReq')
    cost : list[SearchItem]

    @validator('cost', pre=True)
    def get_materials(cls, v):

        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(SearchItem(**item))
        return list_


class Skill(BaseModel):

    id : int
    name : str
    target: str = Field(alias='tagHash')
    type : str = Field(alias='typeDescHash')
    iconPath : Optional[str]
    req_level : int = Field(alias='levelReq')
    req_promotion : int = Field(alias='promotionReq')
    levels : list[SkillLevel] = Field(alias='levelData')

    @validator('iconPath', pre=True)
    def get_icon_path(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)

    @validator('levels', pre=True)
    def get_skill_levels(cls, v):
        list_ = []
        if len(v) != 0:
            for lvl in v:
                list_.append(SkillLevel(**lvl))
        return v

class BuffStatus(BaseModel):
    value : float
    key : str

class Buff(BaseModel):
    id : int
    name: str
    req_level : int = Field(alias='levelReq')
    iconPath : str
    status : list[BuffStatus] = Field(alias='statusList')
    cost: list[SearchItem]

    @validator('status', pre=True)
    def get_buff_status(cls, v):

        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(BuffStatus(**item))
        return list_

    @validator('cost', pre=True)
    def get_materials(cls, v):

        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(SearchItem(**item))
        return list_


    
class BonusSkill(BaseModel):
    id : int
    name : str
    description : str = Field(alias='descHash')
    iconPath : str
    req_level : int = Field(alias='levelReq')
    req_promotion : int = Field(alias='promotionReq')
    levels: list[SkillLevel] = Field(alias='levelData')

    @validator('iconPath', pre=True)
    def get_icon_path(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)

    @validator('levels', pre=True)
    def get_skill_levels(cls, v):
        list_ = []
        if len(v) != 0:
            for lvl in v:
                list_.append(SkillLevel(**lvl))
        return v


class SubSkill(BaseModel):
    id : int
    type : int
    sub_skills : list = Field(alias='children')
    buff : Optional[Buff] = Field(alias='embedBuff')
    cost: Optional[list[SearchItem]]
    bonus_skill : Optional[BonusSkill] = Field(alias='embedBonusSkill')


    @validator("sub_skills", pre=True)
    def get_sub_skills(cls, v):
        list_ = []
        if len(v) != 0:
            for item in v:
                checker = {}                
                checker['has_subskills'] = 'children' in item
                checker['has_buff'] = 'buff' in item or 'embedBuff' in item
                checker['has_bonus'] = 'embedBonusSkill' in item

                list_.append(SubSkill(**{**item, **checker}))
        return list_

    @validator("buff", pre=True)
    def get_buff(cls, v):

        if len(v) != 0:
            return Buff(**v)
        return v
    
    @validator('cost', pre=True)
    def get_materials(cls, v):

        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(SearchItem(**item))
        return list_
    
class SkillTreePoints(BaseModel):
    id : int
    type : int
    sub_skills : list = Field(alias='children')
    buff : Optional[Buff]
    bonus_skill : Optional[BonusSkill] = Field(alias='embedBonusSkill')
    has_bonus : Optional[bool]
    has_buff : Optional[bool]
    has_subskills : Optional[bool]

    
    @validator("sub_skills", pre=True)
    def get_sub_skills(cls, v):
        list_ = []
        if len(v) != 0:
            for item in v:
                checker = {}                
                checker['has_subskills'] = 'children' in item
                checker['has_buff'] = 'buff' in item or 'embedBuff' in item
                checker['has_bonus'] = 'embedBonusSkill' in item

                list_.append(SubSkill(**{**item, **checker}))
        return list_

    @validator("buff", pre=True)
    def get_buff(cls, v):  
              
        if len(v) != 0:
            return Buff(**v)
        return ''
    
    @validator("bonus_skill", pre=True)
    def get_bonus_skill(cls, v):
        if len(v) != 0:
            return BonusSkill(**v)
        return ''
    
class RelicProps(BaseModel):
    type : _RelicTypes = Field(alias='relicTypeHash')
    type_icon : str = Field(alias='relicTypeIcon')
    prop : str = Field(alias='propertyName')    
    prop_icon : str = Field(alias='propertyIconPath')

    @validator('type', pre=True)
    def get_relic_type(cls, v):
        return _RelicTypes(v)
    
    @validator('type_icon', pre=True)
    def get_relic_type_icon(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)
        
    @validator('prop_icon', pre=True)
    def get_relic_prop_icon(cls, v):
        if v != "":
            return IMAGE_ROUTE.format(assetId=v)



class RecommendedRelics(BaseModel):

    two_piece : list = Field(alias='twoPcSets')
    four_piece  : list = Field(alias='fourPcSets')
    recommended_props : list[RelicProps] = Field(alias='props')

    @validator("recommended_props", pre=True)
    def get_rec_props(cls, v):
        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(RelicProps(**item))
        return list_

class VoiceNote(BaseModel):

    id : int
    title : str
    text : str
    unlock: str = Field(alias='unlockRequirement')
    cn : str = Field(alias='cnUrl')
    en : str = Field(alias='enUrl')
    kr : str = Field(alias='krUrl')
    jp : str = Field(alias='jpUrl')

    @validator('cn', pre=True)
    def get_cn_url(cls, v):
        if v != '':
            return AUDIO_ROUTE.format(assetId=v)
        
    @validator('jp', pre=True)
    def get_jp_url(cls, v):
        if v != '':
            return AUDIO_ROUTE.format(assetId=v)
    
    @validator('kr', pre=True)
    def get_kr_url(cls, v):
        if v != '':
            return AUDIO_ROUTE.format(assetId=v)
    
    @validator('en', pre=True)
    def get_en_url(cls, v):
        if v != '':
            return AUDIO_ROUTE.format(assetId=v)

class Character(BaseModel):

    name: str
    spRequirement : int
    rarity: int
    description : str = Field(alias='descHash')
    iconPath : Optional[str] 
    figPath : Optional[str] 
    fgPath : Optional[str] 
    bgPath : Optional[str] 
    artPath :Optional[str] 
    miniIconPath : Optional[str] 
    splashIconPath : Optional[str] 
    element : DamageType = Field(alias='damageType')
    baseType : BaseType = Field(alias='baseType')
    levels : list[LevelData] = Field(alias='levelData')
    ranks : list[Rank]
    skills : list[Skill]
    skill_points : list[SkillTreePoints] = Field(alias='skillTreePoints')
    relics : RecommendedRelics = Field(alias='relicRecommend')
    voice_lines : list[VoiceNote] = Field(alias='voiceItems')

    
    class Config:
        extra = Extra.ignore

    @validator('iconPath', pre=True)
    def get_icon_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v
    
    @validator('figPath', pre=True)
    def get_fig_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v
    
        
    @validator('fgPath', pre=True)
    def get_fg_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v
    
    @validator('bgPath', pre=True)
    def get_bg_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v
    
        
    @validator('miniIconPath', pre=True)
    def get_miniIcon_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v
    
        
    @validator('splashIconPath', pre=True)
    def get_splashIcon_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v
    
    @validator('artPath', pre=True)
    def get_art_path(cls, v):
        if v != '':
            return IMAGE_ROUTE.format(assetId=v)
        return v

    @validator('element', pre=True)
    def get_damage_type(cls, v):
        return DamageType(**v)

    @validator('baseType', pre=True)
    def get_base_type(cls, v):

        return BaseType(**v)
    
    @validator('levels', pre=True)
    def get_levels(cls, v):
        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(LevelData(**item))

        return list_
    
    @validator('ranks', pre=True)
    def get_ranks(cls, v):
        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(Rank(**item))
        return list_
    
    @validator('skills', pre=True)
    def get_skills(cls ,v):
        list_ = []
        if len(v) != 0:
            for item in v:
                list_.append(Skill(**item))
        return list_
    
    @validator('skill_points', pre=True)
    def get_skill_points(cls ,v):
        list_ = []
        if len(v) != 0:
            for item in v:
                checker = {}                
                checker['has_subskills'] = 'children' in item
                checker['has_buff'] = 'buff' in item or 'embedBuff' in item
                checker['has_bonus'] = 'embedBonusSkill' in item

                list_.append(SkillTreePoints(**{**item, **checker}))
        return list_

    @validator('relics', pre=True)
    def get_relics(cls, v):

        if len(v) != 0:
            return RecommendedRelics(**v)

        return ''
    
    @validator('voice_lines', pre=True)
    def get_vl(cls, v):
        list_ = []
        if len(v) != 0:
            for item in v:
               list_.append(VoiceNote(**item))

        return list_



    


