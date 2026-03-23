import urllib.request
import re
import json
import os

# 你的 Google Scholar 主页 URL (带有你的 user ID)
url = "https://scholar.google.com/citations?user=-bCjtakAAAAJ&hl=en"

# 伪装成浏览器访问，防止被 Google 拦截
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

try:
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8')

    # 用正则精准提取总引用量 (匹配 <td class="gsc_rsb_std"> 里的数字)
    citations = re.findall(r'<td class="gsc_rsb_std">([\d,]+)</td>', html)
    
    if citations:
        total_citations = citations[0] # 第一个数字就是总引用量
        print(f"成功抓取到最新引用量: {total_citations}")

        # 如果你是用 Astro 等框架，建议存入 public 文件夹；如果是纯静态单页，存根目录即可
        out_dir = "public" if os.path.exists("public") else "."
        out_file = os.path.join(out_dir, "citations.json")

        # 将数字写入 JSON 文件
        with open(out_file, 'w') as f:
            json.dump({"citations": total_citations}, f)
            
except Exception as e:
    print(f"抓取失败: {e}")