from flask import Flask, request, jsonify
import lightgbm as lgb
import numpy as np
import pickle
import os
import json

app = Flask(__name__)
# 暂时注释CORS，后续安装依赖后再启用
from flask_cors import CORS
CORS(app)  # 启用CORS支持

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载模型和特征列
model_path = os.path.join(base_path, 'models', 'lightgbm_model.txt')
feature_columns_path = os.path.join(base_path, 'models', 'feature_columns.pkl')

# API数据路径
api_data_dir = os.path.join(base_path, 'api_data')

# 全局变量存储模型和特征列
model = None
feature_columns = None

# 初始化函数，加载模型和特征列
def init_model():
    """初始化模型和特征列"""
    global model, feature_columns
    
    try:
        # 加载模型
        model = lgb.Booster(model_file=model_path)
        print(f"模型加载成功: {model_path}")
        
        # 加载特征列
        with open(feature_columns_path, 'rb') as f:
            feature_columns = pickle.load(f)
        print(f"特征列加载成功: {feature_columns}")
        
        return True
    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        return False

# 健康检查接口
@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({"status": "ok", "message": "Flood Prediction API is running"})

# 模型信息接口
@app.route('/info', methods=['GET'])
def model_info():
    """返回模型信息和特征重要性"""
    try:
        with open(os.path.join(api_data_dir, 'model_info.json'), 'r', encoding='utf-8') as f:
            info = json.load(f)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 预测接口
@app.route('/predict', methods=['POST'])
def predict():
    """接收特征数据，返回预测结果"""
    try:
        # 获取请求数据
        data = request.json
        
        # 验证数据格式
        if not data or 'features' not in data:
            return jsonify({"error": "Invalid request format, 'features' key is required"}), 400
        
        # 提取特征数据
        features = data['features']
        
        # 验证特征数量
        if len(features) != len(feature_columns):
            return jsonify({"error": f"Invalid number of features. Expected {len(feature_columns)}, got {len(features)}"}), 400
        
        # 转换为numpy数组
        features_array = np.array(features).reshape(1, -1)
        
        # 进行预测
        prediction = model.predict(features_array)[0]
        
        # 构建响应
        response = {
            "prediction": float(prediction),
            "features": dict(zip(feature_columns, features)),
            "message": "Prediction completed successfully"
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 批量预测接口
@app.route('/predict/batch', methods=['POST'])
def batch_predict():
    """批量预测接口"""
    try:
        # 获取请求数据
        data = request.json
        
        # 验证数据格式
        if not data or 'batch_features' not in data:
            return jsonify({"error": "Invalid request format, 'batch_features' key is required"}), 400
        
        # 提取批量特征数据
        batch_features = data['batch_features']
        
        # 验证每个样本的特征数量
        for i, features in enumerate(batch_features):
            if len(features) != len(feature_columns):
                return jsonify({"error": f"Invalid number of features at index {i}. Expected {len(feature_columns)}, got {len(features)}"}), 400
        
        # 转换为numpy数组
        features_array = np.array(batch_features)
        
        # 进行批量预测
        predictions = model.predict(features_array)
        
        # 构建响应
        response = {
            "predictions": [float(pred) for pred in predictions],
            "batch_size": len(predictions),
            "message": "Batch prediction completed successfully"
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 数据统计接口
@app.route('/stats', methods=['GET'])
def get_stats():
    """获取数据统计信息"""
    try:
        with open(os.path.join(api_data_dir, 'stats.json'), 'r', encoding='utf-8') as f:
            stats = json.load(f)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 模型评估指标接口
@app.route('/evaluation', methods=['GET'])
def get_evaluation():
    """获取模型评估指标"""
    try:
        with open(os.path.join(api_data_dir, 'evaluation.json'), 'r', encoding='utf-8') as f:
            evaluation = json.load(f)
        return jsonify(evaluation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 数据分布接口
@app.route('/distribution', methods=['GET'])
def get_distribution():
    """获取目标变量分布"""
    try:
        with open(os.path.join(api_data_dir, 'distribution.json'), 'r', encoding='utf-8') as f:
            distribution = json.load(f)
        return jsonify(distribution)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 特征相关性接口
@app.route('/correlation', methods=['GET'])
def get_correlation():
    """获取特征相关性矩阵"""
    try:
        with open(os.path.join(api_data_dir, 'correlation.json'), 'r', encoding='utf-8') as f:
            correlation = json.load(f)
        return jsonify(correlation)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 预测结果对比接口
@app.route('/predictions-comparison', methods=['GET'])
def get_predictions_comparison():
    """获取预测值与真实值对比数据"""
    try:
        with open(os.path.join(api_data_dir, 'predictions_comparison.json'), 'r', encoding='utf-8') as f:
            comparison = json.load(f)
        return jsonify(comparison)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 预测误差分布接口
@app.route('/error-distribution', methods=['GET'])
def get_error_distribution():
    """获取预测误差分布"""
    try:
        with open(os.path.join(api_data_dir, 'error_distribution.json'), 'r', encoding='utf-8') as f:
            error_dist = json.load(f)
        return jsonify(error_dist)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 模型参数接口
@app.route('/model-params', methods=['GET'])
def get_model_params():
    """获取模型参数"""
    try:
        with open(os.path.join(api_data_dir, 'model_params.json'), 'r', encoding='utf-8') as f:
            params = json.load(f)
        return jsonify(params)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 训练信息接口
@app.route('/training-info', methods=['GET'])
def get_training_info():
    """获取训练信息"""
    try:
        with open(os.path.join(api_data_dir, 'training_info.json'), 'r', encoding='utf-8') as f:
            info = json.load(f)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# csv信息接口
@app.route('/csv-info', methods=['GET'])
def get_csv_info():
    """获取csv信息"""
    try:
        with open(os.path.join(api_data_dir, 'csv_info.json'), 'r', encoding='utf-8') as f:
            info = json.load(f)
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 训练曲线数据接口
@app.route('/training-curve', methods=['GET'])
def get_training_curve():
    """获取训练曲线数据"""
    try:
        with open(os.path.join(api_data_dir, 'training_curve.json'), 'r', encoding='utf-8') as f:
            curve_data = json.load(f)
        return jsonify(curve_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 主函数
if __name__ == '__main__':
    # 初始化模型
    if init_model():
        # 启动服务
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Failed to initialize model, exiting...")
        exit(1)