# （RHParse）Raw HTTP Parse 原始HTTP数据包解析器

`Raw HTTP Parse` 是一个简单易用的 Python 库，用于将原始 HTTP 数据包解析为 `requests.Request` 对象，以及将 `requests.Response` 对象格式化为原始 HTTP 响应字符串。

## 安装
```bash
pip install rhparse
```

## 使用
```python
from rhparse import RHParse
import requests
# 解析原始 HTTP 请求
raw_request = """POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json

{"name": "张三"}
"""
request = RHParse.parse_request(raw_request)
print(request.url)  # 输出: http://example.com/api/users
print(request.data)  # 输出: {'name': '张三'}

# 使用requests库发起请求
session = requests.session()
res = session.send(request.prepare())
print(res.text)

# 格式化 HTTP 响应
import requests
response = requests.get("https://example.com")
raw_response = RHParse.format_response(response)
print(raw_response)  # 输出原始 HTTP 响应字符串
```

## 功能特点

- 支持常见的 HTTP 方法（GET、POST、PUT 等）
- 自动处理 Cookie 和 Authorization 头
- 支持 JSON 和表单格式的请求体
- 简洁的静态方法调用，无需实例化

## 许可证
MIT