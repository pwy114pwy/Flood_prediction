import numpy as np
import pandas as pd
import lightgbm as lgb
import pickle
import json
import os
from sklearn.metrics import mean_squared_error, r2_score

base_path = 'd:\\Flood_prediction'
data_dir = os.path.join(base_path, 'data')
models_dir = os.path.join(base_path, 'models')
csv_dir = os.path.join(base_path, 'csv_data')
output_dir = os.path.join(base_path, 'api_data')

os.makedirs(output_dir, exist_ok=True)

print("=== 开始生成前端API所需数据 ===\n")

print("1. 加载训练数据...")
train_data = pd.read_csv(os.path.join(csv_dir, 'train.csv'))
print(f"   训练数据加载完成: {len(train_data)} 行\n")

print("2. 加载特征列...")
with open(os.path.join(models_dir, 'feature_columns.pkl'), 'rb') as f:
    feature_columns = pickle.load(f)
print(f"   特征列加载完成: {len(feature_columns)} 个特征\n")

print("3. 加载模型...")
model = lgb.Booster(model_file=os.path.join(models_dir, 'lightgbm_model.txt'))
print("   模型加载完成\n")

print("4. 加载预处理数据...")
X_train = np.load(os.path.join(data_dir, 'X_train.npy'))
y_train = np.load(os.path.join(data_dir, 'y_train.npy'))
X_val = np.load(os.path.join(data_dir, 'X_val.npy'))
y_val = np.load(os.path.join(data_dir, 'y_val.npy'))
X_test = np.load(os.path.join(data_dir, 'X_test.npy'))
y_test = np.load(os.path.join(data_dir, 'y_test.npy'))
print(f"   训练集: {len(X_train)} 行")
print(f"   验证集: {len(X_val)} 行")
print(f"   测试集: {len(X_test)} 行\n")

print("5. 生成数据统计信息...")
stats = {
    "total_records": int(len(train_data)),
    "feature_count": int(len(feature_columns)),
    "target_variable": "FloodProbability",
    "data_type": "结构化表格数据",
    "data_source": "Kaggle 数据集",
    "missing_values": "无",
    "target_stats": {
        "mean": float(train_data['FloodProbability'].mean()),
        "std": float(train_data['FloodProbability'].std()),
        "min": float(train_data['FloodProbability'].min()),
        "max": float(train_data['FloodProbability'].max()),
        "median": float(train_data['FloodProbability'].median())
    },
    "feature_stats": {}
}

for feature in feature_columns:
    stats["feature_stats"][feature] = {
        "mean": float(train_data[feature].mean()),
        "std": float(train_data[feature].std()),
        "min": int(train_data[feature].min()),
        "max": int(train_data[feature].max()),
        "median": float(train_data[feature].median())
    }

with open(os.path.join(output_dir, 'stats.json'), 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)
print("   数据统计信息已保存: stats.json\n")

print("6. 生成模型评估指标...")
y_pred_train = model.predict(X_train)
y_pred_val = model.predict(X_val)
y_pred_test = model.predict(X_test)

evaluation = {
    "test_metrics": {
        "mse": float(mean_squared_error(y_test, y_pred_test)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred_test))),
        "r2": float(r2_score(y_test, y_pred_test))
    },
    "train_metrics": {
        "mse": float(mean_squared_error(y_train, y_pred_train)),
        "rmse": float(np.sqrt(mean_squared_error(y_train, y_pred_train))),
        "r2": float(r2_score(y_train, y_pred_train))
    },
    "val_metrics": {
        "mse": float(mean_squared_error(y_val, y_pred_val)),
        "rmse": float(np.sqrt(mean_squared_error(y_val, y_pred_val))),
        "r2": float(r2_score(y_val, y_pred_val))
    },
    "data_splits": {
        "train_size": int(len(X_train)),
        "val_size": int(len(X_val)),
        "test_size": int(len(X_test))
    }
}

with open(os.path.join(output_dir, 'evaluation.json'), 'w', encoding='utf-8') as f:
    json.dump(evaluation, f, ensure_ascii=False, indent=2)
print("   模型评估指标已保存: evaluation.json\n")

print("7. 生成目标变量分布...")
target_data = train_data['FloodProbability'].values
bins = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
labels = ['0.3-0.35', '0.35-0.4', '0.4-0.45', '0.45-0.5', '0.5-0.55', '0.55-0.6', '0.6-0.65', '0.65-0.7']

distribution = []
for i in range(len(bins) - 1):
    if i == len(bins) - 2:  # Last bin - include upper bound
        count = int(np.sum((target_data >= bins[i]) & (target_data <= bins[i+1])))
    else:
        count = int(np.sum((target_data >= bins[i]) & (target_data < bins[i+1])))
    distribution.append({
        "range": labels[i],
        "count": count,
        "frequency": float(count / len(target_data))
    })

distribution_data = {
    "distribution": distribution,
    "total_count": int(len(target_data))
}

with open(os.path.join(output_dir, 'distribution.json'), 'w', encoding='utf-8') as f:
    json.dump(distribution_data, f, ensure_ascii=False, indent=2)
print("   目标变量分布已保存: distribution.json\n")

print("8. 生成特征相关性矩阵...")
feature_data = train_data[feature_columns]
correlation_matrix = feature_data.corr()

correlation_data = []
for i, feature1 in enumerate(feature_columns):
    for j, feature2 in enumerate(feature_columns):
        correlation_data.append({
            "feature1": feature1,
            "feature2": feature2,
            "correlation": float(correlation_matrix.loc[feature1, feature2])
        })

correlation_json = {
    "features": feature_columns,
    "correlation_matrix": correlation_data
}

with open(os.path.join(output_dir, 'correlation.json'), 'w', encoding='utf-8') as f:
    json.dump(correlation_json, f, ensure_ascii=False, indent=2)
print("   特征相关性矩阵已保存: correlation.json\n")

print("9. 生成预测值与真实值对比数据...")
sample_size = min(100, len(y_test))
np.random.seed(42)
indices = np.random.choice(len(y_test), sample_size, replace=False)

comparison_data = []
for idx in indices:
    comparison_data.append({
        "actual": float(y_test[idx]),
        "predicted": float(y_pred_test[idx])
    })

comparison_json = {
    "comparison_data": comparison_data,
    "sample_size": sample_size
}

with open(os.path.join(output_dir, 'predictions_comparison.json'), 'w', encoding='utf-8') as f:
    json.dump(comparison_json, f, ensure_ascii=False, indent=2)
print("   预测值与真实值对比数据已保存: predictions_comparison.json\n")

print("10. 生成预测误差分布...")
errors = y_test - y_pred_test
bins_count = 20
bin_width = 0.1 / bins_count
histogram = []

for i in range(bins_count):
    start = -0.05 + i * bin_width
    end = -0.05 + (i + 1) * bin_width
    count = int(np.sum((errors >= start) & (errors < end)))
    histogram.append({
        "range": f"{start:.3f}~{end:.3f}",
        "count": count,
        "frequency": float(count / len(errors))
    })

error_distribution_json = {
    "error_distribution": histogram,
    "error_stats": {
        "mean": float(errors.mean()),
        "std": float(errors.std()),
        "min": float(errors.min()),
        "max": float(errors.max())
    }
}

with open(os.path.join(output_dir, 'error_distribution.json'), 'w', encoding='utf-8') as f:
    json.dump(error_distribution_json, f, ensure_ascii=False, indent=2)
print("   预测误差分布已保存: error_distribution.json\n")

print("11. 生成模型信息...")
importance = model.feature_importance(importance_type='split')
feature_importance_dict = {}
for feature, imp in zip(feature_columns, importance):
    feature_importance_dict[feature] = int(imp)

model_info = {
    "model": "LightGBM Regressor",
    "features": feature_columns,
    "feature_importance": feature_importance_dict,
    "message": "Model information retrieved successfully"
}

with open(os.path.join(output_dir, 'model_info.json'), 'w', encoding='utf-8') as f:
    json.dump(model_info, f, ensure_ascii=False, indent=2)
print("   模型信息已保存: model_info.json\n")

print("=== 所有前端API数据生成完成 ===")
print(f"数据保存位置: {output_dir}")
print("\n生成的文件:")
for file in os.listdir(output_dir):
    file_path = os.path.join(output_dir, file)
    file_size = os.path.getsize(file_path) / 1024
    print(f"  - {file} ({file_size:.2f} KB)")
