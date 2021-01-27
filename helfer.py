# Helfer Klassen
import numpy as np
import re # regex
import base64
from PIL import Image
from io import BytesIO

# base64 zu PIL image
def base64_to_pil(img_base64):
    # bild aus request
    # metadaten prefix entfernen
    img_daten = re.sub('^data:image/.+;base64,', '', img_base64)
    # base64 decode
    pil = Image.open(BytesIO(base64.b64decode(img_daten)))
    return pil

# np-array (RGB) zu base64 string (png)
def np_to_base64(img_np):
    # np array zu bild
    img_daten = Image.fromarray(img_np.astype('uint8'), 'RGB')
    # bilddaten zu png (bytesIO -> schneller, weil in memory)
    buffered = BytesIO()
    img_daten.save(buffered, format="PNG")
    return u"data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")
