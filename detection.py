import cv2
import logging
from logger_config import logger
from ultralytics import YOLO
from ultralytics.solutions import speed_estimation

class ObjectDetection():
    def __init__(self):
        self.model = YOLO("bestmodel.pt")
        self.trackingModel = YOLO("bestmodel.pt")
        self.tracks = None
        self.selectedID = None
        self.tracker = cv2.legacy.TrackerCSRT_create()
        self.bbox = None
        self.trackerCSRT_initialized = False
        names = self.model.model.names
        self.show_frames = True
        self.show_colors = True
        self.line_pts = [(0, 240), (1280, 240)]

        # Init speed-estimation obj
        self.speed_obj = speed_estimation.SpeedEstimator()
        self.speed_obj.set_args(reg_pts=self.line_pts,
                        names=names,
                        view_img=False)
        
        self.logger = logger

    def initTrackerCSRT(self, frame):
        if self.bbox == None:
            return
        x1, y1, x2, y2 = self.bbox
        initial_bbox = (float(x1), float(y1), float(x2 - x1), float(y2 - y1))  # Конвертація в формат (x, y, w, h)
        print(initial_bbox)
        self.tracker = cv2.legacy.TrackerCSRT_create()
        self.trackerCSRT_initialized = self.tracker.init(frame, initial_bbox)



    def trackCSRT(self, frame):
        if not self.trackerCSRT_initialized:
            return
        success, bbox = self.tracker.update(frame)
        if success:
            x, y, w, h = map(int, bbox)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    def setLinePts(self, index):
        names = self.model.model.names
        if index == 0:
            self.line_pts = [(0, 240), (1280, 240)]
        elif index == 1:
            self.line_pts = [(0, 70), (1280, 70)]
        elif index == 2:
            self.line_pts = [(0, 350), (1280, 350)]

        self.speed_obj.set_args(reg_pts=self.line_pts,
                        names=names,
                        view_img=False)

    def classNames(self):
        return self.model.model.names

    def convertToBlackAndWhite(self, frame):
            # Конвертуємо кольоровий кадр у чорно-білий
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB) 

    def detect(self, frame, showSpeed, shouldTrack):
        processed_frame = frame

        if showSpeed:
            tracks = self.trackingModel.track(processed_frame, persist=True, show=False)
            speed_frame = self.speed_obj.estimate_speed(processed_frame, tracks)
            if speed_frame is not None:
                processed_frame = speed_frame
        
        # Перевірте стан чекбокса для чорно-білого відображення
        if not self.show_colors:
            processed_frame = self.convertToBlackAndWhite(processed_frame)
 
        # Detect objects on the frame using YOLOv8n
        results = self.model(processed_frame)
        detected_objects = []
            
        for i in range(len(results[0])):
            boxes = results[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]
            # Get class name
            class_name = self.model.names[clsID]

            detected_objects.append({
                'class_name': class_name,
                'confidence': conf,
                'bounding_box': bb,
                'image': frame[int(bb[1]):int(bb[3]), int(bb[0]):int(bb[2])]
            })
        
        processed_frame = results[0].plot(conf=False, boxes=self.show_frames)

        return detected_objects, processed_frame


    def track(self, frame):
        self.tracks = self.trackingModel.track(frame, persist=True, show=False)
        for track in self.tracks:
            for box in track.boxes:
                if box.is_track and box.id.item() == self.selectedID:
                    x1, y1, x2, y2 = box.xyxy[0]
                    self.bbox = box.xyxy[0]

                    # Малюємо рамку навколо обраного об'єкта
                    cv2.rectangle(frame, (int(x1.item()), int(y1.item())), (int(x2.item()), int(y2.item())), (0, 0, 255), 2)
                    
                    # Обчислення центру рамки
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)

                    # Малювання перпендикулярних ліній в центрі рамки
                    line_length = 20  # Довжина ліній
                    color = (0, 0, 255)  # Колір ліній
                    thickness = 2  # Товщина ліній

                    # Горизонтальна лінія
                    cv2.line(frame, (center_x - line_length, center_y), (center_x + line_length, center_y), color, thickness)
                    
                    # Вертикальна лінія
                    cv2.line(frame, (center_x, center_y - line_length), (center_x, center_y + line_length), color, thickness)

                    # Додавання напису над рамкою
                    text = f"ID: {self.selectedID}"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1

                    # Розмір тексту та координати
                    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
                    text_x = int(x1.item())
                    text_y = int(y1.item()) - 10  # Текст над рамкою

                    # Білий фон для тексту
                    cv2.rectangle(frame, (text_x, text_y - text_height - baseline), (text_x + text_width, text_y), (255, 255, 255), cv2.FILLED)

                    # Чорний текст
                    cv2.putText(frame, text, (text_x, text_y - baseline), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)

                    self.logger.info(f"Tracking {self.model.names[box.cls.item()]} ID {self.selectedID}")

    def getSelectedTrackedId(self):
        return self.selectedID
    
    def removeSelectedId(self):
        self.selectedID = None

    def getTracks(self):
        return self.tracks

    def getElementID(self, x, y):
        print(self.tracks)
        print((x,y))
        if (not self.tracks):
            return
        for track in self.tracks:
            for box in track.boxes:
                if box.is_track:
                    # Отримання меж об'єкта (наприклад, у форматі [x1, y1, x2, y2])
                    bbox = box.xyxy[0]
                    #print(track.boxes[0].id)
                    track_id = box.id.item()

                    x1, y1, x2, y2 = bbox
                    print(f"COORDS: {(x1.item(), y1.item(), x2.item(), y2.item())}")

                    # Перевірка, чи знаходяться координати всередині меж об'єкта
                    if x1.item() <= x <= x2.item() and y1.item() <= y <= y2.item():
                        self.selectedID = track_id
                        return
        self.selectedID = None 
