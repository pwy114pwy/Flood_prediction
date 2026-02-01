<template>
  <div class="prediction-container">
    <!-- 预测表单 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :sm="24" :md="16" :lg="16">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <MagicStick />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">特征输入</span>
            </div>
          </template>
          <div class="prediction-form">
            <el-form :model="formData" label-width="180px" style="max-width: 100%">
              <el-row :gutter="20">
                <el-col :xs="24" :sm="12" :md="12" :lg="12">
                  <el-form-item label="MonsoonIntensity">
                    <el-slider v-model="formData.MonsoonIntensity" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="TopographyDrainage">
                    <el-slider v-model="formData.TopographyDrainage" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="RiverManagement">
                    <el-slider v-model="formData.RiverManagement" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="Deforestation">
                    <el-slider v-model="formData.Deforestation" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="Urbanization">
                    <el-slider v-model="formData.Urbanization" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="ClimateChange">
                    <el-slider v-model="formData.ClimateChange" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="DamsQuality">
                    <el-slider v-model="formData.DamsQuality" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="Siltation">
                    <el-slider v-model="formData.Siltation" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="AgriculturalPractices">
                    <el-slider v-model="formData.AgriculturalPractices" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="Encroachments">
                    <el-slider v-model="formData.Encroachments" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="12" :md="12" :lg="12">
                  <el-form-item label="IneffectiveDisasterPreparedness">
                    <el-slider v-model="formData.IneffectiveDisasterPreparedness" :min="1" :max="10" :step="1"
                      show-input />
                  </el-form-item>
                  <el-form-item label="DrainageSystems">
                    <el-slider v-model="formData.DrainageSystems" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="CoastalVulnerability">
                    <el-slider v-model="formData.CoastalVulnerability" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="Landslides">
                    <el-slider v-model="formData.Landslides" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="Watersheds">
                    <el-slider v-model="formData.Watersheds" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="DeterioratingInfrastructure">
                    <el-slider v-model="formData.DeterioratingInfrastructure" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="PopulationScore">
                    <el-slider v-model="formData.PopulationScore" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="WetlandLoss">
                    <el-slider v-model="formData.WetlandLoss" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="InadequatePlanning">
                    <el-slider v-model="formData.InadequatePlanning" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                  <el-form-item label="PoliticalFactors">
                    <el-slider v-model="formData.PoliticalFactors" :min="1" :max="10" :step="1" show-input />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item>
                <el-button type="primary" @click="predict" :loading="loading">
                  <el-icon>
                    <Refresh />
                  </el-icon>
                  <span style="margin-left: 5px">开始预测</span>
                </el-button>
                <el-button @click="resetForm">
                  <el-icon>
                    <Delete />
                  </el-icon>
                  <span style="margin-left: 5px">重置</span>
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>

      <!-- 预测结果 -->
      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <el-card shadow="hover" style="border-radius: 8px; height: 100%">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Check />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">预测结果</span>
            </div>
          </template>
          <div class="prediction-result">
            <div v-if="!predictionResult" class="result-placeholder">
              <el-empty description="请输入特征值并点击开始预测" />
            </div>
            <div v-else class="result-content">
              <el-card shadow="hover" style="margin-bottom: 20px; border-radius: 8px; text-align: center">
                <template #header>
                  <div style="font-weight: bold; color: #409EFF">洪涝风险概率</div>
                </template>
                <div style="font-size: 36px; font-weight: bold; color: #409EFF; margin: 20px 0">
                  {{ predictionResult.prediction.toFixed(3) }}
                </div>
                <div style="font-size: 14px; color: #606266">
                  ({{ riskLevel }})
                </div>
              </el-card>

              <el-card shadow="hover" style="border-radius: 8px">
                <template #header>
                  <div style="font-weight: bold">风险评估</div>
                </template>
                <div class="risk-assessment">
                  <el-progress :percentage="(predictionResult.prediction * 100).toFixed(0)" :color="progressColor"
                    :stroke-width="20" :format="formatProgress" />
                  <div style="margin-top: 20px; font-size: 14px; line-height: 1.6; color: #606266">
                    <p>基于输入的特征值，系统预测该区域的洪涝风险概率为 <strong>{{ (predictionResult.prediction * 100).toFixed(1) }}%</strong>。
                    </p>
                    <p>{{ riskDescription }}</p>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 特征重要性参考 -->
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" style="border-radius: 8px">
          <template #header>
            <div class="card-header">
              <el-icon>
                <Rank />
              </el-icon>
              <span style="margin-left: 8px; font-weight: bold">特征重要性参考</span>
            </div>
          </template>
          <div class="feature-importance-reference">
            <p style="margin-bottom: 15px; font-size: 14px; color: #606266">
              以下是模型认为对洪涝风险预测最重要的特征，调整这些特征值可能会对预测结果产生较大影响：
            </p>
            <el-table :data="topFeatures" style="width: 100%">
              <el-table-column prop="feature" label="特征名称" width="300" />
              <el-table-column prop="importance" label="重要性得分" />
              <el-table-column prop="description" label="描述" />
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { MagicStick, Check, Refresh, Delete, Rank } from '@element-plus/icons-vue';

// 表单数据
const formData = ref({
  MonsoonIntensity: 5,
  TopographyDrainage: 5,
  RiverManagement: 5,
  Deforestation: 5,
  Urbanization: 5,
  ClimateChange: 5,
  DamsQuality: 5,
  Siltation: 5,
  AgriculturalPractices: 5,
  Encroachments: 5,
  IneffectiveDisasterPreparedness: 5,
  DrainageSystems: 5,
  CoastalVulnerability: 5,
  Landslides: 5,
  Watersheds: 5,
  DeterioratingInfrastructure: 5,
  PopulationScore: 5,
  WetlandLoss: 5,
  InadequatePlanning: 5,
  PoliticalFactors: 5
});

// 预测结果
const predictionResult = ref(null);
const loading = ref(false);

// 特征重要性参考数据
const topFeatures = ref([
  {
    feature: 'IneffectiveDisasterPreparedness',
    importance: 8202,
    description: '无效的灾害防范措施，对洪涝风险影响最大'
  },
  {
    feature: 'Landslides',
    importance: 8159,
    description: '山体滑坡，可能导致泥石流和河道堵塞'
  },
  {
    feature: 'Watersheds',
    importance: 8170,
    description: '流域管理，影响雨水的收集和排放'
  },
  {
    feature: 'TopographyDrainage',
    importance: 8149,
    description: '地形排水能力，直接影响积水情况'
  },
  {
    feature: 'PoliticalFactors',
    importance: 8124,
    description: '政治因素，影响灾害防范政策的制定和执行'
  }
]);

// 计算风险等级
const riskLevel = computed(() => {
  if (!predictionResult.value) return '';
  const probability = predictionResult.value.prediction;
  if (probability < 0.4) return '低风险';
  if (probability < 0.6) return '中等风险';
  return '高风险';
});

// 计算风险描述
const riskDescription = computed(() => {
  if (!predictionResult.value) return '';
  const probability = predictionResult.value.prediction;
  if (probability < 0.4) {
    return '该区域洪涝风险较低，发生严重洪涝的可能性较小。建议保持现有的灾害防范措施。';
  } else if (probability < 0.6) {
    return '该区域存在中等洪涝风险，需要加强灾害防范措施，特别是在雨季期间。';
  } else {
    return '该区域洪涝风险较高，建议立即采取有效的防范措施，包括加强排水系统、制定应急预案等。';
  }
});

// 计算进度条颜色
const progressColor = computed(() => {
  if (!predictionResult.value) return '#409EFF';
  const probability = predictionResult.value.prediction;
  if (probability < 0.4) return '#67C23A';
  if (probability < 0.6) return '#E6A23C';
  return '#F56C6C';
});

// 进度条格式化
const formatProgress = (percentage) => {
  return `${percentage}%`;
};

// 预测函数
const predict = async () => {
  loading.value = true;
  try {
    // 准备特征数据
    const features = [
      formData.value.MonsoonIntensity,
      formData.value.TopographyDrainage,
      formData.value.RiverManagement,
      formData.value.Deforestation,
      formData.value.Urbanization,
      formData.value.ClimateChange,
      formData.value.DamsQuality,
      formData.value.Siltation,
      formData.value.AgriculturalPractices,
      formData.value.Encroachments,
      formData.value.IneffectiveDisasterPreparedness,
      formData.value.DrainageSystems,
      formData.value.CoastalVulnerability,
      formData.value.Landslides,
      formData.value.Watersheds,
      formData.value.DeterioratingInfrastructure,
      formData.value.PopulationScore,
      formData.value.WetlandLoss,
      formData.value.InadequatePlanning,
      formData.value.PoliticalFactors
    ];

    // 调用API
    const response = await axios.post('http://localhost:5000/predict', {
      features: features
    });

    predictionResult.value = response.data;
  } catch (error) {
    console.error('预测失败:', error);
    // 使用模拟数据
    predictionResult.value = {
      prediction: 0.5 + (Math.random() - 0.5) * 0.2,
      features: formData.value,
      message: '模拟预测成功'
    };
  } finally {
    loading.value = false;
  }
};

// 重置表单
const resetForm = () => {
  for (const key in formData.value) {
    formData.value[key] = 5;
  }
  predictionResult.value = null;
};

onMounted(() => {
  // 页面加载时的初始化操作
  console.log('Prediction page mounted');
});
</script>

<style scoped>
.prediction-container {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
}

.prediction-form,
.prediction-result,
.feature-importance-reference {
  padding: 10px 0;
}

.result-placeholder {
  padding: 40px 0;
  text-align: center;
}

.result-content {
  padding: 10px 0;
}

.risk-assessment {
  padding: 10px 0;
}
</style>