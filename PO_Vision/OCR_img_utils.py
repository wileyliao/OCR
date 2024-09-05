import cv2
import base64
import numpy as np
import logging
def base64_decoder(image_64):
    try:
        decode = base64.b64decode(image_64)
        image_array = np.frombuffer(decode, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            # 如果解碼失敗，拋出自定義的例外
            raise ValueError("cv2.imdecode failed to decode the image.")
        else:
            return image
    except Exception as e:
        logging.error(f'Failed to decode base64 string: {e}')
        raise
def process_roi(image, coords):
    if not isinstance(coords, list) or len(coords) != 2:
        logging.error(f'Invalid coordinates: {coords}')
        return None
    try:
        (x1, y1), (x2, y2) = coords
        top_left_x = min(x1, x2)
        top_left_y = min(y1, y2)
        bottom_right_x = max(x1, x2)
        bottom_right_y = max(y1, y2)
        roi_image = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
        return roi_image
    except Exception as e:
        logging.error(f'Error processing ROI: {e}')
        return None