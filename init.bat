@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 正在启动MCP服务...
docker-compose up --build

pause