<!--
 * @Author: SBFPGLN
 * @Date: 2025-05-18 01:05:01
 * @LastEditors: SBFPGLN
 * @LastEditTime: 2025-05-18 09:19:52
 * @Description: 
 * 
-->
# transaction_scam_detection
区块链交易欺诈检测系统
项目概述
本系统是一个基于机器学习的区块链交易欺诈检测解决方案，通过分析交易特征识别潜在的欺诈行为。系统包含API服务和直观的前端界面，方便用户提交交易数据并获取风险评估结果。

系统架构
后端: Flask API服务
模型: Heamy堆叠集成模型，结合了随机森林和LightGBM算法
前端: HTML/CSS/JavaScript单页应用
通信: RESTful API
功能特点
基于36项交易特征的欺诈风险评估
直观的用户界面，支持JSON和表单两种输入方式
预设交易样例（正常、可疑和零特征）
结果展示包含置信度可视化
完善的日志记录和错误处理
安装和运行
后端服务
前端页面
直接在浏览器中打开index_fixed.html文件，或通过简单的Web服务器提供：

API接口文档
首页 - GET /
返回API信息和使用说明。

预测 - POST /predict
提交交易数据进行欺诈检测。
请求格式1 - 特征数组:
{
  "features": [0.5, 0.3, 120, 50, 0.0, 1.0, 0.2, ...]
}
请求格式2 - 命名特征:
{
  "transaction_amount": 0.5,
  "gas_price": 0.3,
  "wallet_age": 120,
  ...
}
响应格式:
{
  "prediction": "Scam",
  "is_scam": 1,
  "confidence": 0.87
}
特征说明
系统分析的36个交易特征包括:

transaction_amount - 交易金额
gas_price - Gas价格
wallet_age - 钱包账龄(天)
num_transactions - 交易次数
liquidity_removed - 是否移除流动性
repeated_token_approvals - 重复代币授权
contract_complexity - 合约复杂度
tokens_sent_to_exchanges - 发送到交易所的代币
withdrawal_to_deposit_ratio - 提现存款比率
burst_pattern - 交易爆发模式 ...等更多特征
注意事项
当前系统实现使用随机选择的模型预测结果作为演示，实际生产环境应使用可接收新特征数据进行实时预测的模型。

