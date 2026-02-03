import numpy as np
import lightgbm as lgb
import catboost as cb
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_path, 'data')
models_dir = os.path.join(base_path, 'models')
evaluation_dir = os.path.join(base_path, 'evaluation_data')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 加载预处理后的数据
def load_preprocessed_data():
    """加载预处理后的数据"""
    print("正在加载预处理后的数据...")
    
    X_test = np.load(os.path.join(data_dir, 'X_test.npy'))
    y_test = np.load(os.path.join(data_dir, 'y_test.npy'))
    
    # 加载特征列
    with open(os.path.join(models_dir, 'feature_columns.pkl'), 'rb') as f:
        feature_columns = pickle.load(f)
    
    print(f"测试集: {X_test.shape}")
    
    return X_test, y_test, feature_columns

# 加载模型
def load_models():
    """加载LightGBM和CatBoost模型"""
    print("\n正在加载模型...")
    
    # 加载LightGBM模型
    lgb_model_path = os.path.join(models_dir, 'lightgbm_model.txt')
    lgb_model = lgb.Booster(model_file=lgb_model_path)
    print(f"LightGBM模型加载成功: {lgb_model_path}")
    
    # 加载CatBoost模型
    cb_model_path = os.path.join(models_dir, 'catboost_model.cbm')
    cb_model = cb.CatBoostRegressor()
    cb_model.load_model(cb_model_path)
    print(f"CatBoost模型加载成功: {cb_model_path}")
    
    return lgb_model, cb_model

# 加载训练信息
def load_training_info():
    """加载两个模型的训练信息"""
    print("\n正在加载训练信息...")
    
    # 加载LightGBM训练信息
    with open(os.path.join(models_dir, 'training_info.pkl'), 'rb') as f:
        lgb_info = pickle.load(f)
    
    # 加载CatBoost训练信息
    with open(os.path.join(models_dir, 'catboost_training_info.pkl'), 'rb') as f:
        cb_info = pickle.load(f)
    
    return lgb_info, cb_info

# 加载特征重要性
def load_feature_importance():
    """加载两个模型的特征重要性"""
    print("\n正在加载特征重要性...")
    
    # 加载LightGBM特征重要性
    with open(os.path.join(models_dir, 'feature_importance.pkl'), 'rb') as f:
        lgb_importance = pickle.load(f)
    
    # 加载CatBoost特征重要性
    with open(os.path.join(models_dir, 'catboost_feature_importance.pkl'), 'rb') as f:
        cb_importance = pickle.load(f)
    
    return lgb_importance, cb_importance

# 模型性能对比
def compare_model_performance(lgb_model, cb_model, X_test, y_test):
    """对比两个模型的性能"""
    print("\n=== 模型性能对比 ===")
    
    # LightGBM预测
    lgb_pred = lgb_model.predict(X_test)
    lgb_mse = mean_squared_error(y_test, lgb_pred)
    lgb_rmse = np.sqrt(lgb_mse)
    lgb_r2 = r2_score(y_test, lgb_pred)
    
    # CatBoost预测
    cb_pred = cb_model.predict(X_test)
    cb_mse = mean_squared_error(y_test, cb_pred)
    cb_rmse = np.sqrt(cb_mse)
    cb_r2 = r2_score(y_test, cb_pred)
    
    print("\nLightGBM 测试集性能:")
    print(f"  MSE: {lgb_mse:.6f}")
    print(f"  RMSE: {lgb_rmse:.6f}")
    print(f"  R²: {lgb_r2:.6f}")
    
    print("\nCatBoost 测试集性能:")
    print(f"  MSE: {cb_mse:.6f}")
    print(f"  RMSE: {cb_rmse:.6f}")
    print(f"  R²: {cb_r2:.6f}")
    
    # 计算性能差异
    print("\n性能差异:")
    print(f"  RMSE差异: {abs(lgb_rmse - cb_rmse):.6f} ({'CatBoost更优' if cb_rmse < lgb_rmse else 'LightGBM更优'})")
    print(f"  R²差异: {abs(lgb_r2 - cb_r2):.6f} ({'CatBoost更优' if cb_r2 > lgb_r2 else 'LightGBM更优'})")
    
    return {
        'lightgbm': {'mse': lgb_mse, 'rmse': lgb_rmse, 'r2': lgb_r2, 'predictions': lgb_pred},
        'catboost': {'mse': cb_mse, 'rmse': cb_rmse, 'r2': cb_r2, 'predictions': cb_pred}
    }

# 特征重要性对比
def compare_feature_importance(lgb_importance, cb_importance, feature_columns):
    """对比两个模型的特征重要性"""
    print("\n=== 特征重要性对比 ===")
    
    # 转换为字典格式
    lgb_imp_dict = dict(lgb_importance)
    cb_imp_dict = dict(cb_importance)
    
    # 归一化特征重要性
    lgb_total = sum(lgb_imp_dict.values())
    cb_total = sum(cb_imp_dict.values())
    
    lgb_imp_norm = {k: v/lgb_total for k, v in lgb_imp_dict.items()}
    cb_imp_norm = {k: v/cb_total for k, v in cb_imp_dict.items()}
    
    # 打印Top 10特征对比
    print("\nTop 10 特征重要性对比:")
    print(f"{'特征':<35} {'LightGBM':<15} {'CatBoost':<15}")
    print("-" * 65)
    
    all_features = sorted(set(lgb_imp_dict.keys()) | set(cb_imp_dict.keys()), 
                         key=lambda x: max(lgb_imp_norm.get(x, 0), cb_imp_norm.get(x, 0)), 
                         reverse=True)
    
    for feature in all_features[:10]:
        lgb_val = lgb_imp_norm.get(feature, 0) * 100
        cb_val = cb_imp_norm.get(feature, 0) * 100
        print(f"{feature:<35} {lgb_val:>6.2f}%        {cb_val:>6.2f}%")
    
    return lgb_imp_norm, cb_imp_norm

# 生成可视化对比图
def generate_comparison_plots(performance, lgb_imp_norm, cb_imp_norm, y_test):
    """生成对比可视化图表"""
    print("\n=== 生成对比图表 ===")
    
    # 1. 性能指标对比柱状图
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    metrics = ['MSE', 'RMSE', 'R²']
    lgb_values = [performance['lightgbm']['mse'], performance['lightgbm']['rmse'], performance['lightgbm']['r2']]
    cb_values = [performance['catboost']['mse'], performance['catboost']['rmse'], performance['catboost']['r2']]
    
    for i, (metric, lgb_val, cb_val) in enumerate(zip(metrics, lgb_values, cb_values)):
        axes[i].bar(['LightGBM', 'CatBoost'], [lgb_val, cb_val], color=['#3498db', '#e74c3c'])
        axes[i].set_title(f'{metric} 对比')
        axes[i].set_ylabel(metric)
        
        # 在柱子上显示数值
        for j, val in enumerate([lgb_val, cb_val]):
            axes[i].text(j, val, f'{val:.4f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(evaluation_dir, 'model_performance_comparison.png'), dpi=300, bbox_inches='tight')
    print("性能对比图已保存: model_performance_comparison.png")
    plt.close()
    
    # 2. 特征重要性对比（Top 10）
    top_features = sorted(lgb_imp_norm.keys(), 
                         key=lambda x: max(lgb_imp_norm[x], cb_imp_norm.get(x, 0)), 
                         reverse=True)[:10]
    
    lgb_top_values = [lgb_imp_norm[f] * 100 for f in top_features]
    cb_top_values = [cb_imp_norm.get(f, 0) * 100 for f in top_features]
    
    x = np.arange(len(top_features))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(x - width/2, lgb_top_values, width, label='LightGBM', color='#3498db')
    ax.barh(x + width/2, cb_top_values, width, label='CatBoost', color='#e74c3c')
    
    ax.set_ylabel('特征')
    ax.set_xlabel('重要性 (%)')
    ax.set_title('Top 10 特征重要性对比')
    ax.set_yticks(x)
    ax.set_yticklabels(top_features)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(evaluation_dir, 'feature_importance_comparison.png'), dpi=300, bbox_inches='tight')
    print("特征重要性对比图已保存: feature_importance_comparison.png")
    plt.close()
    
    # 3. 预测值对比散点图
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # LightGBM
    axes[0].scatter(y_test, performance['lightgbm']['predictions'], alpha=0.5, s=10)
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[0].set_xlabel('真实值')
    axes[0].set_ylabel('预测值')
    axes[0].set_title(f'LightGBM 预测 vs 真实值 (R²={performance["lightgbm"]["r2"]:.4f})')
    axes[0].grid(True, alpha=0.3)
    
    # CatBoost
    axes[1].scatter(y_test, performance['catboost']['predictions'], alpha=0.5, s=10, color='#e74c3c')
    axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[1].set_xlabel('真实值')
    axes[1].set_ylabel('预测值')
    axes[1].set_title(f'CatBoost 预测 vs 真实值 (R²={performance["catboost"]["r2"]:.4f})')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(evaluation_dir, 'predictions_comparison.png'), dpi=300, bbox_inches='tight')
    print("预测对比图已保存: predictions_comparison.png")
    plt.close()

# 保存对比报告
def save_comparison_report(performance, lgb_info, cb_info, lgb_imp_norm, cb_imp_norm):
    """保存对比报告为JSON"""
    print("\n=== 保存对比报告 ===")
    
    report = {
        'performance': {
            'lightgbm': {
                'mse': float(performance['lightgbm']['mse']),
                'rmse': float(performance['lightgbm']['rmse']),
                'r2': float(performance['lightgbm']['r2'])
            },
            'catboost': {
                'mse': float(performance['catboost']['mse']),
                'rmse': float(performance['catboost']['rmse']),
                'r2': float(performance['catboost']['r2'])
            }
        },
        'training_info': {
            'lightgbm': {
                'training_time': lgb_info['training_time'],
                'best_iteration': lgb_info['best_iteration']
            },
            'catboost': {
                'training_time': cb_info['training_time'],
                'best_iteration': cb_info['best_iteration']
            }
        },
        'feature_importance': {
            'lightgbm': {k: float(v) for k, v in lgb_imp_norm.items()},
            'catboost': {k: float(v) for k, v in cb_imp_norm.items()}
        },
        'winner': 'CatBoost' if performance['catboost']['r2'] > performance['lightgbm']['r2'] else 'LightGBM',
        'r2_improvement': abs(performance['catboost']['r2'] - performance['lightgbm']['r2'])
    }
    
    report_path = os.path.join(evaluation_dir, 'model_comparison_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"对比报告已保存: {report_path}")
    
    # 打印总结
    print("\n" + "="*60)
    print("模型对比总结".center(60))
    print("="*60)
    print(f"\n🏆 综合表现最优: {report['winner']}")
    print(f"\n📊 R² 提升幅度: {report['r2_improvement']:.6f}")
    print(f"\n⏱️  训练时间对比:")
    print(f"   LightGBM: {lgb_info['training_time']:.2f}秒")
    print(f"   CatBoost: {cb_info['training_time']:.2f}秒")
    print("\n" + "="*60)

if __name__ == "__main__":
    # 加载数据
    X_test, y_test, feature_columns = load_preprocessed_data()
    
    # 加载模型
    lgb_model, cb_model = load_models()
    
    # 加载训练信息
    lgb_info, cb_info = load_training_info()
    
    # 加载特征重要性
    lgb_importance, cb_importance = load_feature_importance()
    
    # 性能对比
    performance = compare_model_performance(lgb_model, cb_model, X_test, y_test)
    
    # 特征重要性对比
    lgb_imp_norm, cb_imp_norm = compare_feature_importance(lgb_importance, cb_importance, feature_columns)
    
    # 生成可视化图表
    generate_comparison_plots(performance, lgb_imp_norm, cb_imp_norm, y_test)
    
    # 保存对比报告
    save_comparison_report(performance, lgb_info, cb_info, lgb_imp_norm, cb_imp_norm)
    
    print("\n=== 模型对比分析完成 ===")
