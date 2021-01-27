"""
Helfer KLassen
"""
import re
import base64

import numpy as np

from PIL import Image
from io import BytesIO


def base64_to_pil(img_base64):
    """
    base64 Bild zu PIL
    """
    img_daten = re.sub('^data:image/.+;base64,', '', img_base64)
    pil = Image.open(BytesIO(base64.b64decode(img_daten)))
    return pil


def np_to_base64(img_np):
    """
    numpy image (RGB) zu base64 string
    """
    img_daten = Image.fromarray(img_np.astype('uint8'), 'RGB')
    buffered = BytesIO()
    img_daten.save(buffered, format="PNG")
    return u"data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")

