import cv2
import pyautogui
import pygetwindow as gw
import win32gui
import win32con

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
_, frame2 = cap.read()

while True:
    # Hitung perbedaan antar frame
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Deteksi kontur (gerakan)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if motion_detected:
        pyautogui.press('space')
        cv2.putText(frame1, "SPACE PRESSED!", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Tampilkan video
    cv2.imshow("Gerakan Tangan = SPACE", frame1)
    try:
        win = gw.getWindowsWithTitle("Gerakan Tangan = SPACE")[0]
        hwnd = win._hWnd
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    except:
        pass

    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret or cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
