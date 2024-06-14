# OCR
Three kinds of OCR



**PaddleOCR** (https://github.com/PaddlePaddle/PaddleOCR)
return [bbox, (text, score)] : a Multi-Level list with results by following structure:
     results[0] 是一個包含多個字典的列表，每個字典包含文字區域的詳細信息：
          bbox: 表示文字區域的四個頂點的座標。
          (text, score): 這是一個二元組，其中 text 是檢測到的文字，score 是置信度。

*bbox* : coordinate of text bbox
     coordinate structure：[ (x1, y1), (x2, y2), (x3, y3), (x4, y4) ]
   
        (x1, y1)         (x2, y2)
          ┌────────────────┐
          │                │
          │                │
          │                │
          └────────────────┘
       (x4, y4)         (x3, y3)

*text* : recognized text
*score* : confidence of text (between 0, 1)



**EasyOCR** (https://github.com/JaidedAI/EasyOCR)
return [bbox, text, prob] : a list with results by following structure:
     每個元素是由三部分組成的元組：
          bbox: 表示文字區域的四個頂點的座標。
          text: OCR 檢測到的文字。
          prob: 置信度，即系統對該文字檢測結果的信心程度。

*bbox* : coordinate of text bbox
     coordinate structure：[ (x1, y1), (x2, y2), (x3, y3), (x4, y4) ]
   
        (x1, y1)         (x2, y2)
          ┌────────────────┐
          │                │
          │                │
          │                │
          └────────────────┘
       (x4, y4)         (x3, y3)

*text* : recognized text
*prob* : confidence of text (between 0, 1)


TesseractOCR
"https://github.com/tesseract-ocr/tesseract"
