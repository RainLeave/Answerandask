import pandas as pd
import random
from sqlalchemy import create_engine

# 定义一些常见的科技产品品牌
brands = ["Apple", "Samsung", "Huawei", "Dell", "Lenovo", "HP"]

# 定义一些科技产品类型
product_types = ["Smartphone", "Laptop", "Tablet", "Smartwatch"]

# 定义一些产品特点
features = [
    "High-resolution display",
    "Powerful processor",
    "Long battery life",
    "Large storage capacity",
    "Waterproof design",
    "Ultra-thin body"
]

# 定义一些常见问题及对应的答案模板
questions = [
    "What is the battery life of this product?",
    "Does it support fast charging?",
    "What is the storage capacity?",
    "Is it waterproof?"
]

answers = [
    "It has a battery life of about {hours} hours.",
    "{support} support fast charging.",
    "It has a storage capacity of {capacity}GB.",
    "{waterproof} waterproof."
]


def generate_data(num_records=1000):
    data = {
        'product_name': [],
        'brand': [],
        'product_type': [],
        'features': [],
        'question': [],
        'answer': []
    }

    for _ in range(num_records):
        # 随机选择品牌和产品类型
        brand = random.choice(brands)
        product_type = random.choice(product_types)
        product_name = f"{brand} {product_type} {random.randint(1, 10)}"

        # 随机选择一些产品特点
        num_features = random.randint(1, 3)
        selected_features = random.sample(features, num_features)
        feature_str = ", ".join(selected_features)

        # 随机选择一个问题并生成对应的答案
        question = random.choice(questions)
        answer_index = questions.index(question)
        if answer_index == 0:
            hours = random.randint(8, 24)
            answer = answers[answer_index].format(hours=hours)
        elif answer_index == 1:
            support = "It does" if random.random() > 0.5 else "It does not"
            answer = answers[answer_index].format(support=support)
        elif answer_index == 2:
            capacity = random.choice([64, 128, 256, 512])
            answer = answers[answer_index].format(capacity=capacity)
        elif answer_index == 3:
            waterproof = "It is" if random.random() > 0.5 else "It is not"
            answer = answers[answer_index].format(waterproof=waterproof)

        data['product_name'].append(product_name)
        data['brand'].append(brand)
        data['product_type'].append(product_type)
        data['features'].append(feature_str)
        data['question'].append(question)
        data['answer'].append(answer)

    df = pd.DataFrame(data)
    return df


# 生成数据
key_info = generate_data()

# 创建 SQLite 数据库连接
engine = create_engine('sqlite:///doc_metadata.db')

# 将数据存入数据库
key_info.to_sql('document_metadata', engine, if_exists='replace', index=False)

print("数据已成功存入 SQLite 数据库。")