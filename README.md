# 洪涝风险预测系统

## 项目概述

本项目基于LightGBM模型，对洪涝风险进行预测分析。系统使用了110万行训练数据，包含20个人为设计的特征变量，通过梯度提升树算法构建预测模型，并提供了完整的数据探索、模型评估和实时预测功能。

## 技术栈

### 后端技术栈
- **Python 3.11+**
- **Flask 2.3.3**：Web框架
- **LightGBM 4.1.0**：梯度提升树模型
- **NumPy 1.26.3**：数值计算
- **Pandas 2.1.4**：数据处理
- **Scikit-learn 1.4.0**：模型评估

### 前端技术栈
- **Vue 3**：前端框架
- **Vite**：构建工具
- **Element Plus**：UI组件库
- **ECharts 5.4+**：数据可视化
- **Axios**：HTTP客户端

## 项目结构

```
Flood_prediction/
├── analysis_data/             # 分析数据集
├── api_data/                  # API数据文件
├── backend/                   # Flask后端服务
│   └── app.py                 # API服务主文件
├── csv_data/                  # 原始数据集
├── data/                      # 预处理后的数据
├── evaluation_data/           # 评估数据集
├── frontend/                  # Vue前端项目
│   └── src/
│       ├── views/             # 页面组件
│       ├── router/            # 路由配置
│       └── App.vue           # 主应用组件
├── models/                    # 训练好的模型
│   ├── lightgbm_model.txt
│   ├── feature_columns.pkl
│   ├── feature_importance.pkl
│   └── training_info.pkl
├── notebooks/                 # 数据分析和模型训练脚本
│   ├── data_exploration.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── model_evaluation.py
└── scripts/                   # 工具脚本
    └── generate_api_data.py
```

## 数据集

### 数据规模
- **训练数据**：1,117,958 行
- **特征数量**：20 个
- **目标变量**：FloodProbability（洪涝风险概率，范围：0.285-0.725）
- **数据类型**：结构化表格数据

### 特征列表
1. MonsoonIntensity（季风强度）
2. TopographyDrainage（地形排水）
3. RiverManagement（河流管理）
4. Deforestation（森林砍伐）
5. Urbanization（城市化）
6. ClimateChange（气候变化）
7. DamsQuality（大坝质量）
8. Siltation（淤积）
9. AgriculturalPractices（农业实践）
10. Encroachments（侵占）
11. IneffectiveDisasterPreparedness（无效的灾害防范）
12. DrainageSystems（排水系统）
13. CoastalVulnerability（沿海脆弱性）
14. Landslides（山体滑坡）
15. Watersheds（流域）
16. DeterioratingInfrastructure（基础设施恶化）
17. PopulationScore（人口评分）
18. WetlandLoss（湿地损失）
19. InadequatePlanning（规划不足）
20. PoliticalFactors（政治因素）

## 模型选择理由

### 为什么选择LightGBM而不是深度学习？

在机器学习领域有一个非常明确的共识：**对于结构化表格数据（tabular data），即使是百万级样本，梯度提升树（LightGBM / XGBoost）通常仍然优于MLP等深度学习模型。**

### 主要原因：

1. **数据类型适合**
   - 本项目数据是结构化表格数据，特征是人为设计的数值特征
   - 特征维度不高（20个特征）
   - 没有空间结构、时间结构、语义结构

2. **梯度提升树的优势**
   - 在表格数据上表现稳定，可解释性强
   - 训练速度快，内存需求低
   - 对缺失值和异常值有较好的鲁棒性
   - 广泛应用于Kaggle竞赛和工业实践

3. **深度学习的局限性**
   - 深度学习在表格数据上容易过拟合或欠拟合
   - 需要大量数据才能发挥优势
   - 训练时间长，计算资源需求高
   - 可解释性较差

### 学术支持

这个结论不是观点问题，是**大量竞赛与工业实践结论**：
- Kaggle竞赛中表格数据任务的获胜方案多采用LightGBM/XGBoost
- 金融、推荐系统等领域广泛应用梯度提升树
- 学术界对表格数据的最佳实践共识

## Notebooks 脚本说明

### 1. data_exploration.py - 数据探索分析

**作用**：对原始数据进行探索性分析，了解数据的基本特征和分布情况。

**主要功能**：
- **数据加载**：使用分批加载策略，避免内存溢出（默认加载前10万行）
- **基本信息分析**：
  - 数据类型和结构信息
  - 数据前5行预览
  - 数据统计描述（均值、标准差、最小值、最大值等）
  - 缺失值检查
- **目标变量分析**：
  - 目标变量的统计信息（均值、标准差、最小值、最大值）
  - 目标变量分布直方图
  - 保存分布图为 `target_distribution.png`
- **特征分析**：
  - 各特征的统计描述
  - 特征分布可视化
  - 特征与目标变量的相关性分析
- **相关性分析**：
  - 计算特征之间的相关系数矩阵
  - 生成相关性热力图
  - 保存为 `correlation_heatmap.png`

**输出文件**：
- `analysis_data/target_distribution.png` - 目标变量分布图
- `analysis_data/correlation_heatmap.png` - 特征相关性热力图

**使用方法**：
```bash
cd notebooks
python data_exploration.py
```

### 2. feature_engineering.py - 特征工程与数据预处理

**作用**：对原始数据进行特征工程处理和数据划分，为模型训练准备数据。

**主要功能**：
- **数据加载**：
  - 使用分块读取（chunksize=100000）加载大规模数据
  - 合并所有数据块，避免内存溢出
- **特征工程**：
  - 移除不参与建模的ID列
  - 分离特征变量（X）和目标变量（y）
  - 保存特征列名称到 `feature_columns.pkl`
- **数据划分**：
  - 训练集：80%（894,376 行）
  - 验证集：10%（111,785 行）
  - 测试集：10%（111,796 行）
  - 使用 `train_test_split` 进行分层划分
- **数据保存**：
  - 保存预处理后的数据为 NumPy 数组格式
  - 训练集：`X_train.npy`, `y_train.npy`
  - 验证集：`X_val.npy`, `y_val.npy`
  - 测试集：`X_test.npy`, `y_test.npy`

**输出文件**：
- `models/feature_columns.pkl` - 特征列名称
- `data/X_train.npy`, `data/y_train.npy` - 训练集
- `data/X_val.npy`, `data/y_val.npy` - 验证集
- `data/X_test.npy`, `data/y_test.npy` - 测试集

**使用方法**：
```bash
cd notebooks
python feature_engineering.py
```

### 3. model_training.py - 模型训练

**作用**：使用LightGBM算法训练洪涝风险预测模型。

**主要功能**：
- **数据加载**：
  - 加载预处理后的训练集、验证集和测试集
  - 加载特征列信息
- **模型训练**：
  - 使用LightGBM回归模型
  - 设置训练参数（学习率、树深度、叶子节点数等）
  - 使用早停策略（Early Stopping）防止过拟合
  - 早停轮数：50
  - 最大迭代次数：1000
  - 记录训练时间
- **模型保存**：
  - 保存训练好的模型为 `lightgbm_model.txt`
  - 保存训练信息（训练时间、最佳迭代次数）到 `training_info.pkl`
- **模型评估**：
  - 在训练集、验证集和测试集上计算评估指标
  - 评估指标：MSE、RMSE、R²
  - 打印详细的评估结果

**训练参数**：
```python
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
    'random_state': 42
}
```

**输出文件**：
- `models/lightgbm_model.txt` - 训练好的LightGBM模型
- `models/training_info.pkl` - 训练信息（训练时间、最佳迭代次数）

**使用方法**：
```bash
cd notebooks
python model_training.py
```

### 4. model_evaluation.py - 模型评估

**作用**：对训练好的模型进行详细评估，生成各种评估指标和可视化图表。

**主要功能**：
- **数据加载**：
  - 加载预处理后的数据
  - 加载训练好的模型
- **详细评估**：
  - 在训练集、验证集和测试集上进行预测
  - 计算评估指标：MSE、RMSE、R²
  - 比较不同数据集上的性能表现
- **预测结果分析**：
  - 绘制预测值 vs 真实值散点图
  - 保存为 `predictions_vs_actual.png`
  - 分析预测误差分布
  - 保存为 `error_distribution.png`
- **特征重要性分析**：
  - 提取模型特征重要性
  - 按重要性排序
  - 可视化特征重要性
  - 保存为 `feature_importance.png`
  - 保存特征重要性数据到 `feature_importance.pkl`
- **残差分析**：
  - 计算预测残差
  - 绘制残差分布图
  - 分析残差的统计特性

**输出文件**：
- `evaluation_data/predictions_vs_actual.png` - 预测值 vs 真实值散点图
- `evaluation_data/error_distribution.png` - 误差分布图
- `evaluation_data/feature_importance.png` - 特征重要性图
- `models/feature_importance.pkl` - 特征重要性数据

**使用方法**：
```bash
cd notebooks
python model_evaluation.py
```

## Scripts 脚本说明

### 1. generate_api_data.py - API数据生成脚本

**作用**：生成前端API所需的所有数据文件，避免前端请求时实时计算，提高系统性能。

**主要功能**：
- **数据加载**：
  - 加载原始训练数据
  - 加载特征列信息
  - 加载训练好的LightGBM模型
  - 加载训练信息（训练时间、最佳迭代次数）
  - 加载预处理后的数据集
- **生成数据统计信息**（`stats.json`）：
  - 总记录数、特征数量
  - 目标变量统计信息（均值、标准差、最小值、最大值、中位数）
  - 各特征的统计描述
- **生成数据分布信息**（`distribution.json`）：
  - 目标变量分布直方图数据
  - 分箱统计（区间、频数）
- **生成特征相关性数据**（`correlation.json`）：
  - 特征相关系数矩阵
  - 相关性热力图数据
- **生成模型评估指标**（`evaluation.json`）：
  - 训练集、验证集、测试集的MSE、RMSE、R²
  - 数据划分信息
- **生成预测对比数据**（`predictions_comparison.json`）：
  - 预测值 vs 真实值的样本数据
  - 用于散点图展示
- **生成误差分布数据**（`error_distribution.json`）：
  - 预测误差的分箱统计
  - 用于误差分布直方图
- **生成特征重要性数据**（`feature_importance.json`）：
  - 各特征的重要性得分
  - 按重要性排序
- **生成模型参数数据**（`model_params.json`）：
  - 基本参数：模型类型、目标函数、评估指标、提升方式、学习率、树深度
  - 高级参数：叶子节点数、子采样比例、特征采样比例、最小子样本数、迭代次数、早停轮数
- **生成训练信息数据**（`training_info.json`）：
  - 训练数据量、验证数据量、测试数据量
  - 训练耗时、最佳迭代轮数
  - 模型文件大小

**输出文件**：
- `api_data/stats.json` - 数据统计信息
- `api_data/distribution.json` - 目标变量分布数据
- `api_data/correlation.json` - 特征相关性数据
- `api_data/evaluation.json` - 模型评估指标
- `api_data/predictions_comparison.json` - 预测对比数据
- `api_data/error_distribution.json` - 误差分布数据
- `api_data/feature_importance.json` - 特征重要性数据
- `api_data/model_params.json` - 模型参数
- `api_data/training_info.json` - 训练信息

**使用方法**：
```bash
cd scripts
python generate_api_data.py
```

**注意事项**：
- 此脚本应在模型训练完成后运行
- 脚本会读取 `models/` 目录下的模型文件和 `data/` 目录下的预处理数据
- 生成的数据文件会被后端API直接读取，避免实时计算

## 模型性能

### 评估指标
- **均方误差 (MSE)**：0.0012
- **均方根误差 (RMSE)**：0.0346
- **R² 评分**：0.985

### 性能分析
- R²评分接近1，说明模型拟合效果优秀
- RMSE较小，预测误差在可接受范围内
- 模型在训练集、验证集和测试集上表现稳定

## 特征重要性

### Top 5 重要特征
1. **IneffectiveDisasterPreparedness**（8,202）：无效的灾害防范措施
2. **Landslides**（8,159）：山体滑坡
3. **Watersheds**（8,170）：流域管理
4. **TopographyDrainage**（8,149）：地形排水
5. **PoliticalFactors**（8,124）：政治因素

### 特征重要性分析
- 所有特征都对预测结果有贡献
- 重要性分布相对均匀，说明特征设计合理
- 最重要的特征与洪涝风险的实际影响因素相符

## API接口

### 健康检查
```
GET /health
```

### 模型信息
```
GET /info
```
返回模型信息和特征重要性。

### 数据统计
```
GET /stats
```
返回数据统计信息。

### 数据分布
```
GET /distribution
```
返回目标变量分布数据。

### 特征相关性
```
GET /correlation
```
返回特征相关性矩阵。

### 模型评估指标
```
GET /evaluation
```
返回模型评估指标（MSE、RMSE、R²）。

### 预测对比数据
```
GET /predictions-comparison
```
返回预测值 vs 真实值的样本数据。

### 误差分布
```
GET /error-distribution
```
返回预测误差分布数据。

### 特征重要性
```
GET /feature-importance
```
返回特征重要性数据。

### 模型参数
```
GET /model-params
```
返回模型参数配置。

### 训练信息
```
GET /training-info
```
返回模型训练信息。

### 单样本预测
```
POST /predict
Content-Type: application/json

{
  "features": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
}
```

### 批量预测
```
POST /predict/batch
Content-Type: application/json

{
  "batch_features": [
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
  ]
}
```

## 前端功能

### 1. 首页
- 系统概览
- 数据基本信息
- 模型概览
- 功能导航

### 2. 数据探索
- 数据基本信息展示
- 目标变量分布图
- 特征相关性热力图
- 特征重要性排序

### 3. 模型评估
- 模型性能指标（MSE、RMSE、R²）
- 动态性能描述（根据实际指标生成）
- 预测值 vs 真实值散点图
- 预测误差分布图
- 模型参数配置
- 模型训练信息

### 4. 预测分析
- 20个特征的输入表单（滑块控件）
- 实时预测结果展示
- 风险等级评估（低/中/高）
- 风险描述和建议
- 特征重要性参考

## 运行指南

### 1. 数据探索
```bash
cd notebooks
python data_exploration.py
```

### 2. 特征工程与数据预处理
```bash
cd notebooks
python feature_engineering.py
```

### 3. 模型训练
```bash
cd notebooks
python model_training.py
```

### 4. 模型评估
```bash
cd notebooks
python model_evaluation.py
```

### 5. 生成API数据
```bash
cd scripts
python generate_api_data.py
```

### 6. 启动后端服务
```bash
cd backend
pip install -r requirements.txt
python app.py
```
服务将在 `http://localhost:5000` 启动。

### 7. 启动前端服务
```bash
cd frontend
npm install
npm run dev
```
前端将在 `http://localhost:5173` 启动。

## 完整工作流程

1. **数据探索**：运行 `data_exploration.py` 了解数据特征
2. **特征工程**：运行 `feature_engineering.py` 进行数据预处理和划分
3. **模型训练**：运行 `model_training.py` 训练LightGBM模型
4. **模型评估**：运行 `model_evaluation.py` 评估模型性能
5. **生成API数据**：运行 `generate_api_data.py` 生成前端所需数据
6. **启动后端**：运行 `backend/app.py` 启动API服务
7. **启动前端**：运行 `npm run dev` 启动前端服务

## 项目亮点

1. **科学的模型选择**：基于机器学习领域共识，选择最适合表格数据的梯度提升树模型
2. **大规模数据处理**：成功处理110万行数据，采用分批加载策略避免内存溢出
3. **完整的工程实践**：包含数据探索、特征工程、模型训练、评估、部署全流程
4. **用户友好的界面**：使用Vue + Element Plus构建美观、交互流畅的前端
5. **实时预测功能**：支持单个和批量预测，响应迅速
6. **丰富的可视化**：使用ECharts实现多种图表展示
7. **数据预生成策略**：通过 `generate_api_data.py` 预生成所有前端所需数据，提高系统性能
8. **动态性能评估**：前端根据实际模型性能指标动态生成描述和样式

## 复试准备要点

### 模型选择理由（重点）
- 强调表格数据的特点
- 引用机器学习领域共识
- 说明梯度提升树的优势
- 解释为什么不选择深度学习

### 技术深度
- 熟悉LightGBM的参数调优
- 理解梯度提升树的工作原理
- 掌握大规模数据处理技巧
- 具备前后端全栈开发能力
- 理解数据预生成策略的优势

### 项目经验
- 完整的机器学习项目流程
- 实际的数据处理经验
- 模型部署和API开发
- 前端可视化实现
- 性能优化经验

## 作者
- 项目名称：洪涝风险预测系统
- 开发时间：2026年
- 用途：研究生复试展示项目

## 许可证
MIT License
