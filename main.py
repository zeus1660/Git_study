import json
import requests

url = "https://api.github.com/repos/python/cpython"

response = requests.get(url, timeout=10)
response.raise_for_status()

data = response.json()
result = {
    "name": data["full_name"],
    "description": data["description"],
    "branch": data["default_branch"],
}
with open("repo.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)

print("已保存到 repo.json")