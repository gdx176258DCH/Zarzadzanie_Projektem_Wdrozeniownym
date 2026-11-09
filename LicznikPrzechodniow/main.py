"""Licznik przechodniów: HOG + SVM oraz śledzenie tymczasowych ID."""
from __future__ import annotations
import argparse
import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import time

import cv2
import numpy as np


def overlap(a, b):
    x, y = max(a[0], b[0]), max(a[1], b[1])
    r, bottom = min(a[0]+a[2], b[0]+b[2]), min(a[1]+a[3], b[1]+b[3])
    inter = max(0, r-x)*max(0, bottom-y)
    return inter / max(1, a[2]*a[3]+b[2]*b[3]-inter)


def suppress(boxes, scores, threshold=0.45):
    remaining = sorted(range(len(boxes)), key=lambda i: scores[i], reverse=True)
    selected = []
    while remaining:
        best = remaining.pop(0)
        selected.append(boxes[best])
        remaining = [i for i in remaining if overlap(boxes[best], boxes[i]) < threshold]
    return selected


@dataclass
class Track:
    box: np.ndarray
    seen: float
    streak: int = 1
    counted: bool = False
    velocity: np.ndarray | None = None
    evidence: list = field(default_factory=lambda: [1])


class Tracker:
    def __init__(self, confirmations=3, max_gap=3.0, confirm_window=8):
        self.confirmations = confirmations
        self.max_gap = max_gap
        self.confirm_window = max(confirmations, confirm_window)
        self.tracks = {}
        self.next_id = 1
        self.total = 0

    def reset(self):
        self.tracks.clear()
        self.next_id, self.total = 1, 0

    def update(self, boxes, now):
        self.tracks = {i: t for i, t in self.tracks.items() if now-t.seen <= self.max_gap}
        for track in self.tracks.values():
            track.evidence = (track.evidence + [0])[-self.confirm_window:]
        boxes = [np.asarray(b, dtype=float) for b in boxes]
        pairs = []
        for ident, track in self.tracks.items():
            dt = max(0, now-track.seen)
            predicted = track.box.copy()
            if track.velocity is not None:
                predicted[:2] += track.velocity * min(dt, 0.75)
            for j, box in enumerate(boxes):
                c1 = predicted[:2]+predicted[2:]/2
                c2 = box[:2]+box[2:]/2
                distance = np.linalg.norm(c1-c2)/max(1, predicted[3], box[3])
                ratio = box[3]/max(1, predicted[3])
                if distance <= 0.8 and 0.5 <= ratio <= 2:
                    pairs.append((distance+0.5*(1-overlap(predicted, box)), ident, j))
        used_tracks, used_boxes = set(), set()
        visible = []
        for _, ident, j in sorted(pairs):
            if ident in used_tracks or j in used_boxes:
                continue
            track = self.tracks[ident]
            dt = max(now-track.seen, 0.001)
            velocity = (boxes[j][:2]-track.box[:2])/dt
            track.velocity = velocity if track.velocity is None else 0.5*track.velocity+0.5*velocity
            track.box, track.seen = boxes[j], now
            track.streak += 1
            track.evidence[-1] = 1
            used_tracks.add(ident)
            used_boxes.add(j)
            visible.append(ident)
        for ident, track in self.tracks.items():
            if ident not in used_tracks:
                track.streak = 0
        for j, box in enumerate(boxes):
            if j not in used_boxes:
                ident = self.next_id
                self.next_id += 1
                self.tracks[ident] = Track(box, now)
                visible.append(ident)
        for ident in visible:
            track = self.tracks[ident]
            if not track.counted and sum(track.evidence) >= self.confirmations:
                self.total += 1
                track.counted = True
        return [(ident, self.tracks[ident]) for ident in visible]


class PeopleDetector:
    def __init__(self, threshold=0.0, nms=0.65, pyramid_scale=1.04):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.threshold = threshold
        self.nms = nms
        self.pyramid_scale = pyramid_scale

    def detect(self, frame):
        if frame.shape[0] < 128 or frame.shape[1] < 64:
            return []
        boxes, scores = self.hog.detectMultiScale(
            frame, self.threshold, (8, 8), (8, 8), self.pyramid_scale, 2)
        return suppress(boxes, np.asarray(scores).reshape(-1), self.nms)


def resize(frame, width):
    return cv2.resize(frame, (width, max(1, round(frame.shape[0]*width/frame.shape[1]))))


class YoloDetector:
    def __init__(self, model, confidence=0.35, nms=0.60):
        import hashlib
        data = model.read_bytes()
        if hashlib.sha1(data).hexdigest() != '68f864475d06e2ec4037181052739f268eeac38d':
            raise ValueError('Nieoczekiwana wersja modelu YOLOv8n; sprawdź źródło w README')
        self.net = cv2.dnn.readNetFromONNX(np.frombuffer(data, np.uint8))
        self.confidence, self.nms = confidence, nms

    def detect(self, frame):
        h, w = frame.shape[:2]
        ratio = min(640/w, 640/h)
        rw, rh = round(w*ratio), round(h*ratio)
        left, top = (640-rw)//2, (640-rh)//2
        canvas = np.full((640,640,3),114,np.uint8)
        canvas[top:top+rh,left:left+rw] = cv2.resize(frame,(rw,rh))
        self.net.setInput(cv2.dnn.blobFromImage(canvas,1/255.0,(640,640),swapRB=True))
        output = self.net.forward()
        if output.ndim != 3 or output.shape[1] != 84:
            raise ValueError(f'Nieobsługiwane wyjście YOLO: {output.shape}')
        boxes, scores = [], []
        for row in output[0].T:
            if row[4] < self.confidence or np.argmax(row[4:]) != 0:
                continue
            cx,cy,bw,bh = row[:4]
            x1 = max(0,float((cx-bw/2-left)*w/rw))
            y1 = max(0,float((cy-bh/2-top)*h/rh))
            x2 = min(w,float((cx+bw/2-left)*w/rw))
            y2 = min(h,float((cy+bh/2-top)*h/rh))
            if x2 > x1 and y2 > y1:
                boxes.append([x1,y1,x2-x1,y2-y1])
                scores.append(float(row[4]))
        return suppress(boxes,scores,self.nms)


def run(args):
    source = int(args.source) if args.source.isdecimal() else args.source
    backend = cv2.CAP_DSHOW if isinstance(source, int) and args.backend == 'dshow' else cv2.CAP_ANY
    detector = (YoloDetector(args.model, args.confidence, args.nms) if args.detector == 'yolo'
                else PeopleDetector(args.threshold, args.nms, args.pyramid_scale))
    tracker = Tracker(args.confirmations, args.max_gap, args.confirm_window)
    cap = cv2.VideoCapture(source, backend)
    log = None
    try:
        if not cap.isOpened():
            raise RuntimeError('Nie można otworzyć źródła. Sprawdź --source lub --backend any.')
        if args.csv:
            args.csv.parent.mkdir(parents=True, exist_ok=True)
            log = args.csv.open('w', encoding='utf-8-sig', newline='')
            writer = csv.writer(log)
            writer.writerow(['date', 'frame', 'session', 'source_time_s', 'width', 'height',
                             'detections', 'unique_tracks_total', 'detect_ms', 'tracking_ms', 'processing_ms',
                             'opencv', 'threshold', 'confirmations', 'max_gap_s', 'confirm_window', 'nms', 'pyramid_scale', 'detector', 'confidence'])
        print('Q/Esc: koniec; R: reset licznika. Licznik oznacza potwierdzone ID, nie tożsamości.')
        print('OpenCV:', cv2.__version__)
        number, session, previous, fps = 0, 1, time.perf_counter(), 0.0
        while True:
            ok, raw = cap.read()
            if not ok:
                if isinstance(source, int):
                    raise RuntimeError('Utracono obraz z kamery')
                break
            begin = time.perf_counter()
            frame = resize(raw, args.width)
            start = time.perf_counter()
            boxes = detector.detect(frame)
            after_detection = time.perf_counter()
            # File timestamps keep tracking independent of machine playback speed.
            media_fps = cap.get(cv2.CAP_PROP_FPS)
            timestamp = (number / media_fps if media_fps > 0 else number / 25.0) if isinstance(source, str) else after_detection
            tracks = tracker.update(boxes, timestamp)
            after_tracking = time.perf_counter()
            detect_ms = (after_detection-start)*1000
            tracking_ms = (after_tracking-after_detection)*1000
            processing_ms = (after_tracking-begin)*1000
            now = time.perf_counter()
            rate = 1/max(now-previous, 1e-6)
            fps = rate if not fps else 0.9*fps+0.1*rate
            previous = now
            if log:
                writer.writerow([datetime.now().astimezone().isoformat(), number, session, round(timestamp, 3) if isinstance(source, str) else '',
                                 frame.shape[1], frame.shape[0], len(boxes), tracker.total,
                                 round(detect_ms,3), round(tracking_ms,3), round(processing_ms,3),
                                 cv2.__version__, args.threshold, args.confirmations, args.max_gap, args.confirm_window, args.nms, args.pyramid_scale, args.detector, args.confidence])
            for ident, track in tracks:
                x,y,w,h = map(int, track.box)
                color = (0,220,0) if track.counted else (0,190,255)
                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                cv2.putText(frame,f'ID {ident}',(max(0,x),max(18,y-6)),cv2.FONT_HERSHEY_SIMPLEX,.55,color,2)
            cv2.rectangle(frame,(0,0),(frame.shape[1],85),(25,25,25),-1)
            cv2.putText(frame,f'SUMA PRZECHODNIOW (ID): {tracker.total}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,255,255),2)
            cv2.putText(frame,f'W kadrze: {len(boxes)} | FPS: {fps:.1f}',(10,50),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
            cv2.putText(frame,f'AI: {detect_ms:.1f} ms | R: reset | Q: koniec',(10,73),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
            number += 1
            if not args.no_display:
                cv2.imshow(f'Licznik przechodniow - {args.detector}',frame)
                key = cv2.waitKey(1) & 0xff
                if key in (27,ord('q')):
                    break
                if key == ord('r'):
                    tracker.reset()
                    session += 1
            if args.max_frames and number >= args.max_frames:
                break
        print(f'Suma potwierdzonych przechodniów (ID): {tracker.total}')
    finally:
        cap.release()
        if log:
            log.close()
        cv2.destroyAllWindows()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--detector', choices=['yolo','hog'], default='yolo')
    p.add_argument('--model', type=Path, default=Path(__file__).resolve().parent/'models'/'yolov8n.onnx')
    p.add_argument('--confidence', type=float, default=0.35)
    p.add_argument('--source',default='0',help='Numer kamery lub ścieżka filmu')
    p.add_argument('--width',type=int,default=1280,help='Szerokość przetwarzania; zachowane proporcje')
    p.add_argument('--backend',choices=['dshow','any'],default='dshow')
    p.add_argument('--threshold',type=float,default=0.0,help='Próg SVM, nie prawdopodobieństwo')
    p.add_argument('--confirmations',type=int,default=3)
    p.add_argument('--max-gap',type=float,default=3.0,help='Czas zachowania niewidocznego ID w sekundach')
    p.add_argument('--confirm-window',type=int,default=8,help='Okno klatek do potwierdzenia ID')
    p.add_argument('--nms',type=float,default=0.60,help='Próg IoU usuwania duplikatów; większy zachowuje nakładające się ramki')
    p.add_argument('--pyramid-scale',type=float,default=1.04)
    p.add_argument('--csv',type=Path)
    p.add_argument('--max-frames',type=int,default=0)
    p.add_argument('--no-display',action='store_true')
    a=p.parse_args()
    if a.width < 64 or a.confirmations < 1 or a.max_gap <= 0 or a.max_frames < 0 or a.confirm_window < a.confirmations or not 0 < a.nms < 1 or not 1.01 <= a.pyramid_scale <= 1.5 or not 0 < a.confidence < 1:
        p.error('Nieprawidłowy rozmiar, liczba potwierdzeń lub czas')
    run(a)


if __name__=='__main__':
    main()
