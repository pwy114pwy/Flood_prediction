import { createRouter, createWebHistory } from 'vue-router';

// 导入页面组件
const Home = () => import('../views/Home.vue');
const DataExplore = () => import('../views/DataExplore.vue');
const ModelEvaluation = () => import('../views/ModelEvaluation.vue');
const Prediction = () => import('../views/Prediction.vue');

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  {
    path: '/explore',
    name: 'DataExplore',
    component: DataExplore,
    meta: {
      title: '数据探索'
    }
  },
  {
    path: '/model',
    name: 'ModelEvaluation',
    component: ModelEvaluation,
    meta: {
      title: '模型评估'
    }
  },
  {
    path: '/predict',
    name: 'Prediction',
    component: Prediction,
    meta: {
      title: '预测分析'
    }
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
});

// 全局前置守卫，设置页面标题
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 洪涝风险预测系统` : '洪涝风险预测系统';
  next();
});

export default router;