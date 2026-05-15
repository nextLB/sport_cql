#!/usr/bin/env python
"""生成教练和课程演示数据"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_booking.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from courses.models import Coach, Course, CourseEnrollment
from venues.models import Venue
from users.models import User
from datetime import date, timedelta

Coach.objects.all().delete()
Course.objects.all().delete()
CourseEnrollment.objects.all().delete()

coaches_data = [
    {
        'name': '陈志强', 'gender': 'male', 'phone': '13876010001', 'email': 'chenzq@example.com',
        'speciality': '篮球, 健身', 'experience': 12,
        'certificate': '国家一级篮球教练员, NASM-CPT',
        'description': '前职业篮球运动员，退役后从事篮球教学12年。擅长青少年篮球启蒙与进阶训练，培养多名学员进入省队。教学风格严谨但不失趣味，深受学员喜爱。'
    },
    {
        'name': '林海燕', 'gender': 'female', 'phone': '13876010002', 'email': 'linhy@example.com',
        'speciality': '羽毛球', 'experience': 8,
        'certificate': '国家二级羽毛球教练员, 社会体育指导员',
        'description': '海南省羽毛球队退役队员，曾获全省羽毛球锦标赛女单冠军。专注羽毛球基础教学与成人进阶训练，教学耐心细致。'
    },
    {
        'name': '王泳', 'gender': 'male', 'phone': '13876010003', 'email': 'wangyong@example.com',
        'speciality': '游泳', 'experience': 15,
        'certificate': '国家级游泳教练员, 救生员资格证',
        'description': '原海南省游泳队主教练，培养过多名全国游泳锦标赛获奖选手。擅长各泳姿教学，从零基础到竞技训练全覆盖，尤其擅长儿童游泳启蒙。'
    },
    {
        'name': '张伟杰', 'gender': 'male', 'phone': '13876010004', 'email': 'zhangwj@example.com',
        'speciality': '足球, 体能训练', 'experience': 10,
        'certificate': '亚足联B级教练员, CSCS体能认证',
        'description': '前中甲联赛球员，退役后转型青训教练。拥有亚足联B级教练证书，专注于青少年足球培训。注重基本功与战术意识培养。'
    },
    {
        'name': '李美玲', 'gender': 'female', 'phone': '13876010005', 'email': 'liml@example.com',
        'speciality': '网球', 'experience': 7,
        'certificate': 'ITF一级教练员, PTR认证教练',
        'description': '体育院校网球专业毕业，拥有ITF和PTR双重认证。教学风格轻松活泼，擅长通过游戏化方式引导学员掌握网球技术。'
    },
    {
        'name': '刘健', 'gender': 'male', 'phone': '13876010006', 'email': 'liujian@example.com',
        'speciality': '乒乓球', 'experience': 20,
        'certificate': '国家级乒乓球教练员, 国家一级裁判员',
        'description': '退休省队乒乓球教练，40年乒乓球教学经验。培养出多名省级冠军选手。擅长技术动作拆解与战术训练，适合各年龄段学员。'
    },
    {
        'name': '黄晓明', 'gender': 'male', 'phone': '13876010007', 'email': 'huangxm@example.com',
        'speciality': '健身, 瑜伽, 拳击', 'experience': 6,
        'certificate': 'ACE-CPT, RYT200瑜伽导师, 拳击教练员',
        'description': '全能型健身教练，拥有ACE私人教练认证和瑜伽导师资格。擅长减脂塑形、力量训练、瑜伽和拳击课程。根据学员体质定制训练计划。'
    },
    {
        'name': '吴芳', 'gender': 'female', 'phone': '13876010008', 'email': 'wufang@example.com',
        'speciality': '排球, 体能训练', 'experience': 9,
        'certificate': '国家一级排球教练员, FMS功能训练认证',
        'description': '前省排球队主力二传手，退役后致力于青少年排球推广。擅长排球基础教学与团队战术配合训练，同时具备FMS功能动作筛查资质。'
    },
]

coaches = []
for data in coaches_data:
    coach = Coach.objects.create(**data)
    coaches.append(coach)
    print(f'教练: {coach.name} ({coach.speciality})')

print()

venues = list(Venue.objects.all()[:20])

today = date.today()
courses_data = [
    {
        'name': '青少年篮球基础班',
        'coach': coaches[0], 'venue': venues[0], 'course_type': 'basketball',
        'description': '面向8-15岁青少年的篮球基础训练课程。包含运球、投篮、传球、防守等基本功教学，以及基础战术配合。每节课1.5小时。',
        'max_students': 20, 'price': 1280.00,
        'start_date': today + timedelta(days=7), 'end_date': today + timedelta(days=97),
        'schedule': '每周六、日 09:00-10:30', 'status': 'enrolling',
    },
    {
        'name': '成人篮球提高班',
        'coach': coaches[0], 'venue': venues[1], 'course_type': 'basketball',
        'description': '面向有一定篮球基础的成人学员。强化个人技术、战术配合、实战对抗训练。提高攻防转换意识和比赛阅读能力。',
        'max_students': 16, 'price': 1680.00,
        'start_date': today + timedelta(days=10), 'end_date': today + timedelta(days=70),
        'schedule': '每周二、四 19:00-20:30', 'status': 'enrolling',
    },
    {
        'name': '羽毛球成人训练营',
        'coach': coaches[1], 'venue': venues[2], 'course_type': 'badminton',
        'description': '面向成人羽毛球爱好者的系统训练。涵盖握拍、发球、高远球、扣杀、网前球等技术动作，以及单双打战术。',
        'max_students': 12, 'price': 980.00,
        'start_date': today + timedelta(days=5), 'end_date': today + timedelta(days=65),
        'schedule': '每周一、三、五 18:30-20:00', 'status': 'enrolling',
    },
    {
        'name': '儿童游泳启蒙班',
        'coach': coaches[2], 'venue': venues[3], 'course_type': 'swimming',
        'description': '面向5-8岁儿童的游泳启蒙课程。以培养水感、克服恐水心理为主，学习基础蛙泳和自由泳。小班教学，每班不超过8人。',
        'max_students': 8, 'price': 1580.00,
        'start_date': today + timedelta(days=3), 'end_date': today + timedelta(days=63),
        'schedule': '每周六、日 10:00-11:00', 'status': 'enrolling',
    },
    {
        'name': '成人游泳进阶班',
        'coach': coaches[2], 'venue': venues[4], 'course_type': 'swimming',
        'description': '面向已掌握基本泳姿的成人学员。纠正泳姿技术细节，提升速度和耐力。学习蝶泳和转身技巧。',
        'max_students': 10, 'price': 1280.00,
        'start_date': today + timedelta(days=4), 'end_date': today + timedelta(days=64),
        'schedule': '每周一、三 19:30-21:00', 'status': 'enrolling',
    },
    {
        'name': '青少年足球青训营',
        'coach': coaches[3], 'venue': venues[5], 'course_type': 'football',
        'description': '面向10-16岁青少年的专业足球训练。包含体能训练、基本功、战术配合、实战比赛。优秀学员可推荐至职业俱乐部试训。',
        'max_students': 24, 'price': 1980.00,
        'start_date': today + timedelta(days=2), 'end_date': today + timedelta(days=92),
        'schedule': '每周六、日 08:00-10:00', 'status': 'enrolling',
    },
    {
        'name': '网球入门精品课',
        'coach': coaches[4], 'venue': venues[6], 'course_type': 'tennis',
        'description': '面向零基础网球爱好者的入门课程。从握拍、正反手击球入手，逐步学习发球、截击等基本技术。小班教学保证每个人有充足练习时间。',
        'max_students': 8, 'price': 1880.00,
        'start_date': today + timedelta(days=1), 'end_date': today + timedelta(days=61),
        'schedule': '每周二、四、六 17:00-18:30', 'status': 'enrolling',
    },
    {
        'name': '乒乓球技术特训班',
        'coach': coaches[5], 'venue': venues[7], 'course_type': 'table_tennis',
        'description': '面向有基础的乒乓球爱好者。强化发球旋转变化、接发球判断、连续攻球等技术。配备发球机辅助训练，提升比赛实战能力。',
        'max_students': 6, 'price': 2200.00,
        'start_date': today + timedelta(days=8), 'end_date': today + timedelta(days=68),
        'schedule': '每周一、四 19:00-21:00', 'status': 'enrolling',
    },
    {
        'name': '综合减脂塑形课',
        'coach': coaches[6], 'venue': venues[8], 'course_type': 'fitness',
        'description': '结合有氧运动、力量训练和瑜伽的综合减脂课程。每节课包含热身、HIIT训练、力量塑形和拉伸放松。适合有减脂塑形需求的成人。',
        'max_students': 30, 'price': 880.00,
        'start_date': today + timedelta(days=3), 'end_date': today + timedelta(days=33),
        'schedule': '每周一至五 06:30-07:30', 'status': 'enrolling',
    },
    {
        'name': '瑜伽身心平衡课',
        'coach': coaches[6], 'venue': venues[9], 'course_type': 'other',
        'description': '传统哈他瑜伽与现代流瑜伽相结合的课程。通过体式练习、呼吸法和冥想放松，改善体态、增强柔韧性、缓解压力。',
        'max_students': 20, 'price': 680.00,
        'start_date': today + timedelta(days=14), 'end_date': today + timedelta(days=44),
        'schedule': '每周二、四 19:00-20:00', 'status': 'enrolling',
    },
    {
        'name': '排球青少年集训',
        'coach': coaches[7], 'venue': venues[10], 'course_type': 'other',
        'description': '面向12-18岁青少年的排球集训课程。系统学习发球、垫球、传球、扣球、拦网等技术，以及团队配合和比赛战术。',
        'max_students': 18, 'price': 1200.00,
        'start_date': today + timedelta(days=5), 'end_date': today + timedelta(days=95),
        'schedule': '每周六、日 14:00-16:00', 'status': 'enrolling',
    },
    {
        'name': 'CF体适能训练营',
        'coach': coaches[6], 'venue': venues[0], 'course_type': 'fitness',
        'description': '高强度功能性训练课程，融合举重、体操和有氧训练元素。每天不同的训练计划，全面提升力量、耐力、速度、协调性等综合体能素质。',
        'max_students': 15, 'price': 1080.00,
        'start_date': today + timedelta(days=-30), 'end_date': today + timedelta(days=60),
        'schedule': '每周一至五 18:00-19:00', 'status': 'in_progress',
    },
]

for data in courses_data:
    course = Course.objects.create(**data)
    print(f'课程: {course.name} | 教练: {course.coach.name} | 场馆: {course.venue.name} | ¥{course.price} | {course.get_status_display()}')

# 给进行中的课程添加一些学员（报名操作）
from bookings.models import Booking
users = list(User.objects.filter(user_type='user')[:5])
if users:
    in_progress_courses = Course.objects.filter(status='in_progress')
    for course in in_progress_courses:
        for i, user in enumerate(users[:3]):
            if not CourseEnrollment.objects.filter(course=course, user=user).exists():
                CourseEnrollment.objects.create(course=course, user=user, status='enrolled')
                print(f'  学员: {user.username} 报名了 {course.name}')

print('\n=== 生成完成 ===')
print(f'教练: {Coach.objects.count()} 人')
print(f'课程: {Course.objects.count()} 门')
print(f'报名记录: {CourseEnrollment.objects.count()} 条')
