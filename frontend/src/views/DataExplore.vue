<template>
  <div class="data-explore-container">
    <!-- 数据基本信息 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <DataLine />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">数据基本信息</span>
            </div>
          </template>
          <div class="data-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="数据总量">1,117,958 行</el-descriptions-item>
              <el-descriptions-item label="特征数量">20 个</el-descriptions-item>
              <el-descriptions-item label="目标变量">FloodProbability</el-descriptions-item>
              <el-descriptions-item label="数据类型">结构化表格数据</el-descriptions-item>
              <el-descriptions-item label="数据来源">Kaggle 数据集</el-descriptions-item>
              <el-descriptions-item label="缺失值">无</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 目标变量分布 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Histogram />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">目标变量分布</span>
            </div>
          </template>
          <div class="target-distribution">
            <div id="targetChart" style="width: 100%; height: 400px"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 特征相关性分析 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Link />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">特征相关性分析</span>
            </div>
          </template>
          <div class="correlation-analysis">
            <div id="correlationChart" style="width: 100%; height: 500px"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 特征重要性 -->
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Rank />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">特征重要性排序</span>
            </div>
          </template>
          <div class="feature-importance">
            <div id="importanceChart" style="width: 100%; height: 500px"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { DataLine, Histogram, Link, Rank } from '@element-plus/icons-vue';
import axios from 'axios';

let targetChart = null;
let correlationChart = null;
let importanceChart = null;
const featureImportance = ref({});

// 初始化目标变量分布图
const initTargetChart = () => {
  const chartDom = document.getElementById('targetChart');
  if (!chartDom) return;

  targetChart = echarts.init(chartDom);

  const option = {
    title: {
      text: 'FloodProbability 分布',
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
      data: ['0.3-0.35', '0.35-0.4', '0.4-0.45', '0.45-0.5', '0.5-0.55', '0.55-0.6', '0.6-0.65', '0.65-0.7'],
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '频率'
    },
    series: [{
      data: [50000, 120000, 180000, 220000, 250000, 150000, 80000, 30000],
      type: 'bar',
      itemStyle: {
        color: '#409EFF'
      }
    }]
  };

  targetChart.setOption(option);
};

// 初始化相关性热力图
const initCorrelationChart = () => {
  const chartDom = document.getElementById('correlationChart');
  if (!chartDom) return;

  correlationChart = echarts.init(chartDom);

  // 模拟相关性数据
  const features = [
    'MonsoonIntensity', 'TopographyDrainage', 'RiverManagement', 'Deforestation', 'Urbanization',
    'ClimateChange', 'DamsQuality', 'Siltation', 'AgriculturalPractices', 'Encroachments',
    'IneffectiveDisasterPreparedness', 'DrainageSystems', 'CoastalVulnerability', 'Landslides',
    'Watersheds', 'DeterioratingInfrastructure', 'PopulationScore', 'WetlandLoss', 'InadequatePlanning', 'PoliticalFactors'
  ];

  // 生成随机相关性数据（实际项目中应从后端获取）
  const correlationData = [];
  for (let i = 0; i < features.length; i++) {
    for (let j = 0; j < features.length; j++) {
      if (i === j) {
        correlationData.push([i, j, 1]);
      } else {
        correlationData.push([i, j, parseFloat((Math.random() * 0.6 - 0.3).toFixed(2))]);
      }
    }
  }

  const option = {
    title: {
      text: '特征相关性热力图',
      left: 'center'
    },
    tooltip: {
      position: 'top'
    },
    grid: {
      height: '60%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: features,
      splitArea: {
        show: true
      },
      axisLabel: {
        rotate: 45,
        fontSize: 10
      }
    },
    yAxis: {
      type: 'category',
      data: features,
      splitArea: {
        show: true
      },
      axisLabel: {
        fontSize: 10
      }
    },
    visualMap: {
      min: -0.5,
      max: 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '5%',
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      }
    },
    series: [{
      name: '相关性',
      type: 'heatmap',
      data: correlationData,
      label: {
        show: false
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  };

  correlationChart.setOption(option);
};

// 初始化特征重要性图
const initImportanceChart = () => {
  const chartDom = document.getElementById('importanceChart');
  if (!chartDom) return;

  importanceChart = echarts.init(chartDom);

  // 从API获取特征重要性数据
  axios.get('http://localhost:5000/info')
    .then(response => {
      const data = response.data;
      featureImportance.value = data.feature_importance;

      // 转换数据格式
      const importanceData = Object.entries(data.feature_importance)
        .map(([feature, importance]) => ({ feature, importance }))
        .sort((a, b) => b.importance - a.importance);

      const features = importanceData.map(item => item.feature);
      const values = importanceData.map(item => item.importance);

      const option = {
        title: {
          text: '特征重要性排序',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '重要性得分'
        },
        yAxis: {
          type: 'category',
          data: features,
          axisLabel: {
            fontSize: 10
          }
        },
        series: [{
          data: values,
          type: 'bar',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        }]
      };

      importanceChart.setOption(option);
    })
    .catch(error => {
      console.error('获取特征重要性失败:', error);
      // 使用默认数据
      const defaultFeatures = ['IneffectiveDisasterPreparedness', 'Landslides', 'Watersheds', 'TopographyDrainage', 'PoliticalFactors'];
      const defaultValues = [8202, 8159, 8170, 8149, 8124];

      const option = {
        title: {
          text: '特征重要性排序',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '重要性得分'
        },
        yAxis: {
          type: 'category',
          data: defaultFeatures,
          axisLabel: {
            fontSize: 10
          }
        },
        series: [{
          data: defaultValues,
          type: 'bar',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        }]
      };

      importanceChart.setOption(option);
    });
};

// 响应式处理
const handleResize = () => {
  targetChart?.resize();
  correlationChart?.resize();
  importanceChart?.resize();
};

onMounted(() => {
  // 初始化图表
  initTargetChart();
  initCorrelationChart();
  initImportanceChart();

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  // 销毁图表实例
  targetChart?.dispose();
  correlationChart?.dispose();
  importanceChart?.dispose();

  // 移除事件监听
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.data-explore-container {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
}

.data-info {
  padding: 10px 0;
}

.target-distribution,
.correlation-analysis,
.feature-importance {
  padding: 10px 0;
}
</style>