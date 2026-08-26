import httpx

url = "https://api.github.com/repos/zeus1660/Git_study"

try:
    response = httpx.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    print(data["full_name"])

except httpx.TimeoutException:
    print("请求超时，请稍后重试")

except httpx.HTTPStatusError as error:
    status_code = error.response.status_code
    print(f"HTTP 请求失败，状态码：{status_code}")

except httpx.RequestError:
    print("网络请求失败，请检查网络")