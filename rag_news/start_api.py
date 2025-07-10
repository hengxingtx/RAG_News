#!/usr/bin/env python
"""
RAG News API启动器
此脚本用于简化API服务器的启动
"""

import os
import sys
import socket
from pathlib import Path

# 确保当前脚本的目录被添加到Python路径
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir.parent))

# 尝试导入必要的依赖，如果找不到则提示安装
try:
    import fastapi
    import uvicorn
    from sqlalchemy import create_engine
    from jose import jwt
    import bcrypt
except ImportError as e:
    print(f"导入依赖时出错: {e}")
    print("\n请先安装必要的依赖:")
    print("方法1: python -m rag_news.api.install_dependencies")
    print(
        '方法2: pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]" bcrypt python-multipart'
    )
    sys.exit(1)


def is_port_in_use(port, host='127.0.0.1'):
    """检查指定端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True


def find_available_port(start_port=8001, max_port=8100):
    """查找可用端口，从start_port开始，最大到max_port"""
    for port in range(start_port, max_port):
        if not is_port_in_use(port):
            return port
    return None


def start_server(host="127.0.0.1", port=8001, reload=True, auto_port=True):
    """启动API服务器"""
    try:
        # 检查端口是否被占用
        if is_port_in_use(port, host):
            if auto_port:
                # 自动寻找可用端口
                new_port = find_available_port(port + 1)
                if new_port:
                    print(f"端口 {port} 已被占用，自动切换到端口 {new_port}")
                    port = new_port
                else:
                    print(f"错误: 在端口范围内未找到可用端口，请手动指定其他端口。")
                    sys.exit(1)
            else:
                print(f"错误: 端口 {port} 已被占用，请尝试使用其他端口，例如：--port 8001")
                sys.exit(1)
                
        print(f"正在启动RAG News API服务器，地址: http://{host}:{port}")
        # 导入app对象
        from rag_news.api.server import app

        # 启动服务器
        uvicorn.run("rag_news.api.server:app", host=host, port=port, reload=reload)
    except Exception as e:
        print(f"启动服务器时出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 处理命令行参数
    import argparse

    parser = argparse.ArgumentParser(description="RAG News API服务器")
    parser.add_argument("--host", default="127.0.0.1", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8001, help="服务器端口")
    parser.add_argument(
        "--no-reload", action="store_false", dest="reload", help="禁用热重载"
    )
    parser.add_argument(
        "--no-auto-port", action="store_false", dest="auto_port", 
        help="禁用自动端口查找（如果指定端口被占用）"
    )

    args = parser.parse_args()
    start_server(host=args.host, port=args.port, reload=args.reload, auto_port=args.auto_port)
