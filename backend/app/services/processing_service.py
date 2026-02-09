import random
import numpy as np

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

def fuse_data(data_streams):
    """
    5.2.3 多元数据融合算法
    Placeholder for data fusion logic.
    """
    print(f"SERVICE: Fusing multiple data streams (simulated).")
    # This would implement the weighted fusion algorithm described in the document.
    fusion_score = random.uniform(0, 1)
    return {
        "raw_fusion_score": fusion_score,
        "risk_level": "Low" if fusion_score < 0.6 else "High"
    }
