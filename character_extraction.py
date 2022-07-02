import cv2
import win32gui
import win32ui
from ctypes import windll
from PIL import Image

import text_prediction as tp


class WindowImage:

    def __init__(self, current_window='None'):
        self.current_window = current_window

    def clicker(self):
        window_handler = win32gui.FindWindow(None, self.current_window)

        left, top, right, bottom = win32gui.GetClientRect(window_handler)

        width = right - left
        height = bottom - top

        window_handler_dc = win32gui.GetWindowDC(window_handler)
        final_dc = win32ui.CreateDCFromHandle(window_handler_dc)
        saved_dc = final_dc.CreateCompatibleDC()

        saved_bitmap = win32ui.CreateBitmap()
        saved_bitmap.CreateCompatibleBitmap(final_dc, width, height)
        saved_dc.SelectObject(saved_bitmap)
        result = windll.user32.PrintWindow(window_handler, saved_dc.GetSafeHdc(), 3)

        bitmap_info = saved_bitmap.GetInfo()
        bitmap_string = saved_bitmap.GetBitmapBits(True)

        im = Image.frombuffer('RGB', (bitmap_info['bmWidth'], bitmap_info['bmHeight']), bitmap_string, 'raw', 'BGRX', 0,
                              1)

        win32gui.DeleteObject(saved_bitmap.GetHandle())
        saved_dc.DeleteDC()
        final_dc.DeleteDC()
        win32gui.ReleaseDC(window_handler, window_handler_dc)

        if result == 1:
            im.save("test.png")

        # detect the characters in the image and crop the required part

        image = cv2.imread('test.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=6)
        contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for c in contours:
            x, y, cropped_width, cropped_height = cv2.boundingRect(c)
            region_of_interest = image[y:y + cropped_height, x:x + cropped_width]
            cv2.imwrite('cropped.png', region_of_interest)
            break

        prediction = tp.ImagePrediction()
        prediction.predict()
