import urllib.request
import json
import os

# 你的 Google Scholar ID
author_id = "-bCjtakAAAAJ"
# 从 GitHub 密码箱里读取 API Key
api_key = os.environ.get("SERPAPI_KEY")

if not api_key:
    print("错误: 找不到 SERPAPI_KEY，请检查 GitHub Secrets 设置！")
    exit(1)

# 构建 SerpApi 的请求链接
url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={author_id}&api_key={api_key}"

try:
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(response)
    
    # 精准提取总引用量
    total_citations = data.get("cited_by", {}).get("table", [])[0].get("citations", {}).get("all")
    
    if total_citations is not None:
        print(f"成功通过 SerpApi 抓取到最新引用量: {total_citations}")
        
        # 强制保存在 public 文件夹下，供 Astro 框架打包
        out_dir = "public"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        out_file = os.path.join(out_dir, "citations.json")
        
        with open(out_file, 'w') as f:
            json.dump({"citations": total_citations}, f)
    else:
        print("抓取失败：未找到引用量数据，请检查 API 响应")
        
except Exception as e:
    print(f"网络请求失败: {e}")
    exit(1)