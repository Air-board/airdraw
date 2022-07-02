import random
from typing import Tuple

import cv2
import numpy as np

from collections import namedtuple

Batch = namedtuple('Batch', 'imgs, gt_texts, batch_size')


class Preprocessor:
    def __init__(self,
                 img_size: Tuple[int, int],
                 padding: int = 0,
                 dynamic_width: bool = False) -> None:

        # when padding is on, we need dynamic width enabled
        assert not (padding > 0 and not dynamic_width)

        self.img_size = img_size
        self.padding = padding
        self.dynamic_width = dynamic_width

    def process_img(self, img: np.ndarray) -> np.ndarray:
        """Resize to target size, apply data augmentation."""

        # there are damaged files in IAM dataset - just use black image instead
        if img is None:
            img = np.zeros(self.img_size[::-1])

        # data augmentation
        img = img.astype(np.float)

        if self.dynamic_width:
            ht = self.img_size[1]
            h, w = img.shape
            f = ht / h
            wt = int(f * w + self.padding)
            wt = wt + (4 - wt) % 4
            tx = (wt - w * f) / 2
            ty = 0
        else:
            wt, ht = self.img_size
            h, w = img.shape
            f = min(wt / w, ht / h)
            tx = (wt - w * f) / 2
            ty = (ht - h * f) / 2

        # map image into target image
        M = np.float32([[f, 0, tx], [0, f, ty]])
        target = np.ones([ht, wt]) * 255
        img = cv2.warpAffine(img, M, dsize=(wt, ht), dst=target, borderMode=cv2.BORDER_TRANSPARENT)

        # transpose for TF
        img = cv2.transpose(img)

        # convert to range [-1, 1]
        img = img / 255 - 0.5
        return img
