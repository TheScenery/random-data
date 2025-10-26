import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_shopping_data(user_data_file, num_rows=20000):
    """生成购物记录数据，引用用户数据"""
    
    # 读取用户数据
    print("正在读取用户数据...")
    users_df = pd.read_excel(user_data_file)
    user_ids = users_df['用户ID'].tolist()
    
    # 初始化Faker
    fake = Faker('zh_CN')
    
    # 商品类别和商品数据
    categories = {
        '电子产品': ['智能手机', '笔记本电脑', '平板电脑', '智能手表', '耳机', '相机', '游戏机'],
        '家用电器': ['冰箱', '洗衣机', '空调', '电视', '微波炉', '吸尘器', '电饭煲'],
        '服装鞋帽': ['T恤', '牛仔裤', '连衣裙', '运动鞋', '衬衫', '外套', '包包'],
        '美妆护肤': ['面霜', '口红', '香水', '面膜', '精华液', '洗发水', '沐浴露'],
        '食品饮料': ['牛奶', '面包', '零食', '饮料', '水果', '方便面', '巧克力'],
        '家居用品': ['床上用品', '厨具', '收纳箱', '装饰品', '灯具', '桌椅', '清洁用品'],
        '运动户外': ['跑步机', '瑜伽垫', '登山鞋', '帐篷', '自行车', '泳衣', '健身器材']
    }
    
    # 支付方式
    payment_methods = ['支付宝', '微信支付', '信用卡', '银行卡', '花呗', '白条']
    
    # 订单状态
    order_statuses = ['已完成', '已发货', '待发货', '已取消', '退款中']
    
    data = []
    
    print("正在生成购物记录数据...")
    for i in range(num_rows):
        # 随机选择一个用户
        user_id = random.choice(user_ids)
        
        # 随机选择商品类别和商品
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        # 生成价格（符合商品类别的合理范围）
        base_prices = {
            '电子产品': (500, 10000),
            '家用电器': (300, 8000),
            '服装鞋帽': (50, 2000),
            '美妆护肤': (30, 1500),
            '食品饮料': (5, 200),
            '家居用品': (20, 3000),
            '运动户外': (100, 5000)
        }
        min_price, max_price = base_prices[category]
        price = round(random.uniform(min_price, max_price), 2)
        quantity = random.randint(1, 5)
        total_amount = round(price * quantity, 2)
        
        # 生成订单时间（基于用户的注册时间）
        user_data = users_df[users_df['用户ID'] == user_id].iloc[0]
        register_date = user_data['注册时间']
        if isinstance(register_date, str):
            register_date = datetime.strptime(register_date, '%Y-%m-%d %H:%M:%S')
        
        # 订单时间在注册时间之后
        days_after_register = random.randint(1, 365*2)  # 注册后2年内
        order_date = register_date + timedelta(days=days_after_register)
        
        order = {
            '订单ID': f'ORDER_{i+1:08d}',
            '用户ID': user_id,
            '商品名称': product,
            '商品类别': category,
            '单价': price,
            '数量': quantity,
            '总金额': total_amount,
            '订单时间': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            '支付方式': random.choice(payment_methods),
            '订单状态': random.choice(order_statuses),
            '收货地址': user_data['地址'],
            '是否使用优惠券': random.choice([True, False]),
            '优惠金额': round(random.uniform(0, min(50, total_amount*0.3)), 2) if random.random() > 0.7 else 0,
            '物流公司': random.choice(['顺丰速运', '圆通快递', '中通快递', '韵达快递', '京东物流', 'EMS']),
            '物流单号': f'SF{random.randint(1000000000, 9999999999)}'
        }
        data.append(order)
    
    return pd.DataFrame(data)

# 主程序
if __name__ == "__main__":
    # 用户数据文件路径（请确保路径正确）
    user_file = "用户基本信息_20000行.xlsx"  # 修改为您的实际文件路径
    
    try:
        # 生成购物记录数据
        print("开始生成购物记录数据...")
        shopping_df = generate_shopping_data(user_file, 20000)
        
        # 显示数据预览
        print("\n购物记录数据预览:")
        print(shopping_df.head())
        
        # 显示数据统计信息
        print(f"\n📊 数据概览:")
        print(f"总订单数: {len(shopping_df)}")
        print(f"总用户数: {shopping_df['用户ID'].nunique()}")
        print(f"总销售额: {shopping_df['总金额'].sum():.2f}元")
        print(f"平均订单金额: {shopping_df['总金额'].mean():.2f}元")
        
        # 按类别统计
        print(f"\n📈 商品类别分布:")
        category_stats = shopping_df.groupby('商品类别').agg({
            '订单ID': 'count',
            '总金额': 'sum'
        }).rename(columns={'订单ID': '订单数量', '总金额': '销售总额'})
        print(category_stats)
        
        # 保存为Excel文件
        output_file = "用户购物记录_20000行.xlsx"
        shopping_df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"\n✅ 购物记录Excel文件已生成: {output_file}")
        print(f"📁 文件包含: {len(shopping_df)} 行订单记录")
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到用户数据文件 '{user_file}'")
        print("请确保用户数据文件存在，或修改文件路径")
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")