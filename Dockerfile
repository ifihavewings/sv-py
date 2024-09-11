# 使用 Python 3.12 的官方镜像
FROM python:3.12.4-slim

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 运行程序
CMD ["python", "app/main.py"]
