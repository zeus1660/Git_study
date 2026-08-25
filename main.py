import json
import requests


def get_repository(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()

repo_name = input("请输入仓库，例如 microsoft/vscode：")

try:
    data = get_repository(repo_name)
except requests.HTTPError:
    print("仓库不存在，或你没有访问权限")
except requests.RequestException:
    print("网络请求失败，请检查网络")
else:
    result = {
        "name": data["full_name"],
        "description": data["description"],
        "branch": data["default_branch"],
    }

    with open("repo.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    print("结果已保存到 repo.json")