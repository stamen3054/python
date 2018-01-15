# 大众点评 crawler
# 需要去大众点评网选择想爬取的区域（今后的开发应该会加入选择功能来替代用户自己输入）
# 例：https://www.dianping.com/search/category/10/10/r1651 是'天津-南开区-王顶堤'附近的餐馆
# 需要决定要爬取几页的餐馆，默认是1，最大是7（7是我随机选的）
# 有时某个餐馆页面与爬虫结构不适配，会报错
# 有时某个推荐菜没有价格，会显示0元


# DazhongDianping crawler
# To run the crawler, certain area needs to be provided(may provide selections in future development instead of url)
# Example: https://www.dianping.com/search/category/10/10/r1651 is for 'Tianjin-Nankai District-WangDingDi'
# The number of pages to be crawled needs to be specified(default 1, max 7)
# Some restaurants are not compatible with the crawler, will crash the application
# Some recommend dishes have no price so it shows $0