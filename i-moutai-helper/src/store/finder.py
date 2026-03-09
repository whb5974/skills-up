#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
门店查询模块
"""

import requests
from typing import List, Dict, Optional
from loguru import logger


class StoreFinder:
    """门店查询类"""
    
    def __init__(self, config):
        """
        初始化门店查询器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.api_key = config.get("store.amap_api_key", "")
        self.max_distance = config.get("store.max_distance", 10.0)
        self.location = config.get("user.location", {})
    
    def find_nearby(self, max_distance: Optional[float] = None) -> List[Dict]:
        """
        查找附近门店
        
        Args:
            max_distance: 最大距离 (公里)
            
        Returns:
            门店列表
        """
        if max_distance is None:
            max_distance = self.max_distance
        
        # 如果有高德 API Key，调用高德 API
        if self.api_key:
            return self._find_by_amap(max_distance)
        
        # 否则返回示例数据
        logger.warning("⚠️ 未配置高德 API Key，返回示例数据")
        return self._get_sample_stores(max_distance)
    
    def _find_by_amap(self, max_distance: float) -> List[Dict]:
        """通过高德地图 API 查找门店"""
        latitude = self.location.get("latitude", 39.9042)
        longitude = self.location.get("longitude", 116.4074)
        
        url = "https://restapi.amap.com/v3/place/text"
        params = {
            "key": self.api_key,
            "keywords": "茅台专卖店",
            "location": f"{longitude},{latitude}",
            "radius": int(max_distance * 1000),
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if result.get("status") == "1":
                stores = []
                for poi in result.get("pois", []):
                    store = {
                        "store_id": poi.get("id", ""),
                        "name": poi.get("name", ""),
                        "address": poi.get("address", ""),
                        "phone": poi.get("tel", ""),
                        "latitude": float(poi.get("location", ",").split(",")[1]) if poi.get("location") else 0,
                        "longitude": float(poi.get("location", ",").split(",")[0]) if poi.get("location") else 0,
                        "distance": float(poi.get("distance", 0)) / 1000,  # 转换为公里
                        "competition_level": self._calculate_competition(poi.get("distance", 0))
                    }
                    stores.append(store)
                
                logger.info(f"✅ 找到 {len(stores)} 家附近门店")
                return stores
            else:
                logger.error(f"❌ 高德 API 返回错误：{result.get('info')}")
                return []
        except Exception as e:
            logger.error(f"❌ 高德 API 请求失败：{e}")
            return []
    
    def _get_sample_stores(self, max_distance: float) -> List[Dict]:
        """返回示例门店数据"""
        return [
            {
                "store_id": "store_001",
                "name": "茅台专卖店 (朝阳店)",
                "address": "北京市朝阳区 XX 路 XX 号",
                "phone": "010-12345678",
                "latitude": 39.9219,
                "longitude": 116.4431,
                "distance": 3.5,
                "competition_level": "中"
            },
            {
                "store_id": "store_002",
                "name": "茅台专卖店 (海淀店)",
                "address": "北京市海淀区 XX 路 XX 号",
                "phone": "010-87654321",
                "latitude": 39.9590,
                "longitude": 116.2982,
                "distance": 8.2,
                "competition_level": "高"
            },
            {
                "store_id": "store_003",
                "name": "茅台专卖店 (东城店)",
                "address": "北京市东城区 XX 街 XX 号",
                "phone": "010-11112222",
                "latitude": 39.9289,
                "longitude": 116.4169,
                "distance": 2.1,
                "competition_level": "低"
            }
        ]
    
    def _calculate_competition(self, distance: float) -> str:
        """
        计算竞争等级
        
        Args:
            distance: 距离 (米)
            
        Returns:
            竞争等级 (低/中/高)
        """
        # 简单规则：距离越远竞争越小
        if distance > 5000:
            return "低"
        elif distance > 2000:
            return "中"
        else:
            return "高"
    
    def get_store_by_id(self, store_id: str) -> Optional[Dict]:
        """
        根据 ID 获取门店详情
        
        Args:
            store_id: 门店 ID
            
        Returns:
            门店信息
        """
        stores = self.find_nearby()
        for store in stores:
            if store["store_id"] == store_id:
                return store
        return None
    
    def get_recommend_stores(self, limit: int = 3) -> List[Dict]:
        """
        获取推荐门店 (竞争较小的门店)
        
        Args:
            limit: 返回数量
            
        Returns:
            推荐门店列表
        """
        stores = self.find_nearby()
        
        # 按竞争等级排序 (低 > 中 > 高)
        competition_order = {"低": 0, "中": 1, "高": 2}
        stores.sort(key=lambda x: competition_order.get(x.get("competition_level", "中"), 1))
        
        return stores[:limit]
