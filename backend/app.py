from flask import Flask, request, jsonify
import lightgbm as lgb
import numpy as np
import pickle
import os

app = Flask(__name__)
# 暂时注释CORS，后续安装依赖后再启用
from flask_cors import CORS
CORS(app)  # 启用CORS支持

# 加载模型和特征列
model_path = 'd:\\Flood_prediction\\models\\lightgbm_model.txt'
feature_columns_path = 'd:\\Flood_prediction\\models\\feature_columns.pkl'

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
        # 获取特征重要性
        importance = model.feature_importance(importance_type='split')
        feature_importance = list(zip(feature_columns, importance))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        # 构建特征重要性字典
        importance_dict = {}
        for feature, imp in feature_importance:
            importance_dict[feature] = int(imp)
        
        return jsonify({
            "model": "LightGBM Regressor",
            "features": feature_columns,
            "feature_importance": importance_dict,
            "message": "Model information retrieved successfully"
        })
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

# 主函数
if __name__ == '__main__':
    # 初始化模型
    if init_model():
        # 启动服务
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Failed to initialize model, exiting...")
        exit(1)