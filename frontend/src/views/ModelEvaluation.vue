<template>
  <div class="model-evaluation-container">
    <!-- 模型性能指标 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <DataAnalysis />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">模型性能指标</span>
            </div>
          </template>
          <div class="performance-metrics">
            <el-row :gutter="20">
              <el-col :xs="24" :sm="12" :md="8" :lg="8">
                <el-statistic :value="evaluationMetrics.testMetrics.mse.toFixed(4)" suffix="" title="均方误差 (MSE)" />
              </el-col>
              <el-col :xs="24" :sm="12" :md="8" :lg="8">
                <el-statistic :value="evaluationMetrics.testMetrics.rmse.toFixed(4)" suffix="" title="均方根误差 (RMSE)" />
              </el-col>
              <el-col :xs="24" :sm="12" :md="8" :lg="8">
                <el-statistic :value="evaluationMetrics.testMetrics.r2.toFixed(3)" suffix="" title="R² 评分" />
              </el-col>
            </el-row>
            <div :style="{
              marginTop: '20px',
              padding: '15px',
              backgroundColor: performanceLevel.bgColor,
              borderRadius: '4px',
              borderLeft: `4px solid ${performanceLevel.borderColor}`
            }">
              <p :style="{ color: performanceLevel.textColor, margin: 0 }">
                <el-icon>
                  <component :is="performanceLevel.icon" />
                </el-icon>
                <span style="margin-left: 8px">{{ performanceDescription }}</span>
              </p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预测结果分析 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" style="border-radius: 8px; height: 100%">
          <template #header>
            <div class="card-header">
              <el-icon>
                <TrendCharts />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">预测值 vs 真实值</span>
            </div>
          </template>
          <div class="predictions-vs-actual">
            <div id="predictionsChart" style="width: 100%; height: 400px"></div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" style="border-radius: 8px; height: 100%">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Histogram />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">预测误差分布</span>
            </div>
          </template>
          <div class="error-distribution">
            <div id="errorChart" style="width: 100%; height: 400px"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 模型参数配置 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Setting />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">模型参数配置</span>
            </div>
          </template>
          <div class="model-params">
            <el-tabs type="border-card">
              <el-tab-pane label="基本参数">
                <el-descriptions :column="3" border>
                  <el-descriptions-item label="模型类型">{{ modelParams.basicParams['模型类型'] || 'LightGBM Regressor'
                  }}</el-descriptions-item>
                  <el-descriptions-item label="目标函数">{{ modelParams.basicParams['目标函数'] || 'regression'
                  }}</el-descriptions-item>
                  <el-descriptions-item label="评估指标">{{ modelParams.basicParams['评估指标'] || 'rmse'
                  }}</el-descriptions-item>
                  <el-descriptions-item label="提升方式">{{ modelParams.basicParams['提升方式'] || 'gbdt'
                  }}</el-descriptions-item>
                  <el-descriptions-item label="学习率">{{ modelParams.basicParams['学习率'] || 0.05 }}</el-descriptions-item>
                  <el-descriptions-item label="树深度">{{ modelParams.basicParams['树深度'] || 8 }}</el-descriptions-item>
                </el-descriptions>
              </el-tab-pane>
              <el-tab-pane label="高级参数">
                <el-descriptions :column="3" border>
                  <el-descriptions-item label="叶子节点数">{{ modelParams.advancedParams['叶子节点数'] || 256
                  }}</el-descriptions-item>
                  <el-descriptions-item label="子采样比例">{{ modelParams.advancedParams['子采样比例'] || 0.8
                  }}</el-descriptions-item>
                  <el-descriptions-item label="特征采样比例">{{ modelParams.advancedParams['特征采样比例'] || 0.8
                  }}</el-descriptions-item>
                  <el-descriptions-item label="最小子样本数">{{ modelParams.advancedParams['最小子样本数'] || 20
                  }}</el-descriptions-item>
                  <el-descriptions-item label="迭代次数">{{ modelParams.advancedParams['迭代次数'] || 1000
                  }}</el-descriptions-item>
                  <el-descriptions-item label="早停轮数">{{ modelParams.advancedParams['早停轮数'] || 50
                  }}</el-descriptions-item>
                </el-descriptions>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 模型训练信息 -->
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Timer />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">模型训练信息</span>
            </div>
          </template>
          <div class="training-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="训练数据量">{{ evaluationMetrics.dataSplits.train_size }}
                行</el-descriptions-item>
              <el-descriptions-item label="验证数据量">{{ evaluationMetrics.dataSplits.val_size }}
                行</el-descriptions-item>
              <el-descriptions-item label="测试数据量">{{ evaluationMetrics.dataSplits.test_size }}
                行</el-descriptions-item>
              <el-descriptions-item label="训练耗时">{{ trainingInfo['训练耗时'] || '120 秒' }}</el-descriptions-item>
              <el-descriptions-item label="最佳迭代轮数">{{ trainingInfo['最佳迭代轮数'] || 850 }}</el-descriptions-item>
              <el-descriptions-item label="模型文件大小">{{ trainingInfo['模型文件大小'] || '15 MB' }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import * as echarts from 'echarts';
import { DataAnalysis, TrendCharts, Histogram, Setting, Timer, Check, Warning, CircleClose } from '@element-plus/icons-vue';
import axios from 'axios';

let predictionsChart = null;
let errorChart = null;

// 模型评估指标
const evaluationMetrics = ref({
  testMetrics: { mse: 0, rmse: 0, r2: 0 },
  trainMetrics: { mse: 0, rmse: 0, r2: 0 },
  valMetrics: { mse: 0, rmse: 0, r2: 0 },
  dataSplits: { trainSize: 0, valSize: 0, testSize: 0 }
});

// 模型参数
const modelParams = ref({
  basicParams: {},
  advancedParams: {}
});

// 训练信息
const trainingInfo = ref({});

// 计算性能描述
const performanceDescription = computed(() => {
  const r2 = evaluationMetrics.value.testMetrics.r2;
  const rmse = evaluationMetrics.value.testMetrics.rmse;

  if (r2 >= 0.9) {
    return `模型性能优秀，R²评分为${r2.toFixed(3)}，预测误差较小（RMSE: ${rmse.toFixed(4)}）`;
  } else if (r2 >= 0.8) {
    return `模型性能良好，R²评分为${r2.toFixed(3)}，预测误差适中（RMSE: ${rmse.toFixed(4)}）`;
  } else if (r2 >= 0.7) {
    return `模型性能一般，R²评分为${r2.toFixed(3)}，预测误差较大（RMSE: ${rmse.toFixed(4)}）`;
  } else {
    return `模型性能较差，R²评分为${r2.toFixed(3)}，预测误差很大（RMSE: ${rmse.toFixed(4)}）`;
  }
});

// 计算性能等级
const performanceLevel = computed(() => {
  const r2 = evaluationMetrics.value.testMetrics.r2;

  if (r2 >= 0.9) {
    return {
      bgColor: '#f0f9eb',
      borderColor: '#67C23A',
      textColor: '#67C23A',
      icon: Check
    };
  } else if (r2 >= 0.8) {
    return {
      bgColor: '#ecf5ff',
      borderColor: '#409EFF',
      textColor: '#409EFF',
      icon: Check
    };
  } else if (r2 >= 0.7) {
    return {
      bgColor: '#fdf6ec',
      borderColor: '#E6A23C',
      textColor: '#E6A23C',
      icon: Warning
    };
  } else {
    return {
      bgColor: '#fef0f0',
      borderColor: '#F56C6C',
      textColor: '#F56C6C',
      icon: CircleClose
    };
  }
});

// 初始化预测值与真实值对比图
const initPredictionsChart = async () => {
  const chartDom = document.getElementById('predictionsChart');
  if (!chartDom) return;

  predictionsChart = echarts.init(chartDom);

  try {
    const response = await axios.get('http://localhost:5000/predictions-comparison');
    const comparisonData = response.data.comparison_data;

    const actualValues = comparisonData.map(item => item.actual);
    const predictedValues = comparisonData.map(item => item.predicted);

    const option = {
      title: {
        text: '预测值 vs 真实值',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      xAxis: {
        type: 'value',
        name: '真实值 (FloodProbability)',
        min: 0.25,
        max: 0.75
      },
      yAxis: {
        type: 'value',
        name: '预测值 (FloodProbability)',
        min: 0.25,
        max: 0.75
      },
      series: [
        {
          name: '预测值',
          type: 'scatter',
          data: actualValues.map((actual, index) => [actual, predictedValues[index]]),
          symbolSize: 6,
          itemStyle: {
            color: '#409EFF'
          }
        },
        {
          name: '理想线',
          type: 'line',
          data: [[0.25, 0.25], [0.75, 0.75]],
          lineStyle: {
            color: '#F56C6C',
            type: 'dashed',
            width: 2
          },
          symbol: 'none'
        }
      ]
    };

    predictionsChart.setOption(option);
  } catch (error) {
    console.error('获取预测对比数据失败:', error);
  }
};

// 初始化误差分布图
const initErrorChart = async () => {
  const chartDom = document.getElementById('errorChart');
  if (!chartDom) return;

  errorChart = echarts.init(chartDom);

  try {
    const response = await axios.get('http://localhost:5000/error-distribution');
    const errorDistribution = response.data.error_distribution;

    const binLabels = errorDistribution.map(item => item.range);
    const histogram = errorDistribution.map(item => item.count);

    const option = {
      title: {
        text: '预测误差分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      xAxis: {
        type: 'category',
        data: binLabels,
        axisLabel: {
          rotate: 45,
          fontSize: 10
        }
      },
      yAxis: {
        type: 'value',
        name: '频率'
      },
      series: [{
        data: histogram,
        type: 'bar',
        itemStyle: {
          color: '#67C23A'
        }
      }]
    };

    errorChart.setOption(option);
  } catch (error) {
    console.error('获取误差分布数据失败:', error);
  }
};

// 加载模型评估指标
const loadEvaluationMetrics = async () => {
  try {
    const response = await axios.get('http://localhost:5000/evaluation');
    evaluationMetrics.value = {
      testMetrics: response.data.test_metrics,
      trainMetrics: response.data.train_metrics,
      valMetrics: response.data.val_metrics,
      dataSplits: response.data.data_splits
    };
  } catch (error) {
    console.error('获取模型评估指标失败:', error);
  }
};

// 加载模型参数
const loadModelParams = async () => {
  try {
    const response = await axios.get('http://localhost:5000/model-params');
    modelParams.value = {
      basicParams: response.data.basic_params,
      advancedParams: response.data.advanced_params
    };
  } catch (error) {
    console.error('获取模型参数失败:', error);
  }
};

// 加载训练信息
const loadTrainingInfo = async () => {
  try {
    const response = await axios.get('http://localhost:5000/training-info');
    trainingInfo.value = response.data;
  } catch (error) {
    console.error('获取训练信息失败:', error);
  }
};

// 响应式处理
const handleResize = () => {
  predictionsChart?.resize();
  errorChart?.resize();
};

onMounted(async () => {
  // 加载模型评估指标
  await loadEvaluationMetrics();
  // 加载模型参数
  await loadModelParams();
  // 加载训练信息
  await loadTrainingInfo();

  // 初始化图表
  initPredictionsChart();
  initErrorChart();

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  // 销毁图表实例
  predictionsChart?.dispose();
  errorChart?.dispose();

  // 移除事件监听
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.model-evaluation-container {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
}

.performance-metrics,
.predictions-vs-actual,
.error-distribution,
.model-params,
.training-info {
  padding: 10px 0;
}
</style>