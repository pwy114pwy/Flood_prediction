from typing import Any
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import time
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_path, 'data')
models_dir = os.path.join(base_path, 'models')
# 加载预处理后的数据
def load_preprocessed_data():
    """加载预处理后的数据"""
    print("正在加载预处理后的数据...")
    
    X_train = np.load(os.path.join(data_dir, 'X_train.npy'))
    y_train = np.load(os.path.join(data_dir, 'y_train.npy')) 
    X_val = np.load(os.path.join(data_dir, 'X_val.npy'))
    y_val = np.load(os.path.join(data_dir, 'y_val.npy'))
    X_test = np.load(os.path.join(data_dir, 'X_test.npy'))
    y_test = np.load(os.path.join(data_dir, 'y_test.npy'))
    
    # 加载特征列
    with open(os.path.join(models_dir, 'feature_columns.pkl'), 'rb') as f:
        feature_columns = pickle.load(f)
    
    print(f"数据加载完成：")
    print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"X_val: {X_val.shape}, y_val: {y_val.shape}")
    print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")
    
    return X_train, y_train, X_val, y_val, X_test, y_test, feature_columns

# 训练LightGBM模型
def train_lightgbm_model(X_train, y_train, X_val, y_val, feature_columns):
    """训练LightGBM模型"""
    print("\n=== 开始训练LightGBM模型 ===")
    
    # 设置训练参数
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'learning_rate': 0.05,
        'max_depth': 8,
        'num_leaves': 256,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_samples': 20,
        'n_estimators': 1000,
        'random_state': 42,
        'verbose': -1
    }
    
    # 创建数据集
    train_data = lgb.Dataset(X_train, label=y_train, feature_name=feature_columns)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data, feature_name=feature_columns)
    
    # 开始训练
    start_time = time.time()
    
    # 记录训练曲线数据
    training_metrics = []
    
    # 自定义回调函数记录训练指标
    def log_metrics_callback(env):
        if env.evaluation_result_list:
            metrics = {}
            for data_name, metric_name, value, is_best in env.evaluation_result_list:
                metrics[f"{data_name}_{metric_name}"] = value
            training_metrics.append({
                'iteration': env.iteration,
                'metrics': metrics
            })
    
    # 设置早停回调
    callbacks = [
        lgb.early_stopping(stopping_rounds=50),
        lgb.log_evaluation(period=100),
        log_metrics_callback
    ]
    
    model = lgb.train(
        params,
        train_data,
        valid_sets=[train_data, val_data],
        valid_names=['train', 'val'],
        num_boost_round=1000,
        callbacks=callbacks
    )
    
    training_time = time.time() - start_time
    print(f"\n模型训练完成，耗时: {training_time:.2f}秒")
    print(f"记录了 {len(training_metrics)} 轮训练指标")
    
    return model, training_time, training_metrics

# 评估模型
def evaluate_model(model, X_test, y_test):
    """评估模型性能"""
    print("\n=== 模型评估 ===")
    
    # 预测
    y_pred = model.predict(X_test)
    
    # 计算评估指标
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"均方误差 (MSE): {mse:.4f}")
    print(f"均方根误差 (RMSE): {rmse:.4f}")
    print(f"R² 评分: {r2:.4f}")
    
    return mse, rmse, r2

# 特征重要性分析
def analyze_feature_importance(model, feature_columns):
    """分析特征重要性"""
    print("\n=== 特征重要性分析 ===")
    
    # 获取特征重要性
    importance = model.feature_importance(importance_type='split')
    feature_importance = list[tuple](zip(feature_columns, importance))
    
    # 按重要性排序
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    # 打印特征重要性
    print("特征重要性排序:")
    for i, (feature, imp) in enumerate(feature_importance[:10]):
        print(f"{i+1}. {feature}: {imp:.2f}")
    
    return feature_importance

# 保存模型
def save_model(model, feature_importance, training_time, training_metrics):
    """保存训练好的模型"""
    print("\n=== 保存模型 ===")
    
    # 保存模型
    model_path = os.path.join(models_dir, 'lightgbm_model.txt')
    model.save_model(model_path)
    print(f"模型已保存: {model_path}")
    
    # 保存特征重要性
    with open(os.path.join(models_dir, 'feature_importance.pkl'), 'wb') as f:
        pickle.dump(feature_importance, f)
    print("特征重要性已保存: feature_importance.pkl")
    
    # 保存训练信息
    training_info = {
        'training_time': training_time,
        'best_iteration': model.num_trees(),
        'training_metrics': training_metrics
    }
    with open(os.path.join(models_dir, 'training_info.pkl'), 'wb') as f:
        pickle.dump(training_info, f)
    print(f"训练信息已保存: training_info.pkl (耗时: {training_time:.2f}秒)")
    print(f"训练曲线数据已保存: {len(training_metrics)} 轮指标")

if __name__ == "__main__":
    # 加载预处理后的数据
    X_train, y_train, X_val, y_val, X_test, y_test, feature_columns = load_preprocessed_data()
    
    # 训练LightGBM模型
    model, training_time, training_metrics = train_lightgbm_model(X_train, y_train, X_val, y_val, feature_columns)
    
    # 评估模型
    mse, rmse, r2 = evaluate_model(model, X_test, y_test)
    
    # 特征重要性分析
    feature_importance = analyze_feature_importance(model, feature_columns)
    
    # 保存模型
    save_model(model, feature_importance, training_time, training_metrics)
    
    print("\n=== 模型训练与评估完成 ===")