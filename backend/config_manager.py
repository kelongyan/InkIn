import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

DEFAULT_CONFIG = {
    'api_key': '',
    'base_url': 'https://api.openai.com/v1',
    'model': 'gpt-4o',
}


def get_config():
    """读取配置，不存在则返回默认配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置，确保所有字段存在
                return {**DEFAULT_CONFIG, **config}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置到文件"""
    # 只保留允许的字段
    valid_keys = set(DEFAULT_CONFIG.keys())
    filtered = {k: v for k, v in config.items() if k in valid_keys}
    merged = {**DEFAULT_CONFIG, **filtered}

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    return merged
