<template>
  <div class="docs-container">
    <el-page-header @back="goBack" title="返回首页" style="margin-bottom: 20px" />

    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon>
            <Document />
          </el-icon>
          <span style="margin-left: 8px; font-weight: bold">系统使用说明与API文档</span>
        </div>
      </template>

      <div class="docs-content">
        <el-collapse v-model="activeNames" accordion>
          <el-collapse-item title="1. 项目概述" name="1">
            <div class="docs-section">
              <p>本项目基于LightGBM模型，对洪涝风险进行预测分析。系统使用了110万行训练数据，包含20个人为设计的特征变量，通过梯度提升树算法构建预测模型，并提供了完整的数据探索、模型评估和实时预测功能。</p>
            </div>
          </el-collapse-item>

          <el-collapse-item title="2. 功能导航" name="2">
            <div class="docs-section">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="首页">
                  系统概览、数据基本信息、模型概览、功能导航
                </el-descriptions-item>
                <el-descriptions-item label="数据探索">
                  数据基本信息展示、目标变量分布图、特征相关性热力图、特征重要性排序
                </el-descriptions-item>
                <el-descriptions-item label="模型评估">
                  模型性能指标（MSE、RMSE、R²）、预测值 vs 真实值散点图、预测误差分布图、模型参数配置、模型训练信息
                </el-descriptions-item>
                <el-descriptions-item label="预测分析">
                  20个特征的输入表单（滑块控件）、实时预测结果展示、风险等级评估（低/中/高）、风险描述和建议、特征重要性参考
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-collapse-item>

          <el-collapse-item title="3. 数据集说明" name="3">
            <div class="docs-section">
              <h4>数据规模</h4>
              <ul>
                <li>训练数据：{{ stats.totalRecords.toLocaleString() }} 行</li>
                <li>特征数量：{{ stats.featureCount }} 个</li>
                <li>目标变量：{{ stats.targetVariable }}（洪涝风险概率，范围：{{ stats.targetStats.min.toFixed(3) }}-{{
                  stats.targetStats.max.toFixed(3) }}）</li>
                <li>数据类型：{{ stats.dataType }}</li>
              </ul>

              <h4>特征列表</h4>
              <el-table :data="features" style="width: 100%; margin-top: 10px" border>
                <el-table-column prop="id" label="序号" width="80" />
                <el-table-column prop="name" label="特征名称" />
                <el-table-column prop="description" label="说明" />
              </el-table>
            </div>
          </el-collapse-item>

          <el-collapse-item title="4. 模型性能" name="4">
            <div class="docs-section">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="均方误差 (MSE)">{{ evaluationMetrics.testMetrics.mse.toFixed(4)
                  }}</el-descriptions-item>
                <el-descriptions-item label="均方根误差 (RMSE)">{{ evaluationMetrics.testMetrics.rmse.toFixed(4)
                  }}</el-descriptions-item>
                <el-descriptions-item label="R² 评分" :span="2">{{ evaluationMetrics.testMetrics.r2.toFixed(3)
                  }}</el-descriptions-item>
              </el-descriptions>

              <h4>性能分析</h4>
              <ul>
                <li v-if="evaluationMetrics.testMetrics.r2 >= 0.9">R²评分为{{ evaluationMetrics.testMetrics.r2.toFixed(3)
                  }}，接近1，说明模型拟合效果优秀</li>
                <li v-else-if="evaluationMetrics.testMetrics.r2 >= 0.8">R²评分为{{
                  evaluationMetrics.testMetrics.r2.toFixed(3)
                  }}，说明模型拟合效果良好</li>
                <li v-else-if="evaluationMetrics.testMetrics.r2 >= 0.7">R²评分为{{
                  evaluationMetrics.testMetrics.r2.toFixed(3)
                  }}，说明模型拟合效果一般</li>
                <li v-else>R²评分为{{ evaluationMetrics.testMetrics.r2.toFixed(3) }}，说明模型拟合效果较差</li>
                <li>RMSE为{{ evaluationMetrics.testMetrics.rmse.toFixed(4) }}，{{ evaluationMetrics.testMetrics.rmse <
                  0.05 ? '预测误差较小，在可接受范围内' : evaluationMetrics.testMetrics.rmse < 0.1 ? '预测误差适中' : '预测误差较大' }}</li>
                <li>模型在训练集（R²: {{ evaluationMetrics.trainMetrics.r2.toFixed(3) }}）、验证集（R²: {{
                  evaluationMetrics.valMetrics.r2.toFixed(3) }}）和测试集（R²: {{ evaluationMetrics.testMetrics.r2.toFixed(3)
                  }}）上表现{{ Math.abs(evaluationMetrics.trainMetrics.r2 - evaluationMetrics.testMetrics.r2) < 0.01 ? '稳定'
                    : '存在一定差异' }}</li>
              </ul>
            </div>
          </el-collapse-item>

          <el-collapse-item title="5. API接口文档" name="5">
            <div class="docs-section">
              <el-table :data="apiList" style="width: 100%; margin-top: 10px" border>
                <el-table-column prop="method" label="方法" width="100" />
                <el-table-column prop="path" label="路径" />
                <el-table-column prop="description" label="说明" />
              </el-table>
            </div>
          </el-collapse-item>

          <el-collapse-item title="6. 使用指南" name="6">
            <div class="docs-section">
              <h4>预测分析使用步骤</h4>
              <ol>
                <li>进入"预测分析"页面</li>
                <li>调整20个特征的滑块值（范围：0-10）</li>
                <li>点击"预测"按钮</li>
                <li>查看预测结果和风险等级</li>
                <li>根据建议采取相应措施</li>
              </ol>

              <h4>风险等级说明</h4>
              <el-alert title="低风险" type="success" :closable="false" style="margin-bottom: 10px">
                洪涝风险概率较低，建议保持常规监测，定期检查排水系统。
              </el-alert>
              <el-alert title="中风险" type="warning" :closable="false" style="margin-bottom: 10px">
                洪涝风险概率中等，建议加强监测，检查排水系统，准备应急措施。
              </el-alert>
              <el-alert title="高风险" type="error" :closable="false">
                洪涝风险概率较高，建议立即采取防范措施，启动应急预案。
              </el-alert>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Document } from '@element-plus/icons-vue';
import axios from 'axios';

const router = useRouter();
const activeNames = ref(['1']);

const evaluationMetrics = ref({
  testMetrics: { mse: 0, rmse: 0, r2: 0 },
  trainMetrics: { mse: 0, rmse: 0, r2: 0 },
  valMetrics: { mse: 0, rmse: 0, r2: 0 }
});

const stats = ref({
  totalRecords: 0,
  featureCount: 0,
  targetVariable: 'FloodProbability',
  dataType: '结构化表格数据',
  targetStats: {
    mean: 0,
    std: 0,
    min: 0,
    max: 0,
    median: 0
  }
});

const features = [
  { id: 1, name: 'MonsoonIntensity', description: '季风强度' },
  { id: 2, name: 'TopographyDrainage', description: '地形排水' },
  { id: 3, name: 'RiverManagement', description: '河流管理' },
  { id: 4, name: 'Deforestation', description: '森林砍伐' },
  { id: 5, name: 'Urbanization', description: '城市化' },
  { id: 6, name: 'ClimateChange', description: '气候变化' },
  { id: 7, name: 'DamsQuality', description: '大坝质量' },
  { id: 8, name: 'Siltation', description: '淤积' },
  { id: 9, name: 'AgriculturalPractices', description: '农业实践' },
  { id: 10, name: 'Encroachments', description: '侵占' },
  { id: 11, name: 'IneffectiveDisasterPreparedness', description: '无效的灾害防范' },
  { id: 12, name: 'DrainageSystems', description: '排水系统' },
  { id: 13, name: 'CoastalVulnerability', description: '沿海脆弱性' },
  { id: 14, name: 'Landslides', description: '山体滑坡' },
  { id: 15, name: 'Watersheds', description: '流域' },
  { id: 16, name: 'DeterioratingInfrastructure', description: '基础设施恶化' },
  { id: 17, name: 'PopulationScore', description: '人口评分' },
  { id: 18, name: 'WetlandLoss', description: '湿地损失' },
  { id: 19, name: 'InadequatePlanning', description: '规划不足' },
  { id: 20, name: 'PoliticalFactors', description: '政治因素' }
];

const apiList = [
  { method: 'GET', path: '/health', description: '健康检查' },
  { method: 'GET', path: '/info', description: '获取模型信息' },
  { method: 'GET', path: '/stats', description: '获取数据统计信息' },
  { method: 'GET', path: '/distribution', description: '获取目标变量分布' },
  { method: 'GET', path: '/correlation', description: '获取特征相关性' },
  { method: 'GET', path: '/evaluation', description: '获取模型评估指标' },
  { method: 'GET', path: '/predictions-comparison', description: '获取预测对比数据' },
  { method: 'GET', path: '/error-distribution', description: '获取误差分布' },
  { method: 'GET', path: '/feature-importance', description: '获取特征重要性' },
  { method: 'GET', path: '/model-params', description: '获取模型参数' },
  { method: 'GET', path: '/training-info', description: '获取训练信息' },
  { method: 'POST', path: '/predict', description: '单样本预测' },
  { method: 'POST', path: '/predict/batch', description: '批量预测' }
];

const loadEvaluationMetrics = async () => {
  try {
    const response = await axios.get('http://localhost:5000/evaluation');
    evaluationMetrics.value = {
      testMetrics: response.data.test_metrics,
      trainMetrics: response.data.train_metrics,
      valMetrics: response.data.val_metrics
    };
  } catch (error) {
    console.error('获取模型评估指标失败:', error);
  }
};

const loadStats = async () => {
  try {
    const response = await axios.get('http://localhost:5000/stats');
    stats.value = {
      totalRecords: response.data.total_records,
      featureCount: response.data.feature_count,
      targetVariable: response.data.target_variable,
      dataType: response.data.data_type,
      targetStats: response.data.target_stats
    };
  } catch (error) {
    console.error('获取数据统计信息失败:', error);
  }
};

const goBack = () => {
  router.push('/');
};

onMounted(async () => {
  await loadEvaluationMetrics();
  await loadStats();
});
</script>

<style scoped>
.docs-container {
  width: 100%;
  padding: 20px;
}

.card-header {
  display: flex;
  align-items: center;
}

.docs-content {
  padding: 20px 0;
}

.docs-section {
  padding: 10px 0;
}

.docs-section h4 {
  margin: 20px 0 10px 0;
  color: #303133;
}

.docs-section ul {
  margin: 10px 0;
  padding-left: 20px;
}

.docs-section li {
  margin: 5px 0;
  color: #606266;
}

.docs-section ol {
  margin: 10px 0;
  padding-left: 20px;
}

.docs-section p {
  margin: 10px 0;
  color: #606266;
  line-height: 1.6;
}
</style>
