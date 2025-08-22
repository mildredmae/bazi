import json
import re

def load_region_data():
    """
    加载region.json数据
    """
    with open('region.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def fuzzy_match(city_name, target_name):
    """
    模糊匹配城市名称
    """
    return re.search(city_name, target_name)

def inquire(birth_city):
    """
    根据输入的城市名称查询经度
    支持模糊查询，优先返回市级经度
    如果没有找到匹配项，返回默认经度120.0
    """
    data = load_region_data()
    
    # 存储匹配的结果
    matched_cities = []
    
    # 递归搜索函数
    def search_districts(districts):
        """
        递归搜索地区数据
        """
        for district in districts:
            # 检查当前地区名称是否匹配
            if fuzzy_match(birth_city, district['name']):
                matched_cities.append(district)
            
            # 递归搜索子地区
            if 'districts' in district and district['districts']:
                search_districts(district['districts'])
    
    # 开始搜索
    search_districts(data['districts'])
    
    # 如果没有匹配项，返回默认经度
    if not matched_cities:
        return 120.0
    
    # 优先选择市级数据
    for city in matched_cities:
        if city['level'] == 'city':
            return float(city['center']['longitude'])
    
    # 如果没有市级数据，选择省级数据
    for city in matched_cities:
        if city['level'] == 'province':
            return float(city['center']['longitude'])
    
    # 如果没有省市级数据，返回第一个匹配项的经度
    return float(matched_cities[0]['center']['longitude'])

# 主函数示例
if __name__ == "__main__":
    # 测试用例
    test_cities = ["广东","深圳", "北京市", "上海", "小榄", "广东惠州"]
    
    for city in test_cities:
        city_longitude = inquire(city)
        print(f"{city}的经度是: {city_longitude}")