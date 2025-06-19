import subprocess
import sys

def install_dependencies():
    """安装所有必要的依赖"""
    dependencies = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-jose[cryptography]",
        "bcrypt",
        "python-multipart"
    ]
    
    print("准备安装所需依赖...")
    
    for dep in dependencies:
        print(f"正在安装 {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"{dep} 安装成功!")
        except subprocess.CalledProcessError:
            print(f"安装 {dep} 失败，请手动安装。")
    
    print("\n所有依赖安装完成！现在可以运行服务器。")
    print("启动命令: python -m rag_news.api.server")

if __name__ == "__main__":
    install_dependencies() 