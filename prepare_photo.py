import os
import sys
from PIL import Image
import numpy as np
import cv2
from copy import deepcopy

path = sys.argv[-1]
filenames = os.listdir(path)
new_path = "./ars_electronica"

for f in filenames:
    fname = os.path.join(path, f)
    img = deepcopy(Image.open(fname))
    new_img = Image.new("RGB", img.size, "BLACK")
    new_img.paste(img, mask=img)

    np_img = np.asarray(new_img)
    cv_img = deepcopy(cv2.imread(fname))
    positions = np.nonzero(cv_img)

    top = positions[0].min()
    bottom = positions[0].max()
    left = positions[1].min()
    right = positions[1].max()

    lborder = max(left - 15, 0)
    rborder = min(right + 15, cv_img.shape[1])
    uborder = max(0, top - 15)
    bborder = min(bottom + 15, cv_img.shape[0])

    output_np = np_img[uborder:bborder, lborder:rborder]
    output = Image.fromarray(output_np).convert("RGB")
    
    # resize
    (W, H) = output.size
    
    if H > 1024:
        output = output.resize((int((1024 / H) * W), 1024))
    # elif W > 512:
    #     img = img.resize((int((512 / W) * H), 512))
    (nW, nH) = output.size

    new_img = Image.new("RGB", (512, 1024), "BLACK")
    bg_center = (512 // 2, 1024 // 2)
    fg_left = bg_center[0] - nW // 2
    fg_top = bg_center[1] - nH // 2
    fg_position = (fg_left, fg_top)
    new_img.paste(output, fg_position)

    new_img.save(os.path.join(new_path, f))
