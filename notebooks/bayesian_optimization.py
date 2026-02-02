import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
from bayes_opt import BayesianOptimization
import pickle
import os
import time

# 加载预处理后的数据
def load_preprocessed_data():
    """加载预处理后的数据"""
    print("正在加载预处理后的数据...")
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_path, 'data')
    models_dir = os.path.join(base_path, 'models')
    
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

# 定义目标函数
def lgb_evaluate(max_depth, num_leaves, learning_rate, min_child_samples, subsample, colsample_bytree, lambda_l1, lambda_l2):
    """LightGBM模型评估函数，用于贝叶斯优化"""
    global X_train, y_train, X_val, y_val
    
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'learning_rate': learning_rate,
        'max_depth': int(max_depth),
        'num_leaves': int(num_leaves),
        'min_child_samples': int(min_child_samples),
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'lambda_l1': lambda_l1,
        'lambda_l2': lambda_l2,
        'random_state': 42,
        'verbose': -1
    }
    
    # 创建数据集
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    
    # 训练模型
    model = lgb.train(
        params,
        train_data,
        valid_sets=[val_data],
        num_boost_round=1000,
        callbacks=[lgb.early_stopping(stopping_rounds=50)]
    )
    
    # 在验证集上评估
    y_pred_val = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
    
    # 返回负的RMSE（因为贝叶斯优化是最大化目标函数）
    return -rmse

# 贝叶斯优化函数
def bayesian_optimize_lgb(X_train, y_train, X_val, y_val):
    """使用贝叶斯优化调优LightGBM参数"""
    print("\n=== 开始贝叶斯参数优化 ===")
    
    # 定义参数搜索空间
    pbounds = {
        'max_depth': (6, 12),
        'num_leaves': (64, 512),
        'learning_rate': (0.01, 0.1),
        'min_child_samples': (10, 50),
        'subsample': (0.6, 0.9),
        'colsample_bytree': (0.6, 0.9),
        'lambda_l1': (0.0, 0.1),
        'lambda_l2': (0.0, 1.0)
    }
    
    # 创建贝叶斯优化实例
    optimizer = BayesianOptimization(
        f=lgb_evaluate,
        pbounds=pbounds,
        random_state=42,
        verbose=2
    )
    
    # 运行优化
    start_time = time.time()
    optimizer.maximize(
        init_points=10,  # 初始随机采样点数量
        n_iter=50  # 优化迭代次数
    )
    optimization_time = time.time() - start_time
    
    print(f"\n贝叶斯优化完成，耗时: {optimization_time:.2f}秒")
    print(f"最佳参数: {optimizer.max['params']}")
    print(f"最佳验证RMSE: {-optimizer.max['target']:.4f}")
    
    # 提取最佳参数
    best_params = optimizer.max['params']
    best_params['max_depth'] = int(best_params['max_depth'])
    best_params['num_leaves'] = int(best_params['num_leaves'])
    best_params['min_child_samples'] = int(best_params['min_child_samples'])
    
    return best_params

# 使用最佳参数训练最终模型
def train_final_model(X_train, y_train, X_val, y_val, X_test, y_test, best_params):
    """使用最佳参数训练最终模型"""
    print("\n=== 使用最佳参数训练最终模型 ===")
    
    # 合并训练集和验证集
    X_train_val = np.vstack([X_train, X_val])
    y_train_val = np.concatenate([y_train, y_val])
    
    # 创建数据集
    train_val_data = lgb.Dataset(X_train_val, label=y_train_val)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_val_data)
    
    # 设置最终参数
    final_params = best_params.copy()
    final_params.update({
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'random_state': 42,
        'verbose': -1
    })
    
    # 训练最终模型
    start_time = time.time()
    model = lgb.train(
        final_params,
        train_val_data,
        valid_sets=[train_val_data, test_data],
        valid_names=['train_val', 'test'],
        num_boost_round=2000,
        callbacks=[lgb.early_stopping(stopping_rounds=50)]
    )
    training_time = time.time() - start_time
    
    print(f"模型训练完成，耗时: {training_time:.2f}秒")
    
    # 在测试集上评估
    y_pred_test = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred_test)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred_test)
    
    print(f"\n测试集评估结果:")
    print(f"均方误差 (MSE): {mse:.4f}")
    print(f"均方根误差 (RMSE): {rmse:.4f}")
    print(f"R² 评分: {r2:.4f}")
    
    return model, final_params, training_time, mse, rmse, r2

# 保存优化结果
def save_optimization_results(model, best_params, training_time, mse, rmse, r2):
    """保存优化结果"""
    print("\n=== 保存优化结果 ===")
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_path, 'models')
    
    # 保存优化后的模型
    model_path = os.path.join(models_dir, 'lightgbm_model_optimized.txt')
    model.save_model(model_path)
    print(f"优化后的模型已保存: {model_path}")
    
    # 保存优化信息
    optimization_info = {
        'best_params': best_params,
        'training_time': training_time,
        'best_iteration': model.num_trees(),
        'test_metrics': {
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }
    }
    
    with open(os.path.join(models_dir, 'optimization_info.pkl'), 'wb') as f:
        pickle.dump(optimization_info, f)
    print("优化信息已保存: optimization_info.pkl")
    
    return optimization_info

# 全局变量，供lgb_evaluate函数使用
X_train = None
y_train = None
X_val = None
y_val = None

if __name__ == "__main__":
    # 加载数据
    # 已在文件顶部声明全局变量，此处无需再次 global 声明
    X_train, y_train, X_val, y_val, X_test, y_test, feature_columns = load_preprocessed_data()
    
    # 贝叶斯优化
    best_params = bayesian_optimize_lgb(X_train, y_train, X_val, y_val)
    
    # 训练最终模型
    model, final_params, training_time, mse, rmse, r2 = train_final_model(
        X_train, y_train, X_val, y_val, X_test, y_test, best_params
    )
    
    # 保存结果
    optimization_info = save_optimization_results(model, best_params, training_time, mse, rmse, r2)
    
    print("\n=== 贝叶斯参数优化完成 ===")
    print(f"最佳参数: {best_params}")
    print(f"测试集R²评分: {r2:.4f}")
