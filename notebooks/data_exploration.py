import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_dir = os.path.join(base_path, 'csv_data')
analysis_dir = os.path.join(base_path, 'analysis_data')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载数据（分批加载，避免内存溢出）
def load_data(file_path, nrows=100000):
    """加载数据，默认只加载前10万行进行分析"""
    print(f"正在加载数据: {file_path}")
    df = pd.read_csv(file_path, nrows=nrows)
    print(f"数据加载完成，形状: {df.shape}")
    return df

# 基本信息分析
def basic_info_analysis(df):
    """分析数据基本信息"""
    print("\n=== 数据基本信息 ===")
    print(df.info())
    
    print("\n=== 数据前5行 ===")
    print(df.head())
    
    print("\n=== 数据统计描述 ===")
    print(df.describe())
    
    print("\n=== 缺失值检查 ===")
    print(df.isnull().sum())

# 目标变量分析
def target_analysis(df, target_col='FloodProbability'):
    """分析目标变量"""
    print(f"\n=== 目标变量 {target_col} 分析 ===")
    print(f"目标变量均值: {df[target_col].mean()}")
    print(f"目标变量标准差: {df[target_col].std()}")
    print(f"目标变量最小值: {df[target_col].min()}")
    print(f"目标变量最大值: {df[target_col].max()}")
    
    # 绘制目标变量分布
    plt.figure(figsize=(10, 6))
    sns.histplot(df[target_col], bins=50, kde=True)
    plt.title(f'{target_col} 分布')
    plt.xlabel(target_col)
    plt.ylabel('频率')
    plt.savefig(os.path.join(analysis_dir, 'target_distribution.png'))
    plt.close()
    print("目标变量分布图已保存: target_distribution.png")

# 特征相关性分析
def correlation_analysis(df):
    """分析特征相关性"""
    print("\n=== 特征相关性分析 ===")
    
    # 计算相关性矩阵
    corr_matrix = df.corr()
    
    # 绘制相关性热力图
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
    plt.title('特征相关性热力图')
    plt.savefig(os.path.join(analysis_dir, 'correlation_heatmap.png'))
    plt.close()
    print("特征相关性热力图已保存: correlation_heatmap.png")

if __name__ == "__main__":
    # 加载训练数据
    train_df = load_data(os.path.join(csv_dir, 'train.csv'), nrows=100000)
    
    # 基本信息分析
    basic_info_analysis(train_df)
    
    # 目标变量分析
    target_analysis(train_df)
    
    # 特征相关性分析
    correlation_analysis(train_df)
    
    print("\n=== 数据探索完成 ===")