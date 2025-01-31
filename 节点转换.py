import base64
import time
import os

# 配置项
NODES_FILE = 'nodes.txt'
SUBSCRIPTION_PREFIX = 'vless://your-online-subscription-url#'  # 从网络获取的固定地址

def read_nodes():
    """读取节点数据文件，返回节点链接列表"""
    try:
        with open(NODES_FILE, 'r', encoding='utf-8') as f:
            nodes = [line.strip() for line in f if line.strip()]
        return nodes
    except FileNotFoundError:
        print("节点数据文件未找到。")
        return []

def generate_subscription(nodes):
    """生成VLESS订阅地址"""
    if not nodes:
        return None
    try:
        # 拼接节点链接
        concatenated = ','.join(nodes)
        # Base64编码
        base64_bytes = base64.b64encode(concatenated.encode('utf-8'))
        base64_string = base64_bytes.decode('utf-8')
        # 使用配置中的固定订阅地址前缀
        subscription_url = SUBSCRIPTION_PREFIX + base64_string
        return subscription_url
    except Exception as e:
        print(f"生成订阅地址时出错: {e}")
        return None

def update_subscription():
    """更新订阅地址文件"""
    nodes = read_nodes()
    subscription_url = generate_subscription(nodes)
    if subscription_url:
        # 写入到订阅地址文件
        with open('subscription.txt', 'w', encoding='utf-8') as f:
            f.write(subscription_url)
        print("订阅地址已更新。")
    else:
        print("未能生成订阅地址。")

# 自动更新订阅地址，每隔5分钟检查一次节点文件是否有变化
last_hash = None
while True:
    # 计算当前节点文件的哈希，判断是否有变化
    current_hash = os.stat(NODES_FILE).st_mtime if os.path.exists(NODES_FILE) else None
    if current_hash != last_hash:
        last_hash = current_hash
        update_subscription()
    time.sleep(300)  # 每5分钟检查一次
