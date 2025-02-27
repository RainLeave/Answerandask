import pandas as pd
from sqlalchemy import create_engine
from llama_index.readers import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index import GPTVectorStoreIndex
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from generate_sample_data import generate_data

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
documents = SimpleDirectoryReader('sample_docs').load_data()

# 解析文档生成节点
parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(documents)

# 构建索引，使用默认的向量存储
index = GPTVectorStoreIndex(nodes)

# 搭建问答系统部分
# 加载 deepseek - coder 模型
# 这里需要根据实际情况配置模型路径等参数
# 注意："deepseek-coder" 应该替换为实际的模型 ID 或路径
llm = HuggingFacePipeline.from_model_id(
    model_id="deepseek-ai/deepseek-coder-6.7b-instruct",  # 替换为实际的模型 ID
    task="text-generation",
    device=0  # 使用 GPU
)

# 设计提示模板
prompt_template = "请根据以下文档内容回答问题：{context} 问题：{question}"
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# 创建 LLM 链
chain = LLMChain(llm=llm, prompt=prompt)

# 实现问答功能
def ask_question(question):
    query_engine = index.as_query_engine()
    result = query_engine.query(question)
    context = result.response
    answer = chain.run(context=context, question=question)
    return answer


# 示例调用
if __name__ == "__main__":
    question = "Apple Smartphone 1 的电池续航是多久？"
    answer = ask_question(question)
    print(f"问题: {question}")
    print(f"答案: {answer}")