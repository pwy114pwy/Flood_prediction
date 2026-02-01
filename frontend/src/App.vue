<template>
  <div id="app">
    <el-container style="min-height: 100vh">
      <!-- 侧边栏导航 -->
      <el-aside width="200px" style="background-color: #f0f2f5; border-right: 1px solid #e4e7ed">
        <div style="padding: 20px; font-size: 18px; font-weight: bold; color: #409EFF; text-align: center; border-bottom: 1px solid #e4e7ed">
          洪涝风险预测系统
        </div>
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          router
          @select="handleMenuSelect"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/explore">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据探索</span>
          </el-menu-item>
          <el-menu-item index="/model">
            <el-icon><Histogram /></el-icon>
            <span>模型评估</span>
          </el-menu-item>
          <el-menu-item index="/predict">
            <el-icon><MagicStick /></el-icon>
            <span>预测分析</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航栏 -->
        <el-header style="background-color: #fff; border-bottom: 1px solid #e4e7ed; display: flex; align-items: center; justify-content: space-between; padding: 0 20px">
          <div style="font-size: 16px; font-weight: bold; color: #303133">
            {{ pageTitle }}
          </div>
          <div>
            <el-button type="primary" size="small" @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
          </div>
        </el-header>
        
        <!-- 内容区域 -->
        <el-main style="padding: 20px">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { House, DataAnalysis, Histogram, MagicStick, Refresh } from '@element-plus/icons-vue';

const route = useRoute();
const activeMenu = ref('/');
const pageTitle = ref('首页');

// 页面标题映射
const titleMap = {
  '/': '首页',
  '/explore': '数据探索',
  '/model': '模型评估',
  '/predict': '预测分析'
};

// 处理菜单选择
const handleMenuSelect = (key) => {
  activeMenu.value = key;
  pageTitle.value = titleMap[key] || '首页';
};

// 刷新数据
const refreshData = () => {
  // 触发页面数据刷新
  window.location.reload();
};

// 监听路由变化
const updateTitle = () => {
  const path = route.path;
  activeMenu.value = path;
  pageTitle.value = titleMap[path] || '首页';
};

onMounted(() => {
  updateTitle();
});

// 监听路由变化
route.beforeEach = (to, from, next) => {
  updateTitle();
  next();
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background-color: #f5f7fa;
  color: #303133;
}

#app {
  width: 100%;
  height: 100vh;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

.el-header {
  height: 60px;
  line-height: 60px;
}

.el-main {
  background-color: #f5f7fa;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>