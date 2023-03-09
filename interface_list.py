host = 'https://lijing.dataserver.cn'
interface_list = [
    {
        'name': '查询工单配置',
        'uri': '/es/orderType/list',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {},
        'data': {},
        'headers': ''
    },
    {
        'name': '查询诉求配置',
        'uri': '/es/appealType/list',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {},
        'data': {},
        'headers': ''
    },
    {
        'name': '查询组织树',
        'uri': '/es/department/getList',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {},
        'data': {},
        'headers': ''
    },
    {
        'name': '查询备件配置',
        'uri': '/es/sparePartsApprovalConfig/list',
        'thread_num': '',
        'run_time': 10,
        'method': 'get',
        'json': {},
        'data': {},
        'headers': ''
    },
    {
        'name': '客户列表',
        'uri': '/es/customer/list2',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {
            "customerNumber": "",
            "fullName": "",
            "contactName": "",
            "employeeId": "",
            "customerManagerId": "",
            "organizationIds": [],
            "labelIds": [],
            "current": 1,
            "size": 100
        },
        'data': {},
        'headers': ''
    },
    {
        'name': '工单列表',
        'uri': '/es/order/list',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {
            "startTime": "2023-01-28 00:00:00",
            "endTime": "2023-02-27 23:59:59",
            "all": 1,
            "current": 1,
            "size": 100
        },
        'data': {},
        'headers': ''
    },
    {
        'name': '诉求列表',
        'uri': '/es/appeal/list',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {
            "startTime": "2023-01-28",
            "endTime": "2023-02-27",
            "status": [],
            "current": 1,
            "size": 100
        },
        'data': {},
        'headers': ''
    },
    {
        'name': '员工列表',
        'uri': '/es/employee/list',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {
            "jobNumber": "",
            "name": "",
            "jobKey": "",
            "deptId": "825810650775506944",
            "current": 1,
            "size": 20
        },
        'data': {},
        'headers': ''
    },
    {
        'name': '产品列表',
        'uri': '/es/product/getPage',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {
            "current": 1,
            "size": 20
        },
        'data': {},
        'headers': ''
    },
    {
        'name': '产品型号列表',
        'uri': '/es/productModel/getPage',
        'thread_num': '',
        'run_time': 10,
        'method': 'post',
        'json': {
            "modelCode": "",
            "modelName": "",
            "current": 1,
            "size": 20
        },
        'data': {},
        'headers': ''
    },
]
# 通过率，并发数，响应时间，响应结果，失败率最高的接口
