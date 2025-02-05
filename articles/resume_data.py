# blog/resume_data.py

resume_data_cn = {
            'personal_info': {
                'name': '张三',
                'title': '资深算法工程师',
                'avatar': 'images/avatar.jpg',
                'email': 'artemiseelu@gmail.com',
                'phone': '0123 456789',
                'location': '北京',
                'github': 'github.com/johndoe',
                'linkedin': 'linkedin.com/in/jiaxing-lu-6a0a16b4/',
                'summary': '5年全栈开发经验，专注于Python/Django开发，\
                      熟悉前端技术栈，具有良好的代码风格和团队协作能力。',
            },
            'skills': [
            {'name': 'Python/Django', 'level': 90},
            {'name': 'JavaScript/Vue', 'level': 85},
            {'name': 'HTML/CSS', 'level': 88},
            {'name': 'PostgreSQL', 'level': 82},
            {'name': 'Docker', 'level': 75},
            {'name': 'Linux', 'level': 80},
        ],
            'sections': {
                'about': '关于我',
                'skills': '技能专长',
                'contact': '联系方式',
                'experience': '工作经历',
                'projects': '项目经验',
                'education': '教育背景',
            },
         'experience': [
            {
                'company': 'XX科技有限公司',
                'title': '高级开发工程师',
                'period': '2020-至今',
                'description': [
                    '负责公司核心业务系统的开发和维护',
                    '优化系统性能，将接口响应时间降低50%',
                    '带领5人团队完成多个重要项目',
                ],
            },
            {
                'company': 'YY互联网公司',
                'title': '开发工程师',
                'period': '2018-2020',
                'description': [
                    '参与电商平台的开发',
                    '实现订单系统重构',
                    '编写技术文档和单元测试',
                ],
            },
        ],
        'projects': [
            {
                'name': '企业资源管理系统',
                'period': '2021-2022',
                'link': 'https://github.com/artemiseelu/blog',
                'description': '使用Django开发的企业级管理系统，\
                              包含人事、财务、库存等模块',
                'technologies': ['Python', 'Django', 'Vue.js', 'PostgreSQL'],
            },
            {
                'name': '在线教育平台',
                'period': '2020-2021',
                'description': '支持在线课程发布、视频播放、作业管理等功能',
                'technologies': ['Django REST framework', 'React', 'Redis'],
            },
        ],
        'education': [
            {
                'school': 'XX大学',
                'degree': '计算机科学与技术 学士',
                'period': '2014-2018',
                'description': '主修课程：数据结构、算法、计算机网络、数据库等',
            }
        ]
        }

resume_data_en = {
    'personal_info': {
        'name': 'John Doe',
        'title': 'Software Developer',
        'avatar': 'images/avatar.jpg',
        'email': 'john.doe@email.com',
        'phone': '0123 456789',
        'location': 'New York',
        'github': 'github.com/johndoe',
        'linkedin': 'linkedin.com/in/johndoe',
        'summary': 'Hi, my name is John Doe...',
    },
    'sections': {
        'about': 'About Me',
        'skills': 'Skills',
        'contact': 'Contact',
        'experience': 'Experience',
        'projects': 'Projects',
        'education': 'Education',
    },
}