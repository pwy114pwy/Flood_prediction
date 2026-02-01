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
├── backend/              # Flask后端服务
│   └── app.py         # API服务主文件
├── csv_data/             # 原始数据集
├── data/               # 预处理后的数据
├── evaluation_data/             # 评估数据集
├── frontend/             # Vue前端项目
│   └── src/
│       ├── views/       # 页面组件
│       ├── router/      # 路由配置
│       └── App.vue      # 主应用组件
├── models/              # 训练好的模型
│   ├── lightgbm_model.txt
│   └── feature_columns.pkl
│   ├── feature_importance.pkl
├── notebooks/           # 数据分析和模型训练脚本
│   ├── data_exploration.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── model_evaluation.py
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

## 模型训练

### 数据划分
- **训练集**：80%（894,376 行）
- **验证集**：10%（111,785 行）
- **测试集**：10%（111,796 行）

### 模型参数
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

### 训练策略
- 使用早停（Early Stopping）防止过拟合
- 早停轮数：50
- 最大迭代次数：1000

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

### 后端服务启动
```bash
cd backend
pip install -r requirements.txt
python app.py
```
服务将在 `http://localhost:5000` 启动。

### 前端服务启动
```bash
cd frontend
npm install
npm run dev
```
前端将在 `http://localhost:5173` 启动。

## 项目亮点

1. **科学的模型选择**：基于机器学习领域共识，选择最适合表格数据的梯度提升树模型
2. **大规模数据处理**：成功处理110万行数据，采用分批加载策略避免内存溢出
3. **完整的工程实践**：包含数据探索、特征工程、模型训练、评估、部署全流程
4. **用户友好的界面**：使用Vue + Element Plus构建美观、交互流畅的前端
5. **实时预测功能**：支持单个和批量预测，响应迅速
6. **丰富的可视化**：使用ECharts实现多种图表展示

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

### 项目经验
- 完整的机器学习项目流程
- 实际的数据处理经验
- 模型部署和API开发
- 前端可视化实现

## 作者
- 项目名称：洪涝风险预测系统
- 开发时间：2026年
- 用途：研究生复试展示项目

## 许可证
MIT License