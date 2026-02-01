<template>
  <div class="home-container">
    <!-- 系统概览卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <InfoFilled />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">系统概览</span>
            </div>
          </template>
          <div class="overview-content">
            <p style="font-size: 16px; line-height: 1.6; color: #606266">
              本系统基于LightGBM模型，对洪涝风险进行预测分析。系统使用了110万行训练数据，
              包含20个人为设计的特征变量，通过梯度提升树算法构建预测模型，
              并提供了数据探索、模型评估和实时预测功能。
            </p>
            <div style="margin-top: 20px; display: flex; flex-wrap: wrap; gap: 20px">
              <el-statistic :value="systemStats.totalRecords" :precision="0" suffix="行" title="训练数据量" />
              <el-statistic :value="systemStats.featureCount" :precision="0" suffix="个" title="特征变量" />
              <el-statistic :value="modelInfo.modelName" title="模型类型" />
              <el-statistic :value="systemStats.modelAccuracy" title="模型准确率" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据概览卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" style="border-radius: 8px; height: 100%">
          <template #header>
            <div class="card-header">
              <el-icon>
                <DataLine />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">数据概览</span>
            </div>
          </template>
          <div class="data-overview">
            <el-table :data="dataInfo" style="width: 100%">
              <el-table-column prop="name" label="数据文件" width="120" />
              <el-table-column prop="size" label="文件大小" />
              <el-table-column prop="records" label="记录数" />
            </el-table>
          </div>
        </el-card>
      </el-col>

      <!-- 模型概览卡片 -->
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" style="border-radius: 8px; height: 100%">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Star />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">模型概览</span>
            </div>
          </template>
          <div class="model-overview">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="模型名称">{{ modelInfo.modelName || 'LightGBM Regressor'
              }}</el-descriptions-item>
              <el-descriptions-item label="训练数据">{{ systemStats.totalRecords.toLocaleString() }} 行 × {{
                systemStats.featureCount }} 特征</el-descriptions-item>
              <el-descriptions-item label="预测目标">{{ modelInfo.targetVariable || 'FloodProbability'
              }}</el-descriptions-item>
              <el-descriptions-item label="评估指标">MSE, RMSE, R²</el-descriptions-item>
              <el-descriptions-item label="API服务">{{ modelInfo.apiService || 'http://localhost:5000'
              }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 功能导航卡片 -->
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Grid />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">功能导航</span>
            </div>
          </template>
          <div class="function-nav">
            <el-grid :cols="4" :gutter="20">
              <el-grid-item>
                <el-card @click="navigateTo('/explore')"
                  style="cursor: pointer; border-radius: 8px; text-align: center; padding: 30px 0; transition: all 0.3s"
                  hover>
                  <el-icon style="font-size: 32px; color: #409EFF; margin-bottom: 12px">
                    <DataAnalysis />
                  </el-icon>
                  <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px">数据探索</div>
                  <div style="font-size: 14px; color: #909399">分析特征分布与相关性</div>
                </el-card>
              </el-grid-item>
              <el-grid-item>
                <el-card @click="navigateTo('/model')"
                  style="cursor: pointer; border-radius: 8px; text-align: center; padding: 30px 0; transition: all 0.3s"
                  hover>
                  <el-icon style="font-size: 32px; color: #67C23A; margin-bottom: 12px">
                    <Histogram />
                  </el-icon>
                  <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px">模型评估</div>
                  <div style="font-size: 14px; color: #909399">查看模型性能与特征重要性</div>
                </el-card>
              </el-grid-item>
              <el-grid-item>
                <el-card @click="navigateTo('/predict')"
                  style="cursor: pointer; border-radius: 8px; text-align: center; padding: 30px 0; transition: all 0.3s"
                  hover>
                  <el-icon style="font-size: 32px; color: #E6A23C; margin-bottom: 12px">
                    <MagicStick />
                  </el-icon>
                  <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px">预测分析</div>
                  <div style="font-size: 14px; color: #909399">输入特征，获取实时预测结果</div>
                </el-card>
              </el-grid-item>
              <el-grid-item>
                <el-card @click="navigateTo('/docs')"
                  style="cursor: pointer; border-radius: 8px; text-align: center; padding: 30px 0; transition: all 0.3s"
                  hover>
                  <el-icon style="font-size: 32px; color: #F56C6C; margin-bottom: 12px">
                    <Document />
                  </el-icon>
                  <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px">文档中心</div>
                  <div style="font-size: 14px; color: #909399">查看系统使用说明与API文档</div>
                </el-card>
              </el-grid-item>
            </el-grid>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { InfoFilled, DataLine, Star, Grid, DataAnalysis, Histogram, MagicStick, Document } from '@element-plus/icons-vue';
import axios from 'axios';

const router = useRouter();

// 数据文件信息
const dataInfo = ref([
  { name: 'train.csv', size: '59.1 MB', records: '1,117,958' },
  { name: 'test.csv', size: '36.1 MB', records: '~400,000' },
  { name: 'sample_submission.csv', size: '8.9 MB', records: '~400,000' }
]);

// 系统统计数据
const systemStats = ref({
  totalRecords: 0,
  featureCount: 0,
  modelAccuracy: '0%'
});

// 模型信息
const modelInfo = ref({
  modelName: '',
  targetVariable: '',
  apiService: ''
});

// 加载数据统计
const loadStats = async () => {
  try {
    const response = await axios.get('http://localhost:5000/stats');
    systemStats.value = {
      totalRecords: response.data.total_records,
      featureCount: response.data.feature_count,
      modelAccuracy: '0%'
    };
  } catch (error) {
    console.error('获取数据统计失败:', error);
  }
};

// 加载模型评估指标
const loadEvaluation = async () => {
  try {
    const response = await axios.get('http://localhost:5000/evaluation');
    const r2Score = response.data.test_metrics.r2;
    const accuracy = (r2Score * 100).toFixed(1);
    systemStats.value.modelAccuracy = `${accuracy}%`;
  } catch (error) {
    console.error('获取模型评估指标失败:', error);
  }
};

// 加载模型信息
const loadModelInfo = async () => {
  try {
    const response = await axios.get('http://localhost:5000/info');
    modelInfo.value = {
      modelName: response.data.model,
      targetVariable: 'FloodProbability',
      apiService: 'http://localhost:5000'
    };
  } catch (error) {
    console.error('获取模型信息失败:', error);
  }
};

// 导航到指定页面
const navigateTo = (path) => {
  router.push(path);
};

onMounted(async () => {
  // 页面加载时的初始化操作
  await loadStats();
  await loadEvaluation();
  await loadModelInfo();
  console.log('Home page mounted');
});
</script>

<style scoped>
.home-container {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
}

.overview-content {
  padding: 10px 0;
}

.data-overview,
.model-overview {
  padding: 10px 0;
}

.function-nav {
  padding: 10px 0;
}

/* 卡片悬停效果 */
.el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style>