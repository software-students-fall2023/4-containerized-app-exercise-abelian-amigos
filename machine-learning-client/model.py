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


import cv2

import numpy as np
import onnxruntime as ort
import torch
from facenet_pytorch import MTCNN
from ml_server_defaults import MODELS_DIR


class Model:
    """
    A class to represent the model that converts images to sketches.
    """

    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.face_detector = MTCNN(
            image_size=256,
            margin=80,
            min_face_size=128,
            thresholds=[0.7, 0.8, 0.9],
            device=self.device,
        )
        self.model = self._load_model()

    @staticmethod
    def _load_model() -> ort.InferenceSession:
        """
        Load the model from the path.
        """
        return ort.InferenceSession(
            MODELS_DIR / "AnimeGANv3_PortraitSketch_25.onnx",
            providers=["CPUExecutionProvider"],
        )

    def detect_face(self, img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Detect face in the image and return the bounding box and the landmarks.
        """
        batch_boxes, _, batch_points = self.face_detector.detect(img, landmarks=True)
        return batch_boxes, batch_points

    @staticmethod
    def margin_face(
        box: np.ndarray, img_hw: tuple[int, int], margin: float | None = None
    ) -> list[int]:
        """
        Get the margin of the face.
        """
        x1, y1, x2, y2 = box
        if margin is None:
            w = x2 - x1
            h = y2 - y1
            x1 = max(0, x1 - w / 2)
            y1 = max(0, y1 - h / 2)
            x2 = min(img_hw[1], x2 + w / 2)
            y2 = min(img_hw[0], y2 + h / 2)
        else:
            x1 = max(0, x1 - margin)
            y1 = max(0, y1 - margin)
            x2 = min(img_hw[1], x2 + margin)
            y2 = min(img_hw[0], y2 + margin)
        return list(map(int, [x1, y1, x2, y2]))

    @staticmethod
    def resize_image(img: np.ndarray, x32: bool = True) -> np.ndarray:
        """
        Resize the image to a multiple of 32s.
        """
        h, w = img.shape[:2]
        ratio = h / w
        if x32:  # resize image to multiple of 32s
            new_h = 256 if h < 256 else h - h % 32
            new_w = int(new_h / ratio) - int(new_h / ratio) % 32
            img = cv2.resize(img, (new_w, new_h))
        return img

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess the image for the model.
        """
        # BGR
        batch_boxes, _ = self.detect_face(image)
        if batch_boxes is None:
            return np.ndarray((0))
        [x1, y1, x2, y2] = self.margin_face(
            batch_boxes[0], (image.shape[0], image.shape[1])
        )
        face_mat = image[y1:y2, x1:x2]
        face_mat = self.resize_image(face_mat)
        # BGR -> RGB
        face_mat = cv2.cvtColor(face_mat, cv2.COLOR_BGR2RGB)
        face_mat = face_mat.astype(np.float32) / 127.5 - 1.0
        face_mat = np.expand_dims(face_mat, axis=0)
        return face_mat

    def run_model(self, face_mat: np.ndarray) -> np.ndarray:
        """
        Run the model on the image.
        """
        x = self.model.get_inputs()[0].name
        fake_img = self.model.run(None, {x: face_mat})
        output_image = (np.squeeze(fake_img) + 1.0) / 2 * 255
        output_image = np.clip(output_image, 0, 255).astype(np.uint8)
        return output_image

    def run(self, image: np.ndarray) -> np.ndarray:
        """
        Run the model on the image.
        """
        # BGR -> RGB
        data = self.preprocess_image(image[:, :, ::-1])
        if data.size == 0:
            raise ValueError("No face detected")
        res = self.run_model(data)
        return res  # RGB
