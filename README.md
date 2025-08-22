# 八字排盘工具

这是一个基于Python的八字辅助工具，可以计算八字、节气信息和大运信息。

## 功能特性

- 八字计算（年柱、月柱、日柱、时柱）
- 真太阳时校正
- 节气信息计算
- 大运信息计算
- 农历转换
- 农历出生时间显示为真太阳时校正后的时间

## 安装依赖

```bash
pip install sxtwl mcp
```
or
```bash
pip install -r requirements.txt
```

## 启动MCP服务

### 使用Docker（推荐）
```bash
docker-compose up --build
```

默认情况下，服务将在 `http://localhost:8001/mcp` 上运行。

如果从宿主机访问Docker容器中的服务，使用以下地址：
- Windows/Linux/macOS: `http://host.docker.internal:8001/mcp`

### 直接运行
```bash
python mcp_server.py
```

默认情况下，服务将在 `http://localhost:8001/mcp` 上运行。

### 连接问题排查
如果遇到503 Service Unavailable错误，请注意：
1. MCP服务需要使用Model Context Protocol客户端连接，不能直接通过浏览器或普通HTTP请求访问
2. 确保客户端支持MCP协议并正确配置连接参数
3. 服务正常启动后会显示"Uvicorn running on http://0.0.0.0:8001"
4. 如果在Docker容器中运行，请使用`host.docker.internal`而不是`localhost`从宿主机访问

### MCP客户端调用

MCP服务提供了一个名为 `bazi` 的工具，可以计算八字信息。该工具接受以下参数：

- `name` (str): 姓名
- `gender` (str): 性别 ('男' 或 '女')
- `calendar` (str): 日历类型 ('公历' 或 '农历')
- `year` (int): 出生年份
- `month` (int): 出生月份
- `day` (int): 出生日期
- `hour` (int): 出生小时 (0-23)
- `minute` (int): 出生分钟 (0-59)
- `birth_city` (str): 出生城市
- `current_city` (str, 可选): 当前居住城市

## 项目结构

```
bazi/ 
├── mcp_server.py         # MCP服务端
├── bazi_tool.py          # 八字计算工具
├── query_longitude.py    # 查询经度
├── region.json           # 城市经纬度数据   
├── README.md             # 项目说明

```

## 示例输出

```
=== 张三的八字信息 ===
姓名：张三
性别：男 (乾造)
出生时间：
  公历：[年份]年[月份]月[日期]日[小时]:[分钟]
  农历：[年份]年[月份]月[日期]日[小时]:[分钟] (非闰月)
出生城市：[城市名]([经度]°E)
现居城市：[城市名]
八字信息：[年柱] [月柱] [日柱] [时柱]
节气信息：生于[节气1]节气后[天数]天，[节气2]节气前[天数]天
大运信息：[阴阳]男，[顺排/逆排]，起运时间[年数]年[月数]月，[起运年龄]岁起运
```