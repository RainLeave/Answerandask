import pandas as pd
from sqlalchemy import create_engine
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from generate_sample_data import generate_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def load_documents(directory):
    texts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                texts.append(content)
    return texts

# 生成样本数据
data = generate_data()

# 创建 sample_docs 目录
if not os.path.exists('sample_docs'):
    os.makedirs('sample_docs')

# 将样本数据转换为文档并保存到 sample_docs 目录
for i, row in data.iterrows():
    doc_content = f"产品名称: {row['product_name']}\n品牌: {row['brand']}\n产品类型: {row['product_type']}\n特点: {row['features']}\n问题: {row['question']}\n答案: {row['answer']}"
    doc_filename = os.path.join('sample_docs', f'doc_{i}.txt')
    with open(doc_filename, 'w', encoding='utf-8') as f:
        f.write(doc_content)

# 文档预处理和索引构建部分
# 加载样本文档
texts = load_documents('sample_docs')

# 文本向量化
vectorizer = TfidfVectorizer()
document_vectors = vectorizer.fit_transform(texts)

# 搭建问答系统部分
# 使用 ModelScope 加载 ChatGLM3-6B 模型
model_name = 'qwen/qwen-7b-chat'
llm_pipeline = pipeline(Tasks.text_generation, model=model_name)
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# 设计提示模板
prompt_template = "请根据以下文档内容回答问题：{context} 问题：{question}"
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# 创建 LLM 链
chain = LLMChain(llm=llm, prompt=prompt)

# 实现问答功能
def ask_question(question):
    # 将查询问题转换为向量
    question_vector = vectorizer.transform([question])
    # 计算查询向量与文档向量的相似度
    similarities = cosine_similarity(question_vector, document_vectors)
    # 找到最相关的文档索引
    most_similar_index = similarities.argmax()
    # 获取最相关的文档内容
    context = texts[most_similar_index]
    # 使用 LLM 链生成答案
    answer = chain.run(context=context, question=question)
    return answer

# 示例调用
if __name__ == "__main__":
    question = "Apple Smartphone 1 的电池续航是多久？"
    answer = ask_question(question)
    print(f"问题: {question}")
    print(f"答案: {answer}")