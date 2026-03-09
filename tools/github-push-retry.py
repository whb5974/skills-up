#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 推送重试脚本
检查网络状态并尝试推送项目到 GitHub
"""

import subprocess
import sys
from datetime import datetime

PROJECT_PATH = "/home/ghost/.openclaw/workspace/dbp-automation"
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
GITHUB_REPO = f"https://{GITHUB_TOKEN}@github.com/whb5974/DBsecurity.git"

def check_network():
    """检查网络连接"""
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '5', 'github.com'],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

def try_push():
    """尝试推送到 GitHub"""
    log = []
    log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查 GitHub 推送...")
    
    # 检查网络
    log.append("检查网络连接...")
    if not check_network():
        log.append("❌ 网络连接失败，无法访问 GitHub")
        return False, log
    
    log.append("✅ 网络连接正常")
    
    # 检查 Git 状态
    try:
        result = subprocess.run(
            ['git', '-C', PROJECT_PATH, 'status', '--porcelain'],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            log.append("⚠️ 有未提交的更改")
        else:
            log.append("✅ 工作区干净")
    except Exception as e:
        log.append(f"❌ Git 状态检查失败：{e}")
        return False, log
    
    # 尝试推送
    log.append("尝试推送到 GitHub...")
    try:
        result = subprocess.run(
            ['git', '-C', PROJECT_PATH, 'push', 'origin', 'main', '--force'],
            capture_output=True, text=True, timeout=60,
            env={**subprocess.os.environ, 'GIT_ASKPASS': 'echo'}
        )
        
        if result.returncode == 0:
            log.append("✅ GitHub 推送成功！")
            log.append(result.stdout)
            return True, log
        else:
            log.append(f"❌ 推送失败：{result.stderr}")
            return False, log
    except subprocess.TimeoutExpired:
        log.append("❌ 推送超时")
        return False, log
    except Exception as e:
        log.append(f"❌ 推送异常：{e}")
        return False, log

if __name__ == "__main__":
    success, log = try_push()
    
    for line in log:
        print(line)
    
    sys.exit(0 if success else 1)
