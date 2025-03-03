from urllib.parse import urlparse, parse_qs
import json
import requests


class RHParse:
    """HTTP 数据包处理工具类，提供简洁的请求解析和响应格式化功能"""

    SUPPORTED_METHODS = {'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'}
    DEFAULT_SCHEME = 'http'

    @staticmethod
    def parse_request(http_packet: str, scheme: str = DEFAULT_SCHEME) -> requests.Request:
        """
        解析原始 HTTP 请求为 requests.Request 对象

        Args:
            http_packet (str): 原始 HTTP 请求字符串
            scheme (str): 默认协议 (http 或 https)，默认 'http'

        Returns:
            requests.Request: 解析后的 Request 对象

        Raises:
            ValueError: 如果数据包无效
        """
        try:
            lines = http_packet.split('\n')
            if not lines:
                raise ValueError("Empty HTTP packet")

            # 解析请求行
            parts = lines[0].strip().split()
            if len(parts) < 3:
                raise ValueError("Invalid request line")
            method, path, _ = parts[0].upper(), parts[1], parts[2]
            if method not in RHParse.SUPPORTED_METHODS:
                raise ValueError(f"Unsupported method: {method}")

            # 分离头部和正文
            headers = {}
            body_lines = []
            header_end = False
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    header_end = True
                    continue
                if not header_end and ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
                else:
                    body_lines.append(line)

            # 构造 URL
            host = headers.get('Host')
            if not host:
                raise ValueError("No Host header found")
            url = f"{scheme}://{host.split(':')[0]}{':' + host.split(':')[1] if ':' in host else ''}{path}"
            params = parse_qs(urlparse(url).query) if urlparse(url).query else None

            # 解析正文
            data = None
            if body_lines:
                body_content = '\n'.join(body_lines).strip()
                if body_content:
                    content_type = headers.get('Content-Type', '').lower()
                    if 'application/json' in content_type:
                        try:
                            data = json.loads(body_content)
                        except json.JSONDecodeError:
                            data = body_content
                    else:
                        data = body_content

            # 处理 Cookie 和 Authorization
            cookies = headers.pop('Cookie', None)
            cookie_dict = dict(pair.split('=', 1) for pair in cookies.split('; ')) if cookies else None
            auth = headers.pop('Authorization', None).split(' ', 1)[1] if headers.get('Authorization', '').lower().startswith('basic') else None

            return requests.Request(
                method=method,
                url=url,
                headers=headers,
                params=params if method == 'GET' else None,
                data=data if method in {'POST', 'PUT', 'PATCH'} else None,
                cookies=cookie_dict,
                auth=auth
            )
        except Exception as e:
            raise ValueError(f"Failed to parse HTTP packet: {str(e)}")

    @staticmethod
    def format_response(response: requests.Response) -> str:
        """
        将 requests.Response 格式化为原始 HTTP 响应字符串

        Args:
            response (requests.Response): Response 对象

        Returns:
            str: 原始 HTTP 响应字符串
        """
        status_line = f"HTTP/1.1 {response.status_code} {response.reason}\r\n"
        headers = '\r\n'.join(f"{k}: {v}" for k, v in response.headers.items()) + '\r\n\r\n'
        return status_line + headers + (response.text or '')