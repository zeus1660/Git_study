import os
import requests
import json




def get_repository(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"

    api_key=os.getenv("GITHUB_TOKEN")
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()
    return response.json()

def save_result(data,filename="final_result.json"):
    result={
        "name":data["full_name"],
        "description":data.get("description") or "无描述",
        "branch":data["default_branch"]


    }

    with open(filename,"w",encoding="utf-8") as file:
        json.dump(result,file,ensure_ascii=False,indent=2)


def main():
    repo_name = input("Enter repository name: ").strip()

    if not repo_name or "/" not in repo_name:
        print("格式错误，请使用 owner/repository")
        return

    try:
        data = get_repository(repo_name)
        save_result(data)
    except requests.HTTPError as error:
        status_code=error.response.status_code

        if status_code == 401:
            print("身份认证失败")
        elif status_code == 403:
            print("访问被拒绝或请求次数过多")
        elif status_code == 404:
            print("仓库不存在")
        else:
            print(f"请求失败，状态码：{status_code}")
    except requests.Timeout:
        print("请求超时，请稍后重试")
    except requests.RequestException as error:
        print(f"网络请求失败:{error}")
    except requests.exceptions.JSONDecodeError:
        print("服务器返回的内容不是有效 JSON")
    else:
        print("结果已保存到 final_result.json")
        print(data["full_name"])

if __name__ == "__main__":
    main()

