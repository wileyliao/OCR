import pytesseract
from pytesseract import Output
from PIL import Image
import cv2
import pylab as plt


def show_txtbox(image_path):
    """
    顯示Tesseract OCR所標記的文字區域
    :param image_path: 原始圖片的路徑
    :return: 顯示帶有文字邊界框的圖片
    """
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用 Tesseract 進行 OCR
    results = pytesseract.image_to_data(image_rgb, output_type=Output.DICT)

    n_boxes = len(results['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (results['left'][i], results['top'][i], results['width'][i], results['height'][i])
        image_rgb = cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 顯示帶有邊界框的圖片
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()


def txt_extract(image_path):
    """
    回傳OCR結果 (文字 + 座標)
    :param image_path: 圖片的路徑
    :return: 提取的文字和座標信息的字典列表
    """
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 使用 Tesseract 進行 OCR
    results = pytesseract.image_to_data(image_rgb, output_type=Output.DICT)

    extracted_data = []
    n_boxes = len(results['level'])
    for i in range(n_boxes):
        text = results['text'][i]
        conf = results['conf'][i]
        if int(conf) > 0:  # 過濾掉空白和低置信度的結果
            (x, y, w, h) = (results['left'][i], results['top'][i], results['width'][i], results['height'][i])
            conf_normalized = int(conf) / 100.0
            extracted_data.append({
                "text": text,
                "coord": (x, y, x + w, y + h),
                "conf": conf_normalized
            })

    return extracted_data


def main():
    # 加載手寫數字圖片
    image_path = "./PO_Vision/product_info/product_info_002.jpg"
    data = txt_extract(image_path)
    for item in data:
        print(f"Text: {item['text']}, Coordinates: {item['coord']}, Confidence: {item['conf']}")


if __name__ == "__main__":
    main()
