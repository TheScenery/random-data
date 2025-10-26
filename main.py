import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker
fake = Faker('zh_CN')  # 中文数据

def generate_user_data(num_rows=20000):
    """生成随机用户数据"""
    
    data = {
        # 基本信息
        '用户ID': [f'USER_{i:06d}' for i in range(1, num_rows + 1)],
        '姓名': [fake.name() for _ in range(num_rows)],
        '性别': [random.choice(['男', '女']) for _ in range(num_rows)],
        '年龄': [random.randint(18, 80) for _ in range(num_rows)],
        '出生日期': [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(num_rows)],
        
        # 联系信息
        '手机号': [fake.phone_number() for _ in range(num_rows)],
        '邮箱': [fake.email() for _ in range(num_rows)],
        '地址': [fake.address() for _ in range(num_rows)],
        
        # 其他信息
        '注册时间': [fake.date_time_between(start_date='-5y', end_date='now') for _ in range(num_rows)],
        '会员等级': [random.choice(['普通', '白银', '黄金', '铂金', '钻石']) for _ in range(num_rows)]
    }
    
    return pd.DataFrame(data)

# 生成数据
print("正在生成20000行用户数据...")
df = generate_user_data(20000)

# 显示前几行数据预览
print("\n数据预览:")
print(df.head())

# 显示数据基本信息
print("\n数据概览:")
print(f"总行数: {len(df)}")
print(f"总列数: {len(df.columns)}")
print("\n列名:", df.columns.tolist())

# 保存为Excel文件
output_file = "用户基本信息_20000行.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"\n✅ Excel文件已生成: {output_file}")
print(f"📊 文件包含: {len(df)} 行, {len(df.columns)} 列")