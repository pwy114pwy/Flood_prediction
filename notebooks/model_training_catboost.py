import numpy as np
import catboost as cb
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

# 训练CatBoost模型
def train_catboost_model(X_train, y_train, X_val, y_val, feature_columns):
    """训练CatBoost模型"""
    print("\n=== 开始训练CatBoost模型 ===")
    
    # 设置训练参数
    params = {
        'iterations': 1000,
        'learning_rate': 0.05,
        'depth': 8,
        'l2_leaf_reg': 3,
        'loss_function': 'RMSE',
        'eval_metric': 'RMSE',
        'random_seed': 42,
        'early_stopping_rounds': 50,
        'verbose': 100
    }
    
    # 创建数据集
    train_pool = cb.Pool(X_train, y_train, feature_names=feature_columns)
    val_pool = cb.Pool(X_val, y_val, feature_names=feature_columns)
    
    # 开始训练
    start_time = time.time()
    
    model = cb.CatBoostRegressor(**params)
    model.fit(
        train_pool,
        eval_set=val_pool,
        use_best_model=True,
        plot=False
    )
    
    training_time = time.time() - start_time
    print(f"\n模型训练完成，耗时: {training_time:.2f}秒")
    print(f"最佳迭代轮数: {model.get_best_iteration()}")
    
    return model, training_time

# 评估模型
def evaluate_model(model, X_train, y_train, X_val, y_val, X_test, y_test):
    """评估模型性能"""
    print("\n=== 模型评估 ===")
    
    # 在训练集上评估
    y_train_pred = model.predict(X_train)
    train_mse = mean_squared_error(y_train, y_train_pred)
    train_rmse = np.sqrt(train_mse)
    train_r2 = r2_score(y_train, y_train_pred)
    
    # 在验证集上评估
    y_val_pred = model.predict(X_val)
    val_mse = mean_squared_error(y_val, y_val_pred)
    val_rmse = np.sqrt(val_mse)
    val_r2 = r2_score(y_val, y_val_pred)
    
    # 在测试集上评估
    y_test_pred = model.predict(X_test)
    test_mse = mean_squared_error(y_test, y_test_pred)
    test_rmse = np.sqrt(test_mse)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print("\n训练集评估结果:")
    print(f"  MSE: {train_mse:.6f}")
    print(f"  RMSE: {train_rmse:.6f}")
    print(f"  R²: {train_r2:.6f}")
    
    print("\n验证集评估结果:")
    print(f"  MSE: {val_mse:.6f}")
    print(f"  RMSE: {val_rmse:.6f}")
    print(f"  R²: {val_r2:.6f}")
    
    print("\n测试集评估结果:")
    print(f"  MSE: {test_mse:.6f}")
    print(f"  RMSE: {test_rmse:.6f}")
    print(f"  R²: {test_r2:.6f}")
    
    return {
        'train': {'mse': train_mse, 'rmse': train_rmse, 'r2': train_r2},
        'val': {'mse': val_mse, 'rmse': val_rmse, 'r2': val_r2},
        'test': {'mse': test_mse, 'rmse': test_rmse, 'r2': test_r2}
    }

# 特征重要性分析
def analyze_feature_importance(model, feature_columns):
    """分析特征重要性"""
    print("\n=== 特征重要性分析 ===")
    
    # 获取特征重要性
    importance = model.get_feature_importance()
    feature_importance = list(zip(feature_columns, importance))
    
    # 按重要性排序
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    # 打印特征重要性
    print("特征重要性排序:")
    for i, (feature, imp) in enumerate(feature_importance[:10]):
        print(f"{i+1}. {feature}: {imp:.2f}")
    
    return feature_importance

# 保存模型
def save_model(model, feature_importance, training_time, metrics):
    """保存训练好的模型"""
    print("\n=== 保存模型 ===")
    
    # 保存模型
    model_path = os.path.join(models_dir, 'catboost_model.cbm')
    model.save_model(model_path)
    print(f"模型已保存: {model_path}")
    
    # 保存特征重要性
    with open(os.path.join(models_dir, 'catboost_feature_importance.pkl'), 'wb') as f:
        pickle.dump(feature_importance, f)
    print("特征重要性已保存: catboost_feature_importance.pkl")
    
    # 保存训练信息
    training_info = {
        'training_time': training_time,
        'best_iteration': model.get_best_iteration(),
        'metrics': metrics
    }
    with open(os.path.join(models_dir, 'catboost_training_info.pkl'), 'wb') as f:
        pickle.dump(training_info, f)
    print(f"训练信息已保存: catboost_training_info.pkl (耗时: {training_time:.2f}秒)")

if __name__ == "__main__":
    # 加载预处理后的数据
    X_train, y_train, X_val, y_val, X_test, y_test, feature_columns = load_preprocessed_data()
    
    # 训练CatBoost模型
    model, training_time = train_catboost_model(X_train, y_train, X_val, y_val, feature_columns)
    
    # 评估模型
    metrics = evaluate_model(model, X_train, y_train, X_val, y_val, X_test, y_test)
    
    # 特征重要性分析
    feature_importance = analyze_feature_importance(model, feature_columns)
    
    # 保存模型
    save_model(model, feature_importance, training_time, metrics)
    
    print("\n=== CatBoost模型训练与评估完成 ===")
