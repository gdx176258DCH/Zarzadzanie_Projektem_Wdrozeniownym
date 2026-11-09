"""YuNet + SFace + MiniFASNetV2 ONNX; Python 3.10+."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil
import tempfile
import time

import cv2
import numpy as np

BASE = Path(__file__).resolve().parent


@dataclass
class Stability:
    candidate: str | None = None
    count: int = 0
    box: np.ndarray | None = None
    last_time: float = 0.0

    def reset(self):
        self.candidate, self.count, self.box, self.last_time = None, 0, None, 0.0

    def update(self, name, box, now):
        continuous = (self.box is not None and now - self.last_time <= 1.0
                      and iou(self.box, box) >= 0.3)
        self.count = min(3, self.count + 1) if continuous and name == self.candidate else 1
        self.candidate, self.box, self.last_time = name, box.copy(), now
        return self.count >= 3


def iou(a, b):
    x, y = np.maximum(a[:2], b[:2])
    right, bottom = np.minimum(a[:2] + a[2:4], b[:2] + b[2:4])
    intersection = max(0, right - x) * max(0, bottom - y)
    return float(intersection / max(1.0, a[2] * a[3] + b[2] * b[3] - intersection))


def read_image(path):
    # imread on Windows can fail for paths containing Polish characters.
    image = cv2.imdecode(np.frombuffer(path.read_bytes(), np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Nie można odczytać zdjęcia: {path}")
    return image


class AntiSpoof:
    """Contract: yakhyo MiniFASNetV2.onnx, BGR 0..255, logits, real class=1."""

    def __init__(self, path):
        self.net = cv2.dnn.readNetFromONNX(np.frombuffer(path.read_bytes(), np.uint8))
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def predict(self, frame, face):
        # Same contextual crop as the selected model's reference inference.
        height, width = frame.shape[:2]
        x, y, w, h = map(int, face[:4])
        if min(w, h) <= 0:
            raise ValueError('Nieprawidłowy prostokąt twarzy')
        scale = min((height - 1) / h, (width - 1) / w, 2.7)
        cx, cy = x + w / 2, y + h / 2
        x1, y1 = max(0, int(cx - w * scale / 2)), max(0, int(cy - h * scale / 2))
        x2, y2 = min(width - 1, int(cx + w * scale / 2)), min(height - 1, int(cy + h * scale / 2))
        crop = frame[y1:y2 + 1, x1:x2 + 1]
        blob = cv2.resize(crop, (80, 80)).astype(np.float32).transpose(2, 0, 1)[None]
        self.net.setInput(np.ascontiguousarray(blob))
        logits = np.asarray(self.net.forward()).reshape(-1)
        if logits.size != 3 or not np.isfinite(logits).all():
            raise ValueError('Nieprawidłowy wynik modelu FAS')
        probabilities = np.exp(logits - logits.max())
        probabilities /= probabilities.sum()
        return float(probabilities[1]), int(probabilities.argmax())


def detect(detector, image):
    height, width = image.shape[:2]
    scale = min(1.0, 960.0 / max(height, width))
    resized = cv2.resize(image, (round(width * scale), round(height * scale))) if scale < 1 else image
    detector.setInputSize((resized.shape[1], resized.shape[0]))
    _, faces = detector.detect(resized)
    if faces is None:
        return []
    faces[:, :14:2] *= width / resized.shape[1]
    faces[:, 1:14:2] *= height / resized.shape[0]
    return faces


def feature(recognizer, image, face):
    result = recognizer.feature(recognizer.alignCrop(image, face)).reshape(-1).copy()
    norm = np.linalg.norm(result)
    if not np.isfinite(result).all() or norm < 1e-8:
        raise ValueError('Nieprawidłowy embedding SFace')
    return result / norm


def load_gallery(folder, detector, recognizer):
    # gallery/Jan/*.jpg or gallery/Jan.jpg; multiple references per person.
    gallery = {}
    for path in sorted(folder.rglob('*')):
        if path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.bmp'}:
            continue
        image = read_image(path)
        faces = detect(detector, image)
        if len(faces) != 1:
            raise ValueError(f"Zdjęcie musi zawierać dokładnie jedną twarz: {path}")
        name = path.stem if path.parent == folder else path.relative_to(folder).parts[0]
        gallery.setdefault(name, []).append(feature(recognizer, image, faces[0]))
    if not gallery:
        raise ValueError(f"Brak zdjęć referencyjnych w {folder}")
    return gallery


def identify(embedding, gallery, threshold, margin):
    scores = sorted(((max(float(embedding @ ref) for ref in refs), name)
                     for name, refs in gallery.items()), reverse=True)
    score, name = scores[0]
    runner = scores[1][0] if len(scores) > 1 else -1.0
    return (name if score >= threshold and score - runner >= margin else None), score


def run(args):
    models = args.models.resolve()
    paths = [models / name for name in ('face_detection_yunet_2023mar.onnx',
             'face_recognition_sface_2021dec.onnx', 'MiniFASNetV2.onnx')]
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Brak modelu: {path}")
    # Avoid native OpenCV model loaders receiving Unicode paths.
    with tempfile.TemporaryDirectory(prefix='face_models_') as temporary:
        if not temporary.isascii():
            raise ValueError('Ustaw TEMP i TMP na istniejący folder bez polskich znaków, np. C:\\Temp')
        cached = []
        for index, source in enumerate(paths[:2]):
            target = Path(temporary) / f'{index}.onnx'
            shutil.copyfile(source, target)
            cached.append(str(target))
        detector = cv2.FaceDetectorYN.create(cached[0], '', (640, 480), 0.9, 0.3, 5000)
        recognizer = cv2.FaceRecognizerSF.create(cached[1], '')
        fas = AntiSpoof(paths[2])
        gallery = load_gallery(args.gallery.resolve(), detector, recognizer)
        print('Baza:', ', '.join(gallery))
        print('Q / Esc: koniec. R: reset. Brak mrugnięcia nie wpływa na decyzję.')
        cap = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW if args.backend == 'dshow' else cv2.CAP_ANY)
        try:
            if not cap.isOpened():
                raise RuntimeError('Nie można otworzyć kamery; sprawdź --camera i --backend any')
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            state = Stability()
            last_accepted = None
            previous = time.perf_counter()
            fps = 0.0
            while True:
                ok, frame = cap.read()
                if not ok:
                    state.reset()
                    raise RuntimeError('Przerwano odczyt kamery')
                start = time.perf_counter()
                faces = detect(detector, frame)
                status, color = 'BRAK TWARZY', (0, 180, 255)
                if len(faces) != 1:
                    state.reset()
                    if len(faces) > 1:
                        status = 'WIELE TWARZY - RESET'
                else:
                    face = faces[0]
                    x, y, w, h = map(int, face[:4])
                    height, width = frame.shape[:2]
                    if min(w, h) < args.min_face or x < 0 or y < 0 or x+w > width or y+h > height:
                        state.reset()
                        status = 'TWARZ ZA MALA / POZA KADREM'
                    else:
                        live, label = fas.predict(frame, face)
                        name, score = identify(feature(recognizer, frame, face), gallery,
                                               args.identity_threshold, args.margin)
                        if label != 1 or live < args.live_threshold:
                            state.reset()
                            status = f'NIEZWERYFIKOWANA FAS | real={live:.3f}'
                        elif name is None:
                            state.reset()
                            status = f'NIEZNANA / NIEPEWNA | SFace={score:.3f}'
                        else:
                            accepted = state.update(name, face[:4], time.perf_counter())
                            # OpenCV's default font is ASCII; full names are printed in console.
                            display_name = name.encode('ascii', 'replace').decode()
                            status = f'{display_name}: {state.count}/3 | S={score:.3f} real={live:.3f}'
                            if accepted:
                                status = 'OK ' + status
                                color = (0, 220, 0)
                                if state.count == 3 and last_accepted != name:
                                    print(f'Zweryfikowano: {name}; SFace={score:.3f}; real={live:.3f}')
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                last_accepted = state.candidate if state.count >= 3 else None
                elapsed = (time.perf_counter() - start) * 1000
                now = time.perf_counter()
                instantaneous = 1 / max(now - previous, 1e-6)
                fps = instantaneous if not fps else 0.9 * fps + 0.1 * instantaneous
                previous = now
                cv2.putText(frame, status, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                cv2.putText(frame, f'FPS {fps:.1f} | processing {elapsed:.1f} ms', (10, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.imshow('YuNet + SFace + Passive FAS', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('r'):
                    state.reset()
                    last_accepted = None
                if key in (27, ord('q')):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models', type=Path, default=BASE / 'models')
    parser.add_argument('--gallery', type=Path, default=BASE / 'faces')
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--backend', choices=['dshow', 'any'], default='dshow')
    parser.add_argument('--identity-threshold', type=float, default=0.363)
    parser.add_argument('--margin', type=float, default=0.05)
    parser.add_argument('--live-threshold', type=float, default=0.90)
    parser.add_argument('--min-face', type=int, default=100)
    args = parser.parse_args()
    if not 0 <= args.live_threshold <= 1 or not -1 <= args.identity_threshold <= 1 or args.margin < 0 or args.min_face <= 0:
        parser.error('Nieprawidłowe progi')
    run(args)


if __name__ == '__main__':
    main()
