import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 人臉偵測 + 表情辨識
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
        emotion = analysis[0]['dominant_emotion']

        # 取出人臉區域座標
        region = analysis[0]['region']  # {'x':..., 'y':..., 'w':..., 'h':...}
        x, y, w, h = region['x'], region['y'], region['w'], region['h']

        # 畫框 + 標籤
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    except Exception as e:
        print("辨識失敗:", e)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()