import easyocr
import cv2
import pylab as plt


def show_txtbox(image_path, reader):
    """
    顯示EasyOCR所標記的文字區域
    :param image_path: 原始圖片
    :param reader: OCR結果
    :return: 顯示圖片
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = reader.readtext(image_path)
    for (bbox, text, prob) in results:
        # 繪製邊界框
        top_left = tuple(bbox[0])
        bottom_right = tuple(bbox[2])
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    plt.imshow(image)
    plt.axis('off')
    plt.show()


def txt_extract(image_path, reader):
    """
    回傳ocr結果(文字 + 座標)
    :param image_path: 圖片
    :param reader: OCR
    :return:dictionary
    [{'text': 'text_read', 'coor': [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 'conf': between 0~1}]
    example:
        extracted_info = txt_extract(image_path, reader)
        # 打印提取的文本和對應的座標
        for item in extracted_info:
        print(f"Text: {item['text']}, Coordinates: {item['coordinates']}")
    """
    results = reader.readtext(image_path)
    extracted_data = []
    for (bbox, text, prob) in results:
        extracted_data.append({
            "text": text,
            "coord": bbox,
            "conf": prob
        })
    return extracted_data


def main():
    # 初始化讀取器，設置語言為繁體中文
    reader = easyocr.Reader(['en'])
    image_path = 'output_image.png'
    data = txt_extract(image_path, reader)
    for item in data:
        print(f"Text: {item['text']}, Coordinates: {item['coord']}, Conf: {item['conf']}")

    show_txtbox(image_path, reader)


if __name__ == "__main__":
    main()
