import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle

print("开始特征工程与数据预处理...")

# 加载数据
print("加载数据...")
chunks = pd.read_csv('./csv_data/train.csv', chunksize=100000)
df_list = []
for chunk in chunks:
    df_list.append(chunk)
df = pd.concat(df_list, axis=0)
print(f"数据加载完成，共{len(df)}行")

# 特征工程
print("\n特征工程...")

# 1. 移除ID列（不参与建模）
X = df.drop(['id', 'FloodProbability'], axis=1)
y = df['FloodProbability']

print(f"特征维度：{X.shape}")
print(f"目标变量维度：{y.shape}")

# 2. 查看特征列
print("\n特征列：")
print(X.columns.tolist())

# 3. 数据划分
print("\n数据划分...")
# 先划分为训练集和测试集（90%训练，10%测试）
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42
)

# 再将训练集划分为训练集和验证集（80%训练，10%验证）
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.1111, random_state=42  # 0.1111 * 0.9 = 0.1
)

print(f"训练集大小：{len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
print(f"验证集大小：{len(X_val)} ({len(X_val)/len(df)*100:.1f}%)")
print(f"测试集大小：{len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")

# 4. 保存预处理后的数据
print("\n保存预处理后的数据...")

# 保存特征列
with open('models/feature_columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)
print("已保存特征列")

# 保存数据划分结果
np.save('data/X_train.npy', X_train.values)
np.save('data/y_train.npy', y_train.values)
np.save('data/X_val.npy', X_val.values)
np.save('data/y_val.npy', y_val.values)
np.save('data/X_test.npy', X_test.values)
np.save('data/y_test.npy', y_test.values)
print("已保存数据划分结果")

print("\n特征工程与数据预处理完成！")
