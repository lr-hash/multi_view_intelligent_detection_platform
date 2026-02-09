import random
from datetime import datetime, timedelta

def get_comparison_data(borehole_id, data_type):
    """
    5.4.1 数据对比分析
    Retrieves pre- and post-fracturing data for comparison.
    """
    print(f"SERVICE: Retrieving {data_type} comparison data for borehole {borehole_id} (simulated).")
    # Simulate fetching data from a month before and after a fictional fracturing date
    fracturing_date = datetime.utcnow() - timedelta(days=15)
    
    if data_type == 'pressure':
        return {
            "pre_fracturing": {"max": 45.2, "avg": 35.1, "fluctuation": 0.15},
            "post_fracturing": {"max": 38.5, "avg": 31.2, "fluctuation": 0.08}
        }
    elif data_type == 'microseismic':
        return {
            "pre_fracturing": {"count": 50, "total_energy": 5e4},
            "post_fracturing": {"count": 120, "total_energy": 8e4} # Expected to increase
        }
    elif data_type == 'deformation':
        return {
            "pre_fracturing": {"max_rate": 15, "total": 200},
            "post_fracturing": {"max_rate": 5, "total": 50}
        }
    return {}

def calculate_evaluation_indices(borehole_id):
    """
    5.4.2 评价指标计算
    Calculates various evaluation indices.
    """
    print(f"SERVICE: Calculating evaluation indices for borehole {borehole_id} (simulated).")
    return {
        "roof_stability_index": {"value": random.randint(75, 95), "level": "稳定"},
        "fracturing_efficiency": {"value": random.randint(30, 80), "unit": "%", "level": "有效"},
        "pressure_control_effect": {"value": random.randint(60, 90), "level": "良好"}
    }

def generate_evaluation_report(borehole_id):
    """
    5.4.3 评价报告生成
    Generates a full evaluation report.
    """
    print(f"SERVICE: Generating evaluation report for borehole {borehole_id} (simulated).")
    
    comparison = {
        "pressure": get_comparison_data(borehole_id, "pressure"),
        "microseismic": get_comparison_data(borehole_id, "microseismic"),
        "deformation": get_comparison_data(borehole_id, "deformation")
    }
    indices = calculate_evaluation_indices(borehole_id)

    return {
        "report_title": f"钻孔 #{borehole_id} 压裂效果评价报告",
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "conclusion": "压裂效果良好，有效降低了顶板压力，巷道变形得到控制。",
            "recommendation": "建议在下一区域继续采用此压裂方案。"
        },
        "data_comparison": comparison,
        "evaluation_indices": indices
    }

def calculate_evaluation_metrics(borehole_id):
    """
    研发评价算法核心逻辑：量化计算压裂有效率和顶板稳定性。
    """
    # 获取对比数据 (模拟)
    p_data = get_comparison_data(borehole_id, 'pressure')
    d_data = get_comparison_data(borehole_id, 'deformation')
    
    # 1. 矿压降低率 (Pressure Reduction Rate)
    p_pre = p_data['pre_fracturing']['avg']
    p_post = p_data['post_fracturing']['avg']
    p_reduction = (p_pre - p_post) / p_pre if p_pre > 0 else 0
    
    # 2. 变形控制率 (Deformation Control Rate)
    d_pre = d_data['pre_fracturing']['max_rate']
    d_post = d_data['post_fracturing']['max_rate']
    d_control = (d_pre - d_post) / d_pre if d_pre > 0 else 0
    
    # 3. 压裂有效率 (综合评分)
    # 权重：压力 0.6, 变形 0.4
    eff_value = (p_reduction * 0.6 + d_control * 0.4) * 100
    eff_value = max(0, min(100, eff_value + 50)) # 基础分 50
    
    # 4. 稳定性指数 (基于残余压力和变形)
    stability = 100 - (p_post * 1.5 + d_post * 2)
    stability = max(0, min(100, stability))
    
    return {
        "borehole_id": borehole_id,
        "metrics": {
            "pressure_reduction": round(p_reduction * 100, 2),
            "deformation_control": round(d_control * 100, 2),
            "efficiency": round(eff_value, 2),
            "stability_index": round(stability, 2)
        },
        "level": "稳定" if stability > 70 else ("一般" if stability > 40 else "危险")
    }
