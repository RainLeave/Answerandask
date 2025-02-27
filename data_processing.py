import pandas as pd
from sqlalchemy import create_engine
from generate_sample_data import generate_data

# 模拟数据收集，调用生成模拟数据的函数
data = generate_data()

# 提取关键信息，根据实际业务场景选择特定列
key_info = data[['product_name', 'brand', 'product_type', 'question', 'answer']]

# 创建 SQLite 数据库连接
engine = create_engine('sqlite:///doc_metadata.db')

# 将关键信息存储到数据库
key_info.to_sql('key_metadata', engine, if_exists='replace', index=False)

print("关键信息已成功存储到数据库。")