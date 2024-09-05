import re
import opencc
from paddleocr import PaddleOCR
import logging

def convert_to_traditional(text):
    converter = opencc.OpenCC('s2t')
    return converter.convert(text)

def extract_numbers(text):
    return re.findall(r'\d+', text)

def extract_after_no(text):
    # 使用 rsplit 從右側分割，並只分割一次
    parts = text.rsplit('no.', 1)
    if len(parts) > 1:
        return parts[1].strip()
    return text
def txt_extract(image_path, reader):
    results = reader.ocr(image_path, cls=True)
    extracted_data = []
    for bbox, (text, score) in results[0]:
        extracted_data.append({
            "text": text,
            "coord": bbox,
            "conf": score
        })
    return extracted_data
def preprocess_text(text):
    # 替換 '/' 為空格
    text = text.replace('/', ' ')
    # 將文本中的所有空白字符移除，並轉換為小寫
    processed_text = re.sub(r'\s+', '', text).lower()
    # 將 "p0" 替換為 "po" 來處理 OCR 錯誤
    processed_text = processed_text.replace("p0", "po")
    return processed_text

def match_keywords(keywords, data):
    logging.info(f'matching_keywords')
    matched_keywords = {}
    try:
        for keyword in keywords:
            for item in data:
                try:
                    # 假設 preprocess_text 是用來處理文本的函數
                    processed_keyword = preprocess_text(keyword)
                    processed_text = preprocess_text(item['text'])

                    if processed_keyword in processed_text:
                        # 在返回結果中，替換文本中的 'P0' 為 'PO'
                        matched_keywords[keyword] = {
                            **item,
                            'text': processed_text.replace("p0", "po")  # 這裡對原始文本進行替換
                        }
                        break
                except KeyError:
                    logging.info(f"missing_text:{item}")
                except Exception as e:
                    logging.error(f"Error processing item {item}: {e}")

    except Exception as e:
        logging.critical(f"Error in matching keywords: {e}")

    return matched_keywords

def group_data_by_keywords(matched_keywords, data):
    logging.info(f'grouping_data')
    grouped_data = {}

    for keyword, info in matched_keywords.items():
        if keyword.lower() == 'pono':
            grouped_data[keyword] = [info]
            continue
        if keyword not in grouped_data:
            grouped_data[keyword] = [info]

        keyword_x_min = min(point[0] for point in info['coord'])
        keyword_x_max = max(point[0] for point in info['coord'])
        keyword_y_center = sum(point[1] for point in info['coord']) / 4  # 計算關鍵字框的中心 y 座標

        for item in data:
            if item in grouped_data[keyword]:
                continue  # 跳過已經加入的關鍵字本身
            item_x_min = min(point[0] for point in item['coord'])
            item_x_max = max(point[0] for point in item['coord'])
            item_y_center = sum(point[1] for point in item['coord']) / 4  # 計算文本框的中心 y 座標
            # 檢查是否有 x 軸範圍的重疊並且文本框在關鍵字框下方
            if (keyword_x_min <= item_x_max and item_x_min <= keyword_x_max and item_y_center > keyword_y_center):
                grouped_data[keyword].append(item)
    return grouped_data

def save_grouped_data(grouped_data):
    saved_dict = {}
    for keyword, items in grouped_data.items():
        group_name = convert_to_traditional(keyword)
        processed_items = []
        if keyword.lower() == 'pono':
            # 對於 'pono' 關鍵字，提取 'No.' 後面的部分
            for item in items:
                text = extract_after_no(item['text'])
                # 去掉空值和僅包含空格的字符串
                if text.strip():
                    processed_items.append(text)
            if processed_items:  # 確保只有在 processed_items 不為空時才保存到字典中
                saved_dict[group_name] = processed_items

        else:
            # 處理其他關鍵字
            for item in items[1:]:  # 跳過第一個文本（關鍵字本身）
                text = convert_to_traditional(item['text'])

                if keyword.lower() == 'quantity':
                    # 提取數字
                    text = ''.join(extract_numbers(text))

                elif keyword.lower() == 'expirydate':
                    # 提取數字
                    text = ''.join(extract_numbers(text))

                # 去掉空值和僅包含空格的字符串
                if text.strip():
                    processed_items.append(text)
            if processed_items:  # 確保只有在 processed_items 不為空時才保存到字典中
                saved_dict[group_name] = processed_items
    return saved_dict
def ROI_result(image_path, keywords, match_info):
    try:
        reader = PaddleOCR(use_angle_cls=True, lang='ch')
        try:
            ori_txt = txt_extract(image_path, reader)
            logging.debug(f'original_text:{ori_txt}')

        except Exception as e:
            logging.error(f'Error extracting text: {e}', exc_info=True)
            return {'error': f'Error extracting text: {str(e)}'}

        if match_info:
            try:
                matched = match_keywords(keywords, ori_txt)
                group = group_data_by_keywords(matched, ori_txt)
                ui_result = save_grouped_data(group)

                logging.debug(f'matched_keywords:{matched}')
                logging.debug(f'grouped_matched_keywords:{group}')
                logging.debug(f'cleaned_unnecessary_words:{ui_result}')
                return ui_result
            except KeyError as e:
                logging.error(f'Key error during keyword matching: {e}', exc_info=True)
                return {'error': f'Key error during keyword matching: {str(e)}'}
            except ValueError as e:
                logging.error(f'Value error during keyword matching: {e}', exc_info=True)
                return {'error': f'Value error during keyword matching: {str(e)}'}
            except Exception as e:
                logging.error(f'General error during keyword matching: {e}', exc_info=True)
                return {'error': f'Error during keyword matching: {str(e)}'}

    except FileNotFoundError as e:
        logging.error(f'File not found: {e}', exc_info=True)
        return {'error': f'File not found: {str(e)}'}
    except IOError as e:
        logging.error(f'I/O error: {e}', exc_info=True)
        return {'error': f'I/O error: {str(e)}'}
    except Exception as e:
        logging.error(f'Unexpected error: {e}', exc_info=True)
        return {'error': f'Unexpected error: {str(e)}'}

