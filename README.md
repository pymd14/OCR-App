# 练手应用程序，感谢QFluentDesigner和百度飞桨PaddleOCR
主程序为OCR_20241206.py，模型调用ch_PP-OCRv4_det_infer和ch_PP-OCRv4_rec_infer<br>
如果gpu就将device='cpu'改为device='gpu'<br>
实现det坐标筛选，settings可以修改置信度颜色，可自主根据置信度二次核对。<br>
全部核对后可以赛博装订，做了图书借阅模式（但是感觉做的不好）<br>
![](output/result_shl.png)
![](output/result_ynsz.png)<br>

新增test.py，实现竖排古籍显示逻辑，.classic多了竖线，更拟真古文阅读习惯

## 近期发布了PPOCRv5，def show_result可能需要重写一下
