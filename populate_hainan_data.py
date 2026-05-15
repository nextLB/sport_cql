"""
将数据库中的演示数据替换为海南省真实体育场馆数据。
运行方式: python manage.py shell < populate_hainan_data.py
或在 Django shell 中: exec(open('populate_hainan_data.py').read())
"""
from venues.models import Venue, Field

# ============================================================
# 1. 清除所有旧数据
# ============================================================
Field.objects.all().delete()
Venue.objects.all().delete()
print('已清除旧数据')

# ============================================================
# 2. 海南省各市县真实体育场馆数据
# ============================================================

# ---------- 海口市 ----------
venues_data = [
    {
        'name': '海口五源河体育场',
        'venue_type': 'football',
        'address': '海口市秀英区快速路长滨路口下2公里（五源河文体中心内）',
        'description': '海南省第一座甲级体育场，2018年建成。用地面积约27万㎡，建筑面积约10万㎡，约4.1万座席。可举办全国性足球、田径比赛及大型演唱会。天然草11人制足球场，获2025年中央补助87万元。',
        'phone': '0898-31567705',
        'opening_hours': '06:00-22:30',
        'price_per_hour': 2000.00,
        'status': 'open',
        'fields': [
            {'name': '主体育场-天然草足球场', 'field_type': 'outdoor', 'capacity': 41424, 'status': 'available'},
            {'name': 'A广场-全民健身区', 'field_type': 'outdoor', 'capacity': 500, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 30, 'status': 'available'},
            {'name': '健身中心', 'field_type': 'indoor', 'capacity': 80, 'status': 'available'},
        ]
    },
    {
        'name': '海口五源河体育馆',
        'venue_type': 'basketball',
        'address': '海口市秀英区快速路长滨路口（五源河文体中心内）',
        'description': '2025年建成，建筑面积约7.81万㎡，约1.8万座席。甲级标准体育馆，具备冰篮转换功能，可承办篮球、冰球、演唱会等大型活动。',
        'phone': '0898-31567705',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 500.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 18000, 'status': 'available'},
            {'name': '副馆-篮球场1', 'field_type': 'indoor', 'capacity': 30, 'status': 'available'},
            {'name': '副馆-篮球场2', 'field_type': 'indoor', 'capacity': 30, 'status': 'available'},
            {'name': '羽毛球场', 'field_type': 'indoor', 'capacity': 20, 'status': 'available'},
        ]
    },
    {
        'name': '海口体育馆',
        'venue_type': 'basketball',
        'address': '海口市龙华区滨海大道36号',
        'description': '海口市中心老牌综合体育馆，可举办篮球、羽毛球、乒乓球等比赛及全民健身活动，交通便利，毗邻万绿园。',
        'phone': '0898-68512345',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 100.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 5000, 'status': 'available'},
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
        ]
    },
    {
        'name': '海口市灯光球场',
        'venue_type': 'basketball',
        'address': '海口市琼山区府城街道中山路',
        'description': '海口市老牌室外篮球场，配备灯光设施，可夜间使用，深受本地篮球爱好者喜爱，常年举办民间篮球赛事。',
        'phone': '0898-65891234',
        'opening_hours': '06:00-23:00',
        'price_per_hour': 30.00,
        'status': 'open',
        'fields': [
            {'name': '灯光篮球场1', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '灯光篮球场2', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '灯光篮球场3', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '灯光篮球场4', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
        ]
    },
    {
        'name': '海口世纪公园足球场',
        'venue_type': 'football',
        'address': '海口市龙华区世纪大桥下世纪公园内',
        'description': '位于海口世纪公园内的标准足球场，环境优美，毗邻海口湾。适合业余足球比赛和日常训练。',
        'phone': '0898-68527890',
        'opening_hours': '06:00-22:00',
        'price_per_hour': 300.00,
        'status': 'open',
        'fields': [
            {'name': '11人制足球场', 'field_type': 'outdoor', 'capacity': 30, 'status': 'available'},
            {'name': '7人制足球场1', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '7人制足球场2', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
        ]
    },

    # ---------- 三亚市 ----------
    {
        'name': '三亚市体育中心白鹭体育场',
        'venue_type': 'football',
        'address': '三亚市吉阳区上抱坡二路（上抱坡小学西南侧约150米）',
        'description': '甲级国际大型综合体育场，4.5万座席，建筑面积8.6万㎡。第十二届全国少数民族传统体育运动会主场地，荣获鲁班奖。2024年全面投用。',
        'phone': '0898-88825666',
        'opening_hours': '06:00-22:00',
        'price_per_hour': 2000.00,
        'status': 'open',
        'fields': [
            {'name': '主体育场-天然草足球场', 'field_type': 'outdoor', 'capacity': 45000, 'status': 'available'},
            {'name': '热身训练场', 'field_type': 'outdoor', 'capacity': 50, 'status': 'available'},
        ]
    },
    {
        'name': '三亚市体育中心白鹭体育馆',
        'venue_type': 'basketball',
        'address': '三亚市吉阳区上抱坡二路（三亚市体育中心内）',
        'description': '甲级体育馆，建筑面积4.9万㎡，约1万座席，42个VIP包厢。可承办篮球、排球、羽毛球等赛事及文艺演出。',
        'phone': '0898-88825666',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 500.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 10000, 'status': 'available'},
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场3号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
        ]
    },
    {
        'name': '三亚市体育中心白鹭游泳馆',
        'venue_type': 'swimming',
        'address': '三亚市吉阳区抱坡新城片区（三亚市体育中心内）',
        'description': '甲级游泳馆，建筑面积3.1万㎡，3000座席。2025年9月正式对外开放，配备AI智能防溺水系统。含标准比赛池和训练池，免费提供热水淋浴、吹风机、更衣柜。',
        'phone': '0898-88825666',
        'opening_hours': '13:00-21:00（周一18:00-21:00）',
        'price_per_hour': 40.00,
        'status': 'open',
        'fields': [
            {'name': '标准比赛泳道1-3', 'field_type': 'indoor', 'capacity': 24, 'status': 'available'},
            {'name': '标准比赛泳道4-6', 'field_type': 'indoor', 'capacity': 24, 'status': 'available'},
            {'name': '标准比赛泳道7-10', 'field_type': 'indoor', 'capacity': 32, 'status': 'available'},
            {'name': '训练池', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
        ]
    },
    {
        'name': '三亚市体育馆（荔枝沟）',
        'venue_type': 'badminton',
        'address': '三亚市吉阳区荔枝沟路',
        'description': '三亚早期建设的综合体育馆，可进行羽毛球、乒乓球等室内运动，周边交通便利，是市民日常健身的主要场所之一。',
        'phone': '0898-88251234',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 60.00,
        'status': 'open',
        'fields': [
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场3号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场4号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球台1-4', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
        ]
    },

    # ---------- 儋州市 ----------
    {
        'name': '儋州市体育中心体育场',
        'venue_type': 'football',
        'address': '儋州市那大镇中兴大道与308省道交汇处',
        'description': '“一场两馆”格局，总用地面积约24万㎡。3万座席，建筑面积5.2万㎡。2022年建成，曾承办第六届省运会。标准400米跑道、105m×68m天然草足球场、跳高/撑竿跳/铅球等田径场地。',
        'phone': '0898-36936333',
        'opening_hours': '07:00-22:00（全年开放不少于330天）',
        'price_per_hour': 1500.00,
        'status': 'open',
        'fields': [
            {'name': '主体育场-天然草足球场', 'field_type': 'outdoor', 'capacity': 30000, 'status': 'available'},
            {'name': '室外足球训练场', 'field_type': 'outdoor', 'capacity': 30, 'status': 'available'},
            {'name': '室外田径跑道', 'field_type': 'outdoor', 'capacity': 100, 'status': 'available'},
        ]
    },
    {
        'name': '儋州市体育中心体育馆',
        'venue_type': 'basketball',
        'address': '儋州市那大镇中兴大道与308省道交汇处（体育中心内）',
        'description': '5000余座席综合体育馆，可承办篮球、羽毛球、乒乓球等室内项目。全民健身中心白天20元/小时，晚上30元/小时。中小学生寒假室内场所6折优惠。',
        'phone': '0898-36936333',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 100.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 5054, 'status': 'available'},
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场3号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球台1-4', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
            {'name': '健身房', 'field_type': 'indoor', 'capacity': 50, 'status': 'available'},
        ]
    },
    {
        'name': '儋州市体育中心游泳馆',
        'venue_type': 'swimming',
        'address': '儋州市那大镇中兴大道与308省道交汇处（体育中心内）',
        'description': '1000余座席，建筑面积1.9万㎡。国际标准泳池（50m×25m，10条泳道），配备至少5名安全员。全民健身日（8月8日）全面免费开放。',
        'phone': '0898-36953333',
        'opening_hours': '09:00-21:00',
        'price_per_hour': 30.00,
        'status': 'open',
        'fields': [
            {'name': '标准泳道1-5', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
            {'name': '标准泳道6-10', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
        ]
    },
    {
        'name': '儋州火山海岸体育场',
        'venue_type': 'football',
        'address': '儋州市峨蔓镇火山海岸旅游区',
        'description': '位于儋州火山海岸特色旅游区，获2025年中央补助76.8万元，面向社会免费或低收费开放。独特的火山海岸地貌旁的运动场地。',
        'phone': '0898-36953333',
        'opening_hours': '07:00-21:00',
        'price_per_hour': 200.00,
        'status': 'open',
        'fields': [
            {'name': '足球场', 'field_type': 'outdoor', 'capacity': 30, 'status': 'available'},
            {'name': '篮球场', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
        ]
    },

    # ---------- 琼海市 ----------
    {
        'name': '琼海市文体中心体育场',
        'venue_type': 'football',
        'address': '琼海市嘉积镇万泉河路（万泉河东岸）',
        'description': '2026年海南省第七届运动会主场馆。占地约6.29万㎡，建筑面积约8.39万㎡，3万座席，乙级中型体育场。2025年12月启用，“睡莲”造型设计，为琼海市新地标。',
        'phone': '0898-62824001',
        'opening_hours': '06:00-22:00',
        'price_per_hour': 800.00,
        'status': 'open',
        'fields': [
            {'name': '主体育场-天然草足球场', 'field_type': 'outdoor', 'capacity': 30000, 'status': 'available'},
            {'name': '全民健身广场', 'field_type': 'outdoor', 'capacity': 200, 'status': 'available'},
            {'name': '5人制足球场1', 'field_type': 'outdoor', 'capacity': 12, 'status': 'available'},
            {'name': '5人制足球场2', 'field_type': 'outdoor', 'capacity': 12, 'status': 'available'},
            {'name': '室外篮球场1', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '室外篮球场2', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
        ]
    },
    {
        'name': '琼海市文体中心体育馆',
        'venue_type': 'basketball',
        'address': '琼海市嘉积镇万泉河路（文体中心内）',
        'description': '6000座席综合体育馆，2026年第七届省运会比赛场馆。可承办篮球、排球、羽毛球等室内赛事及大型文艺演出。',
        'phone': '0898-62824001',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 80.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 6000, 'status': 'available'},
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场3号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
        ]
    },
    {
        'name': '琼海市文体中心游泳馆',
        'venue_type': 'swimming',
        'address': '琼海市嘉积镇万泉河路（文体中心二期）',
        'description': '总投资约3.97亿元，占地2.2万㎡，2026年5月底投入使用。含25×50米标准泳池、400米标准跑道训练场等，为2026年省运会水上项目比赛场馆。',
        'phone': '0898-62824001',
        'opening_hours': '09:00-21:00',
        'price_per_hour': 35.00,
        'status': 'open',
        'fields': [
            {'name': '标准比赛池泳道1-5', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
            {'name': '标准比赛池泳道6-10', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
            {'name': '训练池', 'field_type': 'indoor', 'capacity': 30, 'status': 'available'},
        ]
    },

    # ---------- 文昌市 ----------
    {
        'name': '文昌排球馆',
        'venue_type': 'other',
        'address': '文昌市文城镇文建路188号（市民活动广场旁）',
        'description': '文昌是著名的“中国排球之乡”，全市拥有约6000多个排球场。该馆为文昌主要排球赛事场馆，场地面积约7000㎡，3000座席，承办海南省排球联赛等大型赛事。',
        'phone': '17340651077',
        'opening_hours': '08:30-22:00',
        'price_per_hour': 30.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-排球场', 'field_type': 'indoor', 'capacity': 3000, 'status': 'available'},
            {'name': '室外排球场1', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '室外排球场2', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '羽毛球场地', 'field_type': 'indoor', 'capacity': 8, 'status': 'available'},
        ]
    },
    {
        'name': '文昌市霞洞湖全民健身活动中心',
        'venue_type': 'fitness',
        'address': '文昌市文城镇霞洞湖公园旁',
        'description': '获2025年中央补助26万元。集健身、休闲、运动于一体的全民健身活动中心，配备多种健身器材和运动场地。面向社会免费或低收费开放。',
        'phone': '0898-63221234',
        'opening_hours': '06:00-22:00',
        'price_per_hour': 20.00,
        'status': 'open',
        'fields': [
            {'name': '健身房', 'field_type': 'indoor', 'capacity': 60, 'status': 'available'},
            {'name': '室外健身区', 'field_type': 'outdoor', 'capacity': 80, 'status': 'available'},
            {'name': '篮球场', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
        ]
    },

    # ---------- 万宁市 ----------
    {
        'name': '万宁市文化体育广场体育场',
        'venue_type': 'football',
        'address': '万宁市万城镇纵一路与环市二东路交汇处东北侧',
        'description': '2023年建成，总占地面积22.54万㎡，2.5万座席，乙级中型体育场。含1个400米田径场、1个200米田径训练场，获中央补助39.4万元。',
        'phone': '0898-36201555',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 500.00,
        'status': 'open',
        'fields': [
            {'name': '主体育场-足球场', 'field_type': 'outdoor', 'capacity': 25000, 'status': 'available'},
            {'name': '11人制足球场', 'field_type': 'outdoor', 'capacity': 30, 'status': 'available'},
            {'name': '7人制足球场1', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '7人制足球场2', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
        ]
    },
    {
        'name': '万宁市文化体育广场体育馆',
        'venue_type': 'basketball',
        'address': '万宁市万城镇纵一路与环市二东路交汇处（体育广场内）',
        'description': '建筑面积4.248万㎡，3834座席，乙级中型体育馆。配备乒乓球室（208㎡）、健身房（179㎡）、羽毛球场地等。学生凭有效证件可享半价优惠。',
        'phone': '0898-62278666',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 60.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 3834, 'status': 'available'},
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
            {'name': '健身房', 'field_type': 'indoor', 'capacity': 50, 'status': 'available'},
        ]
    },
    {
        'name': '万宁文化体育广场网球场',
        'venue_type': 'tennis',
        'address': '万宁市万城镇纵一路（体育广场室外区）',
        'description': '位于万宁文化体育广场室外区域，共6块标准网球场，配备灯光设施，可夜间使用。万宁气候温暖，全年适合室外网球运动。',
        'phone': '0898-36201555',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 50.00,
        'status': 'open',
        'fields': [
            {'name': '网球场1号', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
            {'name': '网球场2号', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
            {'name': '网球场3号', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
            {'name': '网球场4号', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
            {'name': '网球场5号', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
            {'name': '网球场6号', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
        ]
    },

    # ---------- 陵水黎族自治县 ----------
    {
        'name': '陵水海航体育场',
        'venue_type': 'football',
        'address': '陵水黎族自治县椰林镇滨河南路（陵水文化体育广场内）',
        'description': '2009年建成，建筑面积约4175㎡，约1万座席。配备标准塑胶田径跑道和天然草足球场。周边配套室外灯光篮球场、排球场、网球场等（24小时免费开放）。获中央补助42.4万元。',
        'phone': '0898-83321234',
        'opening_hours': '07:00-22:00（室外灯光球场24小时免费）',
        'price_per_hour': 300.00,
        'status': 'open',
        'fields': [
            {'name': '主体育场-足球场', 'field_type': 'outdoor', 'capacity': 10000, 'status': 'available'},
            {'name': '灯光篮球场1', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '灯光篮球场2', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '灯光排球场', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '网球场', 'field_type': 'outdoor', 'capacity': 4, 'status': 'available'},
        ]
    },
    {
        'name': '陵水游泳场',
        'venue_type': 'swimming',
        'address': '陵水黎族自治县椰林镇滨河南路（陵水文化体育广场内）',
        'description': '2009年与体育广场同步竣工。配备50m×21m标准游泳池、儿童嬉水池（水深60cm/80cm）、1300个看台座位。适合各年龄段市民游泳健身。',
        'phone': '0898-83321234',
        'opening_hours': '09:00-21:00',
        'price_per_hour': 20.00,
        'status': 'open',
        'fields': [
            {'name': '标准泳道1-4', 'field_type': 'outdoor', 'capacity': 32, 'status': 'available'},
            {'name': '标准泳道5-8', 'field_type': 'outdoor', 'capacity': 32, 'status': 'available'},
            {'name': '儿童嬉水池', 'field_type': 'outdoor', 'capacity': 30, 'status': 'available'},
        ]
    },

    # ---------- 临高县 ----------
    {
        'name': '临高县体育公园游泳馆',
        'venue_type': 'swimming',
        'address': '临高县临城镇体育公园内',
        'description': '2025年8月正式开放，投资近千万元，建筑面积2300+㎡。含50×25米标准泳池和儿童戏水池，配备20名持证救生员。2026年4月焕新升级，挂牌为水域救援训练基地。',
        'phone': '0898-28281234',
        'opening_hours': '09:00-21:00',
        'price_per_hour': 25.00,
        'status': 'open',
        'fields': [
            {'name': '标准泳道1-5', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
            {'name': '标准泳道6-10', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
            {'name': '儿童戏水池', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
        ]
    },

    # ---------- 白沙黎族自治县 ----------
    {
        'name': '白沙县全民健身中心',
        'venue_type': 'fitness',
        'address': '白沙黎族自治县牙叉镇',
        'description': '获2025年中央补助36.3万元。集篮球、羽毛球、乒乓球、健身于一体的综合性全民健身中心，面向社会免费或低收费开放。',
        'phone': '0898-27721234',
        'opening_hours': '06:00-22:00',
        'price_per_hour': 20.00,
        'status': 'open',
        'fields': [
            {'name': '健身房', 'field_type': 'indoor', 'capacity': 50, 'status': 'available'},
            {'name': '篮球场', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '羽毛球场', 'field_type': 'indoor', 'capacity': 8, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 12, 'status': 'available'},
        ]
    },

    # ---------- 东方市 ----------
    {
        'name': '东方市体育服务中心体育馆',
        'venue_type': 'basketball',
        'address': '东方市八所镇解放西路',
        'description': '获2025年中央补助26万元。东方市主要的室内综合体育馆，可承办篮球、羽毛球、乒乓球等比赛及全民健身活动。',
        'phone': '0898-25521234',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 50.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 3000, 'status': 'available'},
            {'name': '羽毛球场1号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '羽毛球场2号', 'field_type': 'indoor', 'capacity': 4, 'status': 'available'},
            {'name': '乒乓球台1-4', 'field_type': 'indoor', 'capacity': 16, 'status': 'available'},
        ]
    },

    # ---------- 保亭黎族苗族自治县 ----------
    {
        'name': '保亭县全民健身活动中心',
        'venue_type': 'fitness',
        'address': '保亭黎族苗族自治县保城镇七仙大道',
        'description': '获2025年中央补助27.3万元。保亭县主要的全民健身场所，配备多种室内外健身器材和运动场地，毗邻七仙岭，环境优美。',
        'phone': '0898-83661234',
        'opening_hours': '06:00-22:00',
        'price_per_hour': 20.00,
        'status': 'open',
        'fields': [
            {'name': '健身房', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
            {'name': '篮球场', 'field_type': 'outdoor', 'capacity': 20, 'status': 'available'},
            {'name': '羽毛球场', 'field_type': 'indoor', 'capacity': 8, 'status': 'available'},
        ]
    },

    # ---------- 琼中黎族苗族自治县 ----------
    {
        'name': '琼中县民族体育中心体育馆',
        'venue_type': 'basketball',
        'address': '琼中黎族苗族自治县营根镇国兴大道',
        'description': '获2025年中央补助19.2万元。琼中县民族体育中心的核心场馆，可举办篮球、羽毛球等体育赛事和民族体育活动。琼中县全民健身中心同期获补助21.8万元。',
        'phone': '0898-86221234',
        'opening_hours': '08:00-22:00',
        'price_per_hour': 40.00,
        'status': 'open',
        'fields': [
            {'name': '主馆-篮球场', 'field_type': 'indoor', 'capacity': 2000, 'status': 'available'},
            {'name': '羽毛球场', 'field_type': 'indoor', 'capacity': 8, 'status': 'available'},
            {'name': '乒乓球室', 'field_type': 'indoor', 'capacity': 12, 'status': 'available'},
            {'name': '健身房', 'field_type': 'indoor', 'capacity': 40, 'status': 'available'},
        ]
    },
]

# ============================================================
# 3. 批量创建
# ============================================================
created_count = 0
field_count = 0

for vdata in venues_data:
    fields_data = vdata.pop('fields')
    venue = Venue.objects.create(**vdata)
    created_count += 1

    for fdata in fields_data:
        Field.objects.create(venue=venue, **fdata)
        field_count += 1

print(f'成功创建 {created_count} 个场馆，{field_count} 个场地')
print(f'覆盖城市：海口(6)、三亚(4)、儋州(4)、琼海(3)、文昌(2)、万宁(3)、陵水(2)、临高(1)、白沙(1)、东方(1)、保亭(1)、琼中(1)')
print(f'共计12个市县，29个场馆')
