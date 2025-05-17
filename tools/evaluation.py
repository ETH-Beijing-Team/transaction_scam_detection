from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def evaluate_model(y_train, y_train_pred, y_train_prob, y_test, y_test_pred, y_test_prob, model_name="Model"):
    """
    评估分类模型在训练集与测试集上的表现，并分别计算AUC。
    
    参数：
        y_train (array-like): 训练集真实标签
        y_train_pred (array-like): 训练集预测标签
        y_train_prob (array-like): 训练集预测正类概率
        y_test (array-like): 测试集真实标签
        y_test_pred (array-like): 测试集预测标签
        y_test_prob (array-like): 测试集预测正类概率
        model_name (str): 模型名称，用于显示
        
    返回：
        metrics (dict): 包含训练集与测试集评估指标的字典
    """
    # 计算训练集指标
    train_accuracy = accuracy_score(y_train, y_train_pred)
    train_precision = precision_score(y_train, y_train_pred)
    train_recall = recall_score(y_train, y_train_pred)
    train_f1 = f1_score(y_train, y_train_pred)
    train_auc = roc_auc_score(y_train, y_train_prob)
    
    # 计算测试集指标
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred)
    test_recall = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)
    test_auc = roc_auc_score(y_test, y_test_prob)
    
    # 输出评估指标
    print(f"Evaluation Metrics for {model_name}:")
    print("训练集：")
    print(f"  Accuracy: {train_accuracy:.4f}")
    print(f"  Precision: {train_precision:.4f}")
    print(f"  Recall: {train_recall:.4f}")
    print(f"  F1-Score: {train_f1:.4f}")
    print(f"  AUC: {train_auc:.4f}")
    
    print("测试集：")
    print(f"  Accuracy: {test_accuracy:.4f}")
    print(f"  Precision: {test_precision:.4f}")
    print(f"  Recall: {test_recall:.4f}")
    print(f"  F1-Score: {test_f1:.4f}")
    print(f"  AUC: {test_auc:.4f}")
    
    # 绘制训练集与测试集的ROC曲线
    train_fpr, train_tpr, _ = roc_curve(y_train, y_train_prob)
    test_fpr, test_tpr, _ = roc_curve(y_test, y_test_prob)
    
    # 设置5号字体 (10.5pt) 和 Times New Roman 字体
    font_size = 30
    
    # 重置rcParams以避免之前的设置干扰
    plt.rcParams.update(plt.rcParamsDefault)
    
    # 配置Times New Roman字体
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = font_size
    plt.rcParams['axes.unicode_minus'] = False  # 确保负号正确显示
    
    plt.figure(figsize=(10, 8))
    
    plt.plot(train_fpr, train_tpr, color='blue', lw=2, label=f'train ROC (AUC = {train_auc:.2f})')
    plt.plot(test_fpr, test_tpr, color='darkorange', lw=2, label=f'test ROC (AUC = {test_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    
    # 明确为每个文本元素设置Times New Roman字体
    plt.xlabel('False Positive Rate', fontsize=font_size, fontfamily='Times New Roman')
    plt.ylabel('True Positive Rate', fontsize=font_size, fontfamily='Times New Roman')
    plt.title(f'ROC Curve for {model_name}', fontsize=font_size, fontfamily='Times New Roman')
    plt.legend(loc="lower right", fontsize=font_size)
    
    # 调整图表边距以确保所有元素都能显示
    plt.tight_layout()
    plt.show()
    
    # 返回包含训练集与测试集指标的字典
    return {
        "train": {
            "accuracy": train_accuracy,
            "precision": train_precision,
            "recall": train_recall,
            "f1_score": train_f1,
            "auc": train_auc
        },
        "test": {
            "accuracy": test_accuracy,
            "precision": test_precision,
            "recall": test_recall,
            "f1_score": test_f1,
            "auc": test_auc
        }
    }