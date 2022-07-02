import cv2
from path import Path
from typing import List
from collections import namedtuple

from dl_model import Model, DecoderType
from image_preprocessor import Preprocessor
from firebase_uploader import FilestoCloud

Batch = namedtuple('Batch', 'imgs, gt_texts, batch_size')


class ImagePrediction:

    def __init__(self, cropped_path='cropped.png'):
        self.cropped_path = cropped_path

    def char_list_from_file(self) -> List[str]:
        with open('model/charList.txt') as f:
            return list(f.read())

    def infer(self, model: Model, fn_img: Path) -> None:
        """Recognizes text in image provided by file path."""
        img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)
        assert img is not None
        preprocessor = Preprocessor((128, 32), dynamic_width=True, padding=16)
        img = preprocessor.process_img(img)

        batch = Batch([img], None, 1)
        recognized, probability = model.infer_batch(batch, True)
        print(f'Recognized: "{recognized[0]}"')
        print(f'Probability: {probability[0]}')
        file_to_upload = FilestoCloud(recognized[0])
        file_to_upload.upload_file()

    def predict(self):
        model = Model(self.char_list_from_file(), DecoderType.BestPath, must_restore=True)
        self.infer(model, self.cropped_path)
