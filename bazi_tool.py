import sxtwl
import datetime
import math
from query_longitude import inquire

# 天干地支索引
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
     "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", 
     "立冬", "小雪", "大雪"]

ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", 
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", 
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]


class BaZiCalculator:
    def __init__(self, name, gender, calendar, year, month, day, hour, minute, birth_city, current_city=None):
        """
        初始化八字计算器
        """
        self.name = name
        self.gender = gender
        self.calendar = calendar
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.birth_city = birth_city
        self.current_city = current_city
        
        # 获取出生城市经度
        self.birth_longitude = inquire(birth_city)
        
        # 计算真太阳时
        self.solar_time = self.calculate_solar_time()
        
        # 转换为农历
        self.lunar_date = self.convert_to_lunar()
        
        # 计算八字
        self.ba_zi = self.calculate_ba_zi()
        
        # 计算节气信息
        self.jie_qi_info = self.calculate_jie_qi_info()
        
        # 计算大运信息
        self.da_yun_info = self.calculate_da_yun_info()
    
    def calculate_solar_time(self):
        """
        计算真太阳时
        真太阳时 = 出生时间 + (出生城市经度 - 120) × 4分钟
        """
        # 计算时间差（分钟）
        time_diff = (self.birth_longitude - 120) * 4
        
        # 创建出生时间
        birth_time = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
        
        # 计算真太阳时
        solar_time = birth_time + datetime.timedelta(minutes=time_diff)
        
        return solar_time
    
    def convert_to_lunar(self):
        """
        将公历日期转换为农历
        """ 
        if self.calendar == "公历":
            # 使用真太阳时转换
            year = self.solar_time.year
            month = self.solar_time.month
            day = self.solar_time.day
            day_obj = sxtwl.fromSolar(year, month, day)
        else:  # 农历
            # 直接使用输入的农历日期
            year = self.year
            month = self.month
            day = self.day
            # 需要判断是否为闰月
            day_obj = sxtwl.fromLunar(year, month, day)
            
            # 同时更新solar_time为对应的公历日期
            solar_year = day_obj.getSolarYear()
            solar_month = day_obj.getSolarMonth()
            solar_day = day_obj.getSolarDay()
            # 保持原始的小时和分钟，仅更新日期部分
            self.solar_time = datetime.datetime(solar_year, solar_month, solar_day, self.solar_time.hour, self.solar_time.minute, self.solar_time.second, self.solar_time.microsecond)
        
        return day_obj
    
    def calculate_ba_zi(self):
        """
        计算八字
        """
        # 获取年柱
        year_gz = self.lunar_date.getYearGZ()
        year_ba_zi = Gan[year_gz.tg] + Zhi[year_gz.dz]
        
        # 获取月柱
        month_gz = self.lunar_date.getMonthGZ()
        month_ba_zi = Gan[month_gz.tg] + Zhi[month_gz.dz]
        
        # 获取日柱
        day_gz = self.lunar_date.getDayGZ()
        day_ba_zi = Gan[day_gz.tg] + Zhi[day_gz.dz]
        
        # 获取时柱
        # 使用日天干和真太阳时的小时来计算时柱
        hour_gz = sxtwl.getShiGz(day_gz.tg, self.solar_time.hour)
        hour_ba_zi = Gan[hour_gz.tg] + Zhi[hour_gz.dz]
        
        return year_ba_zi + " " + month_ba_zi + " " + day_ba_zi + " " + hour_ba_zi
    
    def calculate_jie_qi_info(self):
        """
        计算节气信息
        """
        # 获取当前日期的节气信息
        current_day = self.lunar_date
        
        # 查找上一个节气
        prev_jie_qi = None
        prev_jie_qi_day = current_day
        days_since_prev = 0
        
        # 向前查找最多30天
        for i in range(30):
            if prev_jie_qi_day.hasJieQi():
                prev_jie_qi = prev_jie_qi_day.getJieQi()
                break
            prev_jie_qi_day = prev_jie_qi_day.before(1)
            days_since_prev += 1
        
        # 查找下一个节气
        next_jie_qi = None
        next_jie_qi_day = current_day
        days_to_next = 0
        
        # 向后查找最多30天
        for i in range(30):
            if next_jie_qi_day.hasJieQi():
                next_jie_qi = next_jie_qi_day.getJieQi()
                break
            next_jie_qi_day = next_jie_qi_day.after(1)
            days_to_next += 1
        
        # 格式化输出
        if prev_jie_qi is not None and next_jie_qi is not None:
            prev_jie_qi_name = jqmc[prev_jie_qi]
            next_jie_qi_name = jqmc[next_jie_qi]
            return f"生于{prev_jie_qi_name}节气后{days_since_prev}天，{next_jie_qi_name}节气前{days_to_next}天"
        
        return ""
    
    def calculate_da_yun_info(self):
        """
        计算大运信息
        """
        # 获取年干
        year_gz = self.ba_zi[:2]
        year_tg = year_gz[0]
        
        # 判断年干阴阳
        yang_tian_gan = ["甲", "丙", "戊", "庚", "壬"]
        is_year_tg_yang = year_tg in yang_tian_gan
        
        # 判断性别
        is_male = self.gender == "男"
        
        # 判断大运顺逆排
        # 阳男阴女顺排，阴男阳女逆排
        is_forward = (is_year_tg_yang and is_male) or (not is_year_tg_yang and not is_male)
        da_yun_direction = "顺排" if is_forward else "逆排"
        
        # 计算起运时间
        # 首先获取节气信息
        current_day = self.lunar_date
        
        if is_forward:
            # 顺排：查找下一个节气
            jie_qi_day = current_day
            days_to_jie_qi = 0
            
            # 向后查找最多30天
            for i in range(30):
                if jie_qi_day.hasJieQi():
                    break
                jie_qi_day = jie_qi_day.after(1)
                days_to_jie_qi += 1
        else:
            # 逆排：查找上一个节气
            jie_qi_day = current_day
            days_to_jie_qi = 0
            
            # 向前查找最多30天
            for i in range(30):
                if jie_qi_day.hasJieQi():
                    break
                jie_qi_day = jie_qi_day.before(1)
                days_to_jie_qi += 1
        
        # 计算起运时间（天数转年数）
        # 起运时间 = 节气天数 ÷ 3
        qi_yun_years_float = days_to_jie_qi / 3.0
        qi_yun_years = int(qi_yun_years_float)
        qi_yun_months = int(round((qi_yun_years_float - qi_yun_years) * 12))
        
        # 计算起运岁数
        # 起运时间为整数，起运岁数 = 起运时间
        # 如果起运时间为余数，起运岁数 = 起运时间向上取整
        import math
        qi_yun_age = int(math.ceil(qi_yun_years_float))
        
        # 格式化输出
        # 根据规则显示性别和年干信息
        if is_male:
            gender_info = "阳男" if is_year_tg_yang else "阴男"
        else:
            gender_info = "阳女" if is_year_tg_yang else "阴女"
        return f"{gender_info}，{da_yun_direction}，起运时间{qi_yun_years}年{qi_yun_months}月，{qi_yun_age}岁起运"
    
    def format_output(self):
        """
        格式化输出
        """
        output = ""
        if self.name:
            output += f"姓名：{self.name}\n"
        
        # 性别
        gender_text = "男 (乾造)" if self.gender == "男" else "女 (坤造)"
        output += f"性别：{gender_text}\n"
        
        # 出生时间
        output += "出生时间：\n"
        
        if self.calendar == "公历":
            # 显示公历日期和对应的农历日期
            # 公历使用真太阳时，但显示为整数分钟
            output += f"  公历：{self.solar_time.year}年{self.solar_time.month}月{self.solar_time.day}日{self.solar_time.hour:02d}:{self.solar_time.minute:02d}\n"
            
            # 农历
            lunar_year = self.lunar_date.getLunarYear()
            lunar_month = self.lunar_date.getLunarMonth()
            lunar_day = self.lunar_date.getLunarDay()
            is_leap = "(闰月)" if self.lunar_date.isLunarLeap() else "(非闰月)"
            output += f"  农历：{lunar_year}年{lunar_month}月{lunar_day}日{self.solar_time.hour:02d}:{self.solar_time.minute:02d} {is_leap}\n"
        else:  # 农历
            # 显示农历日期和对应的公历日期
            # 农历使用真太阳时校正后的时间
            lunar_year = self.lunar_date.getLunarYear()
            lunar_month = self.lunar_date.getLunarMonth()
            lunar_day = self.lunar_date.getLunarDay()
            is_leap = "(闰月)" if self.lunar_date.isLunarLeap() else "(非闰月)"
            output += f"  农历：{lunar_year}年{lunar_month}月{lunar_day}日{self.solar_time.hour:02d}:{self.solar_time.minute:02d} {is_leap}\n"
            
            # 公历使用真太阳时，但显示为整数分钟
            output += f"  公历：{self.solar_time.year}年{self.solar_time.month}月{self.solar_time.day}日{self.solar_time.hour:02d}:{self.solar_time.minute:02d}\n"
        
        # 出生城市
        output += f"出生城市：{self.birth_city}({self.birth_longitude}°E)\n"
        
        # 现居城市
        if self.current_city:
            output += f"现居城市：{self.current_city}\n"
        
        # 八字信息
        output += f"八字信息：{self.ba_zi}\n"
        
        # 节气信息
        if self.jie_qi_info:
            output += f"节气信息：{self.jie_qi_info}\n"
        
        # 大运信息
        if self.da_yun_info:
            output += f"大运信息：{self.da_yun_info}\n"
        
        return output


def main():
    # 示例输入
    name = "张三"
    gender = "男"
    calendar = "公历"
    year = 1993
    month = 9
    day = 19
    hour = 5
    minute = 45
    birth_city = "深圳"
    current_city = "惠州"
    
    # 创建计算器实例
    calculator = BaZiCalculator(name, gender, calendar, year, month, day, hour, minute, birth_city, current_city)
    
    # 输出结果
    print(calculator.format_output())


if __name__ == "__main__":
    main()