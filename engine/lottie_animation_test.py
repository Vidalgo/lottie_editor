from __future__ import annotations

import json

from pydantic import BaseModel, Field, confloat, conint, validator, conlist
from typing import List, Optional, Any

import random
from os import makedirs, path

# from vidalgo_lottie_base import Vidalgo_lottie_base, ID_SUFFIX, PATH
# from helpers import update_intersected_ids, store_json
#
# from metadata import Metadata
# from font import Font
# from char import Char
# from image_asset import Image_asset
# from precomposition import Precomposition
# from layer import Layer, Lottie_layer_type, find_layer, add_layer, delete_layer, replace_layer, update_ref_id
# from precomp_layer import Precomp_layer
# from text_layer import Text_layer, refactor_font_name


class Lottie_animation(BaseModel):
    version: Optional[str] = Field(..., alias='v')
    frame_rate: float = Field(..., alias='fr')
    in_point: float = Field(..., alias='ip')
    out_point: float = Field(..., alias='op')
    width: int = Field(..., alias='w')
    height: int = Field(..., alias='h')
    three_dimensional: Optional[int] = Field(..., alias='ddd')
    assets: Optional[list] = Field(..., alias='assets')
    fonts: Optional[list]
    chars: Optional[list]
    layers: list = Field(..., alias='layers')
    meta: Optional[list] = Field(alias='meta')
    markers: Optional[list] = Field(alias='markers')
    motion_blur: Optional[dict] = Field(alias='mb')



def main() -> None:
    """Main function."""

    data = open("D:\\lottie_files_path\\coin.json")
    json_obj = json.load(data)
    la = Lottie_animation(**json_obj)
    #data = json.load("D:\\lottie_files_path\\coin.json")
    pass

if __name__ == "__main__":
    main()
