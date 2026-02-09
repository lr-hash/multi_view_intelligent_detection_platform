import random
import numpy as np
from datetime import datetime

class DataCleaner:
    """数据清洗工具类"""
    
    @staticmethod
    def remove_outliers(values, threshold=3):
        """
        使用 Z-score 剔除异常值
        """
        if not values:
            return []
        
        arr = np.array(values)
        mean = np.mean(arr)
        std = np.std(arr)
        
        if std == 0:
            return list(arr)
            
        z_scores = (arr - mean) / std
        return list(arr[np.abs(z_scores) < threshold])

    @staticmethod
    def fill_missing_values(values, strategy='mean'):
        """
        填充缺失值
        """
        if not values:
            return []
            
        arr = np.array(values, dtype=float)
        mask = np.isnan(arr)
        
        if not np.any(mask):
            return list(arr)
            
        if strategy == 'mean':
            fill_val = np.nanmean(arr)
        else:
            fill_val = 0.0
            
        arr[mask] = fill_val
        return list(arr)

class CoordinateTransformer:
    """坐标转换工具类"""
    
    @staticmethod
    def local_to_global(x, y, z, offset_e=0, offset_n=0, offset_z=0):
        """
        本地坐标转大地坐标 (简单平移模型)
        """
        return x + offset_e, y + offset_n, z + offset_z

    @staticmethod
    def calculate_distance(p1, p2):
        """
        计算两点间欧域距离 (p1, p2 为 (x,y,z) 元组)
        """
        return np.sqrt(np.sum((np.array(p1) - np.array(p2))**2))

def validate_data(data, source):
    """
    5.2.1 数据完整性与合理性校验
    Placeholder for data validation logic.
    """
    print(f"SERVICE: Validating data from {source} (simulated).")
    # Simulate a small chance of failure for demonstration
    if random.random() < 0.05:
        return False, "Validation failed: random check."
    return True, "Data is valid."

def align_and_standardize(data):
    """
    5.2.2 数据时间对齐与空间标准化
    Placeholder for alignment and standardization logic.
    """
    print(f"SERVICE: Aligning and standardizing data (simulated).")
    # In a real scenario, this would involve interpolation, coordinate transformation, etc.
    data['standardized'] = True
    data['aligned_timestamp'] = data.get('timestamp', 'N/A')
    return data

def fuse_data(pressure_data, seismic_data, deformation_data):
    """
    5.2.3 多元数据融合算法 - 顶板稳定性指数计算
    融合矿压 (pressure), 微震 (seismic), 变形 (deformation) 三方指标。
    返回 0-100 的评分，分数越低表示越危险。
    """
    # 权重定义 (示例)
    W_P = 0.4  # 矿压权重
    W_S = 0.35 # 微震权重
    W_D = 0.25 # 变形权重
    
    # 1. 矿压评分 (假设正常 20-30MPa, 超过 40 为危险)
    p_score = 100
    if pressure_data > 0:
        p_score = max(0, 100 - (max(0, pressure_data - 25) * 5))
        
    # 2. 微震评分 (假设单次能量 > 10^5J 为危险)
    s_score = 100
    if seismic_data > 0:
        s_score = max(0, 100 - (np.log10(max(1, seismic_data)) - 3) * 20)
        
    # 3. 变形评分 (假设速率 > 10mm/d 为危险)
    d_score = 100
    if deformation_data > 0:
        d_score = max(0, 100 - (deformation_data * 8))
        
    final_score = (p_score * W_P) + (s_score * W_S) + (d_score * W_D)
    
    risk_level = "Green"
    if final_score < 40:
        risk_level = "Red"
    elif final_score < 70:
        risk_level = "Yellow"
        
    return {
        "stability_score": round(final_score, 2),
        "risk_level": risk_level,
        "components": {
            "pressure": round(p_score, 2),
            "seismic": round(s_score, 2),
            "deformation": round(d_score, 2)
        },
        "timestamp": datetime.utcnow().isoformat()
    }
