import pandas
import sqlalchemy
import llama_index
import langchain
import nltk

print(f"pandas 版本: {pandas.__version__}")
print(f"sqlalchemy 版本: {sqlalchemy.__version__}")

try:
    import llama_index
    # 尝试获取版本号
    try:
        llama_index_version = llama_index.__version__
    except AttributeError:
        # 如果没有 __version__ 属性，尝试通过其他方式获取版本
        import importlib.metadata
        try:
            llama_index_version = importlib.metadata.version('llama-index')
        except importlib.metadata.PackageNotFoundError:
            llama_index_version = "未找到版本信息"
except ImportError:
    llama_index_version = "未安装"


print(f"llama_index 版本: {llama_index_version}")
print(f"langchain 版本: {langchain.__version__}")
print(f"nltk 版本: {nltk.__version__}")
