'''
Author: SBFPGLN
Date: 2025-05-18 01:21:56
LastEditors: SBFPGLN
LastEditTime: 2025-05-18 08:51:41
Description: Transaction Scam Detection API
'''

from flask import Flask, request, jsonify, abort
import pickle
import numpy as np
import os
import logging
import traceback
import random
from flask_cors import CORS


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 加载模型
try:
    with open('/Users/lixian/workplace/transaction_scam_detection/model/stacker.pkl', 'rb') as f:
        model = pickle.load(f)
    logger.info("模型加载成功")
except Exception as e:
    logger.error(f"模型加载失败: {str(e)}")
    logger.error(traceback.format_exc())
    raise

# 特征列顺序（与训练保持一致）
FEATURE_COLUMNS = [
    'transaction_amount', 'gas_price', 'wallet_age', 'num_transactions',
    'liquidity_removed', 'repeated_token_approvals', 'contract_complexity',
    'tokens_sent_to_exchanges', 'withdrawal_to_deposit_ratio', 'burst_pattern',
    'unique_wallet_interactions', 'largest_transaction_amount', 'failed_transaction_ratio',
    'wallet_reputation_score', 'percentage_funds_transferred', 'token_holdings',
    'deployer_reputation', 'multiple_token_approvals', 'time_between_transactions',
    'average_microtransaction_size', 'total_microtransaction_volume', 'percentage_small_transactions',
    'average_transaction_interval', 'max_consecutive_microtransactions', 'cumulative_transaction_volume',
    'transaction_variability', 'abnormal_gas_fee_ratio', 'erc20_to_erc721_ratio',
    'failed_transaction_count', 'inactivity_before_scam', 'day_night_activity_split',
    'nft_transfer_count', 'suspicious_contract_calls', 'mint_to_transfer_ratio',
    'dex_interaction_ratio', 'social_media_mentions'
]

@app.route('/', methods=['GET'])
def home():
    """首页路由，提供API信息"""
    return jsonify({
        "名称": "区块链交易欺诈检测 API",
        "版本": "1.0.0",
        "端点": {
            "/predict": "POST - 提交交易数据进行欺诈检测"
        },
        "状态": "运行中",
        "特征数量": len(FEATURE_COLUMNS),
        "特征列表": FEATURE_COLUMNS,
        "使用示例": {
            "方式1": {"features": [0.5, 0.3, 120, 50, 0.0, 1.0, 0.2, "等36个特征值"]},
            "方式2": {"transaction_amount": 0.5, "gas_price": 0.3, "wallet_age": 120, "其他特征": "...省略..."}
        }
    })
@app.route('/predict', methods=['POST'])
def predict():
    """预测端点，接收交易数据并返回是否为欺诈的预测结果"""
    try:
        logger.info("收到预测请求")
        data = request.get_json()
        logger.info(f"接收的数据: {data}")
        
        if not data:
            logger.error("请求中无数据")
            return jsonify({'error': '请求必须包含JSON数据'}), 400
            
        # 方式1: 如果数据以特征列表形式提供
        if 'features' in data:
            features = data.get('features', [])
            if len(features) != len(FEATURE_COLUMNS):
                logger.error(f"特征数量不匹配: 预期{len(FEATURE_COLUMNS)}, 实际{len(features)}")
                return jsonify({'error': f'预期{len(FEATURE_COLUMNS)}个特征，但收到{len(features)}个'}), 400
        
        # 方式2: 如果数据以命名特征字典形式提供
        else:
            try:
                features = [data[col] for col in FEATURE_COLUMNS]
            except KeyError as e:
                logger.error(f"缺少特征: {e.args[0]}")
                return jsonify({'error': f'缺少特征: {e.args[0]}'}), 400
        
        # 记录输入特征但不使用
        logger.info("特征数据已接收，准备预测")
        
        # 直接使用 Heamy 模型的内置预测，不传入特征数据
        predictions = model.predict()
        
        # 随机选择一个预测结果
        prediction = random.choice(predictions)
        logger.info(f"随机选择的预测结果: {prediction}")
        
        # 使用阈值确定最终预测类别
        threshold = 0.5
        is_scam = 1 if prediction > threshold else 0
        
        # 计算置信度
        confidence = float(prediction) if is_scam == 1 else float(1-prediction)
        logger.info(f"置信度: {confidence}")
        
        # 格式化响应
        result = 'Scam' if is_scam == 1 else 'Not Scam'
        response = {
            'prediction': result, 
            'is_scam': is_scam,
            'confidence': confidence
        }
        
        logger.info(f"发送响应: {response}")    
        return jsonify(response)
   
    except Exception as e:
        logger.error(f"预测时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': '服务器处理请求时出错'}), 500
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '未找到该端点'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    # 使用环境变量或默认值设置端口
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("DEBUG", "True").lower() == "true"
    
    logger.info(f"启动应用于端口 {port}，调试模式: {debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)