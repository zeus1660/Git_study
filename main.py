import json
import requests
import os





def get_repository(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"
    api_key = os.getenv("GITHUB_TOKEN")
    print("认证状态：", "已使用 Token" if api_key else "未使用 Token")
    headers = {}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.get(
        url,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()

    return response.json()

def save_result(data, filename="repo.json"):
    result = {
        "name": data["full_name"],
        "description": data.get("description") or "无描述",
        "branch": data["default_branch"],
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)



def main():
    repo_name = input("请输入仓库，例如 microsoft/vscode：")

    try:
        data = get_repository(repo_name)

    except requests.Timeout:
        print("请求超时，请稍后重试")

    except requests.HTTPError as error:
        status_code = error.response.status_code

        if status_code == 404:
            print("仓库不存在")
        elif status_code == 401:
            print("身份认证失败")
        elif status_code == 403:
            print("没有访问权限，或请求次数受限")
        else:
            print(f"HTTP 请求失败，状态码：{status_code}")

    except requests.exceptions.JSONDecodeError:
        print("服务器返回的内容不是有效 JSON")
    except requests.RequestException:
        print("网络请求失败，请检查网络")
    else:
        save_result(data)
        print("结果已保存到 repo.json")

if __name__ == "__main__":
    main()