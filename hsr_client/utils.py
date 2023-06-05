
from __future__ import annotations

from hsr_client.errors import InvalidFilter

from typing import Any, Union
from dataclasses import dataclass
from pydantic import BaseModel

from PIL import Image, ImageChops, ImageOps, ImageDraw, ImageFont, ImageFilter

from datetime import datetime
import inspect
import requests
from io import BytesIO
from colorthief import ColorThief

from datetime import date, timedelta
import calendar

import random

def generate_t(input):
    t = 0

    for n in range(len(input)):
        t = (t << 5) -t + list(bytes(input, encoding="utf8"))[n]
        t = t & t
    t = t % (2**32) 
    return t

def base36encode(number):
    if not isinstance(number, int):
        raise TypeError('number must be an integer')
    is_negative = number < 0
    number = abs(number)

    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36
    if is_negative:
        base36 = '-' + base36

    return base36.lower() or alphabet[0].lower()

def check(model : BaseModel, attribute : str, value : Union[str, bool, int]) -> BaseModel:
    """checks in a model for attribute and returns it if attributes matches the value given
    to be used for 

    Args:
        model (SearchItem): SearchItem model
        attribute (str): attribute of searchItem
        value (Union[str, bool, int]): value to match

    Raises:
        InvalidFilter: raised when provided attribute [filter] doesnot exist in search item

    Returns:
        SearchItem: 
    """    

    if hasattr(model, attribute):


        if isinstance(model.__getattribute__(attribute), str):
            if value.lower() in model.__getattribute__(attribute).lower():
                return model
        
        if value == model.__getattribute__(attribute):
            return model
    
    raise InvalidFilter(model.available_filters())
        











def get_weekday(date : date):

    return calendar.weekday(date.year, date.month, date.day)

    
def get_monday(date : date):
    return date - timedelta(days=get_weekday(date))



def logc(*msg):
    stack = inspect.stack()
    class_name = stack[1][0].f_locals["self"].__class__.__name__
    print(f"[{class_name}] at [{datetime.now().strftime('%c')}] - ", *msg)





                        

