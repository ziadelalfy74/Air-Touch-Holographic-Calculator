import cv2
import numpy as np
import time
import math
import winsound
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class Button:
    def __init__(self, pos, text, size=[80, 75]):
        self.pos = pos
        self.size = size
        self.text = text

keys = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['C', '0', '=', '+'],
    ['←', '.', '(', ')']
]

button_list = []
start_x, start_y = 457, 130  

for i in range(len(keys)):
    for j in range(len(keys[i])):
        x_pos = start_x + j * 95
        y_pos = start_y + i * 82
        button_list.append(Button([x_pos, y_pos], keys[i][j]))

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),      # الإبهام
    (0, 5), (5, 6), (6, 7), (7, 8),      # السبابة
    (5, 9), (9, 10), (10, 11), (11, 12),  # الوسطى
    (9, 13), (13, 14), (14, 15), (15, 16),# البنسر
    (13, 17), (17, 18), (18, 19), (19, 20),# الخنصر
    (0, 17)                              # قاعدة الكف
]

def draw_cyber_glove(frame, hand_landmarks, h, w):
    points = []
    for lm in hand_landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        points.append((cx, cy))

    for start_idx, end_idx in HAND_CONNECTIONS:
        p1, p2 = points[start_idx], points[end_idx]
        cv2.line(frame, p1, p2, (255, 200, 0), 3, cv2.LINE_AA)
        cv2.line(frame, p1, p2, (255, 255, 255), 1, cv2.LINE_AA)

    for i, p in enumerate(points):
        if i in [4, 8, 12, 16, 20]:
            cv2.circle(frame, p, 9, (255, 229, 0), 2, cv2.LINE_AA)
            cv2.circle(frame, p, 4, (0, 255, 255), cv2.FILLED)
        else:
            cv2.circle(frame, p, 4, (255, 150, 0), cv2.FILLED)
            cv2.circle(frame, p, 2, (255, 255, 255), cv2.FILLED)

    return points

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1
)
recognizer = vision.GestureRecognizer.create_from_options(options)

expression = ""
click_threshold = 30
is_pinched = False

def play_click_sound():
    try:
        winsound.Beep(1200, 40)
    except:
        pass

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

window_name = "Air-Touch Holographic Calculator"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)
cv2.moveWindow(window_name, 320, 100)
try:
    import win32gui, win32con
    win32gui.SendMessage(win32gui.FindWindow(None, window_name), win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, "icon.ico", win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
except:
    pass

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, c = img.shape

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    recognition_result = recognizer.recognize(mp_image)

    x1, y1 = -1, -1
    distance = 999

    if recognition_result.hand_landmarks:
        for hand_landmarks in recognition_result.hand_landmarks:
            points = draw_cyber_glove(img, hand_landmarks, h, w)
            x1, y1 = points[8]   # قمة السبابة
            tx, ty = points[4]   # قمة الإبهام
            distance = math.hypot(tx - x1, ty - y1)

    screen_x1, screen_y1 = start_x, 50
    screen_x2, screen_y2 = start_x + 365, 120
    
    cv2.rectangle(img, (screen_x1, screen_y1), (screen_x2, screen_y2), (20, 20, 35), cv2.FILLED)
    cv2.rectangle(img, (screen_x1, screen_y1), (screen_x2, screen_y2), (0, 255, 200), 2)
    
    disp_text = expression if expression else "0"
    if len(disp_text) > 11:
        disp_text = "..." + disp_text[-8:]
    cv2.putText(img, disp_text, (screen_x1 + 15, screen_y1 + 45), cv2.FONT_HERSHEY_PLAIN, 2.8, (255, 255, 255), 3)

    hint_text = "HINT: Hover on button & Pinch (Thumb + Index) to Click"
    text_size = cv2.getTextSize(hint_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    hint_x = (1280 - text_size[0]) // 2
    cv2.putText(img, hint_text, (hint_x, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)

    triggered_action = None

    for btn in button_list:
        bx, by = btn.pos
        bw, bh = btn.size
        
        is_hovered = (bx < x1 < bx + bw and by < y1 < by + bh) if x1 != -1 else False
        
        overlay = img.copy()
        if is_hovered:
            cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), (0, 200, 255), cv2.FILLED)
            cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), (255, 255, 255), 2)
        else:
            cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), (40, 40, 60), cv2.FILLED)
            cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), (255, 200, 0), 2)
        
        alpha = 0.65
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        
        text_color = (0, 255, 255) if btn.text in ['=', 'C', '←'] else (255, 255, 255)
        cv2.putText(img, btn.text, (bx + 25, by + 48), cv2.FONT_HERSHEY_PLAIN, 2.5, text_color, 3)

        if is_hovered and distance < click_threshold:
            triggered_action = btn.text
            cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, btn.text, (bx + 25, by + 48), cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 0, 0), 3)

   
    if recognition_result.hand_landmarks:
        tx, ty = points[4]
        if distance < click_threshold:
            cv2.line(img, (x1, y1), (tx, ty), (0, 255, 0), 3)
            
            if not is_pinched:
                is_pinched = True
                if triggered_action:
                    play_click_sound()
                    if triggered_action == 'C':
                        expression = ""
                    elif triggered_action == '←':
                        expression = expression[:-1]
                    elif triggered_action == '=':
                        try:
                            result = eval(expression)
                            if isinstance(result, float):
                                if result.is_integer():
                                    result = int(result)
                                else:
                                    result = round(result, 4)
                            expression = str(result)
                        except Exception:
                            expression = "Error"
                    else:
                        if expression == "Error":
                            expression = ""
                        expression += triggered_action
        else:
            is_pinched = False
            if x1 != -1:
                cv2.line(img, (x1, y1), (tx, ty), (255, 0, 255), 1)

    cv2.imshow(window_name, img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()