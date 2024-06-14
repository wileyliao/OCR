import cv2
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR, draw_ocr


def show_txtbox(image_path, ocr_reader):
    """
    顯示PaddleOCR所標記的文字區域
    :param image_path: 原始圖片的路徑
    :param ocr: PaddleOCR物件
    :return: 顯示帶有文字邊界框的圖片
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = ocr_reader.ocr(image_path, cls=True)
    # 轉換結果為需要的格式
    boxes = [line[0] for line in results[0]]
    '''
    顯示文字與置信度(如果需要)
    txts = [line[1][0] for line in results[0]]
    scores = [line[1][1] for line in results[0]]
    '''
    # 繪製邊界框
    image_with_boxes = draw_ocr(image, boxes) #show all: draw_ocr(image, boxes, txts, scores)
    plt.figure(figsize=(10, 10))
    plt.imshow(image_with_boxes)
    plt.axis('off')
    plt.show()

def txt_extract(image_path, ocr):
    """
    回傳OCR結果 (文字 + 座標)
    :param image_path: 圖片的路徑
    :param ocr: PaddleOCR物件
    :return: 提取的文字和座標信息的字典列表
    """
    results = ocr.ocr(image_path, cls=True)
    extracted_data = []
    for bbox, (text, score) in results[0]:
        extracted_data.append({
            "text": text,
            "coord": bbox,
            "conf": score
        })
    return extracted_data

def main():
    # 初始化讀取器，設置語言為繁體中文
    reader = PaddleOCR(use_angle_cls=True, lang='ch')
    image_path = './product_info/Product_info_008.jpg'
    data = txt_extract(image_path, reader)
    for item in data:
        print(f"Text: {item['text']}, Coordinates: {item['coord']}")

if __name__ == "__main__":
    main()
