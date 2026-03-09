#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试用例
"""

import pytest
from pathlib import Path
import sys

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import Config
from src.utils.database import Database


class TestConfig:
    """配置模块测试"""
    
    def test_config_load(self, tmp_path):
        """测试配置加载"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
user:
  phone: "13800138000"
  name: "测试用户"
""")
        
        config = Config(config_file)
        assert config.get("user.phone") == "13800138000"
        assert config.get("user.name") == "测试用户"
    
    def test_config_get_nested(self, tmp_path):
        """测试嵌套配置获取"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
user:
  location:
    city: "北京市"
    latitude: 39.9042
""")
        
        config = Config(config_file)
        assert config.get("user.location.city") == "北京市"
        assert config.get("user.location.latitude") == 39.9042
    
    def test_config_get_default(self, tmp_path):
        """测试默认值"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
user:
  phone: "13800138000"
""")
        
        config = Config(config_file)
        assert config.get("user.name", "默认名") == "默认名"


class TestDatabase:
    """数据库模块测试"""
    
    def test_database_init(self, tmp_path):
        """测试数据库初始化"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(f"""
database:
  path: "{tmp_path / 'test.db'}"
""")
        
        from src.utils.config import Config
        config = Config(config_file)
        db = Database(config)
        db.init_tables()
        
        assert db.db_path.exists()
    
    def test_database_user_crud(self, tmp_path):
        """测试用户 CRUD 操作"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(f"""
database:
  path: "{tmp_path / 'test.db'}"
""")
        
        from src.utils.config import Config
        config = Config(config_file)
        db = Database(config)
        db.init_tables()
        
        # 添加用户
        user_id = db.add_user("13800138000", "测试用户")
        assert user_id > 0
        
        # 查询用户
        user = db.get_user_by_phone("13800138000")
        assert user is not None
        assert user["name"] == "测试用户"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
