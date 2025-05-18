'''
Author: SBFPGLN
Date: 2025-05-18 06:58:05
LastEditors: SBFPGLN
LastEditTime: 2025-05-18 07:12:13
Description: 

'''
# 保存为 test_api.py
import requests
import json

url = 'http://127.0.0.1:8080/predict'
# data = {"features": [0.5, 0.3, 120, 50, 0, 1, 0.2, 0.1, 0.7, 1, 15, 1000, 0.05, 0.8, 0.3, 500, 0.9, 1, 30, 50, 500, 0.2, 120, 5, 10000, 0.4, 0.1, 0.8, 3, 0, 0.5, 2, 3, 0.7, 0.6, 10]}

# response = requests.post(url, json=data)

# 使用全零特征来测试
minimal_data = {"features": [0.0] * 36}  # 36个零
response = requests.post(url, json=minimal_data)
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")