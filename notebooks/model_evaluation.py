import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载预处理后的数据
def load_preprocessed_data():
    """加载预处理后的数据"""
    print("正在加载预处理后的数据...")
    
    X_train = np.load('./data/X_train.npy')
    y_train = np.load('./data/y_train.npy')
    X_val = np.load('./data/X_val.npy')
    y_val = np.load('./data/y_val.npy')
    X_test = np.load('./data/X_test.npy')
    y_test = np.load('./data/y_test.npy')
    
    # 加载特征列
    with open('./models/feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    
    return X_train, y_train, X_val, y_val, X_test, y_test, feature_columns

# 加载训练好的模型
def load_trained_model():
    """加载训练好的模型"""
    print("正在加载训练好的模型...")
    model_path = './models/lightgbm_model.txt'
    model = lgb.Booster(model_file=model_path)
    print(f"模型加载完成: {model_path}")
    return model

# 详细评估模型
def detailed_evaluation(model, X_train, y_train, X_val, y_val, X_test, y_test):
    """详细评估模型性能"""
    print("\n=== 详细模型评估 ===")
    
    # 在各个数据集上的预测
    y_pred_train = model.predict(X_train)
    y_pred_val = model.predict(X_val)
    y_pred_test = model.predict(X_test)
    
    # 计算评估指标
    metrics = {}
    
    # 训练集
    metrics['train'] = {
        'mse': mean_squared_error(y_train, y_pred_train),
        'rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
        'r2': r2_score(y_train, y_pred_train)
    }
    
    # 验证集
    metrics['val'] = {
        'mse': mean_squared_error(y_val, y_pred_val),
        'rmse': np.sqrt(mean_squared_error(y_val, y_pred_val)),
        'r2': r2_score(y_val, y_pred_val)
    }
    
    # 测试集
    metrics['test'] = {
        'mse': mean_squared_error(y_test, y_pred_test),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
        'r2': r2_score(y_test, y_pred_test)
    }
    
    # 打印评估结果
    for dataset, scores in metrics.items():
        print(f"\n{dataset} 集评估结果:")
        print(f"  均方误差 (MSE): {scores['mse']:.4f}")
        print(f"  均方根误差 (RMSE): {scores['rmse']:.4f}")
        print(f"  R² 评分: {scores['r2']:.4f}")
    
    return metrics

# 特征重要性可视化
def visualize_feature_importance(model, feature_columns):
    """可视化特征重要性"""
    print("\n=== 特征重要性可视化 ===")
    
    # 获取特征重要性
    importance = model.feature_importance(importance_type='split')
    feature_importance = list(zip(feature_columns, importance))
    
    # 按重要性排序
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    # 提取排序后的特征和重要性值
    sorted_features = [f[0] for f in feature_importance]
    sorted_importance = [f[1] for f in feature_importance]
    
    # 绘制特征重要性条形图
    plt.figure(figsize=(12, 8))
    sns.barplot(x=sorted_importance, y=sorted_features, palette='viridis')
    plt.title('特征重要性排序')
    plt.xlabel('重要性得分')
    plt.ylabel('特征名称')
    plt.tight_layout()
    plt.savefig('./evaluation_data/feature_importance.png', dpi=150)
    plt.close()
    print("特征重要性图已保存: feature_importance.png")
    
    # 打印前10个最重要的特征
    print("\n前10个最重要的特征:")
    for i, (feature, imp) in enumerate(feature_importance[:10]):
        print(f"{i+1}. {feature}: {imp:.2f}")
    
    return feature_importance

# 预测结果分析
def analyze_predictions(model, X_test, y_test):
    """分析预测结果"""
    print("\n=== 预测结果分析 ===")
    
    # 预测
    y_pred = model.predict(X_test)
    
    # 计算预测误差
    errors = y_test - y_pred
    
    # 分析误差分布
    print(f"预测误差均值: {errors.mean():.4f}")
    print(f"预测误差标准差: {errors.std():.4f}")
    print(f"预测误差最小值: {errors.min():.4f}")
    print(f"预测误差最大值: {errors.max():.4f}")
    
    # 绘制预测值与真实值的散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, s=10)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title('预测值 vs 真实值')
    plt.xlabel('真实值 (FloodProbability)')
    plt.ylabel('预测值 (FloodProbability)')
    plt.grid(True, alpha=0.3)
    plt.savefig('./evaluation_data/predictions_vs_actual.png', dpi=150)
    plt.close()
    print("预测值与真实值散点图已保存: predictions_vs_actual.png")
    
    # 绘制误差分布直方图
    plt.figure(figsize=(10, 6))
    sns.histplot(errors, bins=50, kde=True)
    plt.title('预测误差分布')
    plt.xlabel('误差 (真实值 - 预测值)')
    plt.ylabel('频率')
    plt.grid(True, alpha=0.3)
    plt.savefig('./evaluation_data/error_distribution.png', dpi=150)
    plt.close()
    print("预测误差分布图已保存: error_distribution.png")

if __name__ == "__main__":
    # 加载预处理后的数据
    X_train, y_train, X_val, y_val, X_test, y_test, feature_columns = load_preprocessed_data()
    
    # 加载训练好的模型
    model = load_trained_model()
    
    # 详细评估模型
    metrics = detailed_evaluation(model, X_train, y_train, X_val, y_val, X_test, y_test)
    
    # 特征重要性可视化
    feature_importance = visualize_feature_importance(model, feature_columns)
    
    # 预测结果分析
    analyze_predictions(model, X_test, y_test)
    
    print("\n=== 模型评估与分析完成 ===")