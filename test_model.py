'''
Author: SBFPGLN
Date: 2025-05-18 07:37:09
LastEditors: SBFPGLN
LastEditTime: 2025-05-18 07:57:52
Description: 

'''
# 保存为 test_model.py
import pickle
import numpy as np

# 加载模型
with open('/Users/lixian/workplace/transaction_scam_detection/model/stacker.pkl', 'rb') as f:
    model = pickle.load(f)

# 输出模型信息
print(f"模型类型: {type(model)}")
print(f"模型属性: {dir(model)}")

# 尝试不同调用方式
features = np.zeros(36).reshape(1, -1)

try:
    print("尝试方式1: model.predict(features)")
    result = model.predict(features)
    print(f"结果: {result}")
except Exception as e:
    print(f"错误: {e}")

try:
    print("尝试方式2: model.predict()")
    result = model.predict()[0]
    print(f"结果: {result}")
except Exception as e:
    print(f"错误: {e}")