"""This code is adapted from https://github.com/TachibanaYoshino/AnimeGANv3
https://colab.research.google.com/drive/1XYNWwM8Xq-U7KaTOqNap6A-Yq1f-V-
FB?usp=sharing.

The original license is the following:
```
License

This repo is made freely available to academic and
non-academic entities for non-commercial purposes such
as academic research, teaching, scientific publications.
Permission is granted to use the AnimeGANv3 given
that you agree to my license terms. Regarding the
request for commercial use, please contact us via
email to help you obtain the authorization letter.

Author

Asher Chan
```
"""

from __future__ import annotations

import cv2
import huggingface_hub
import numpy as np
import onnxruntime as ort
import torch
from facenet_pytorch import MTCNN


class Model:
    def __init__(self):
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        self.face_detector = MTCNN(image_size=256,
                                   margin=80,
                                   min_face_size=128,
                                   thresholds=[0.7, 0.8, 0.9],
                                   device=self.device)
        self.model = self._load_model()

    @staticmethod
    def _load_model() -> ort.InferenceSession:
        path = './models/AnimeGANv3_PortraitSketch_25.onnx'
        breakpoint()
        return ort.InferenceSession(
            path, providers=['CPUExecutionProvider'])

    def detect_face(self, img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        batch_boxes, batch_probs, batch_points = self.face_detector.detect(
            img, landmarks=True)
        return batch_boxes, batch_points

    @staticmethod
    def margin_face(box: np.ndarray,
                    img_HW: tuple[int, int],
                    margin: float | None = None) -> list[int]:
        x1, y1, x2, y2 = box
        if margin is None:
            w = x2 - x1
            h = y2 - y1
            x1 = max(0, x1 - w / 2)
            y1 = max(0, y1 - h / 2)
            x2 = min(img_HW[1], x2 + w / 2)
            y2 = min(img_HW[0], y2 + h / 2)
        else:
            x1 = max(0, x1 - margin)
            y1 = max(0, y1 - margin)
            x2 = min(img_HW[1], x2 + margin)
            y2 = min(img_HW[0], y2 + margin)
        return list(map(int, [x1, y1, x2, y2]))

    @staticmethod
    def resize_image(img: np.ndarray, x32: bool = True) -> np.ndarray:
        h, w = img.shape[:2]
        ratio = h / w
        if x32:  # resize image to multiple of 32s

            def to_32s(x):
                return 256 if x < 256 else x - x % 32

            new_h = to_32s(h)
            new_w = int(new_h / ratio) - int(new_h / ratio) % 32
            img = cv2.resize(img, (new_w, new_h))
        return img

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        # BGR
        batch_boxes, batch_points = self.detect_face(image)
        if batch_boxes is None:
            print('No face detected!')
            return
        [x1, y1, x2, y2] = self.margin_face(batch_boxes[0], image.shape[:2])
        face_mat = image[y1:y2, x1:x2]
        face_mat = self.resize_image(face_mat)
        # BGR -> RGB
        face_mat = cv2.cvtColor(face_mat, cv2.COLOR_BGR2RGB)
        face_mat = face_mat.astype(np.float32) / 127.5 - 1.0
        face_mat = np.expand_dims(face_mat, axis=0)
        return face_mat

    def run_model(
        self, face_mat: np.ndarray, img_size: tuple[int, int] = (256, 256)
    ) -> np.ndarray:
        x = self.model.get_inputs()[0].name
        fake_img = self.model.run(None, {x: face_mat})
        output_image = (np.squeeze(fake_img) + 1.) / 2 * 255
        output_image = np.clip(output_image, 0, 255).astype(np.uint8)
        return output_image

    def run(self, image: np.ndarray) -> np.ndarray:
        # BGR -> RGB
        data = self.preprocess_image(image[:, :, ::-1])
        res = self.run_model(data)
        return res  # RGB