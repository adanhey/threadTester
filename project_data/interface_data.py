interfaces = {
    "员工列表": {
        "uri": "/es/workOrderStaffStatistics/queryStaff",
        "method": "post",
        "be_from_data": {
            "data_type": "json",
            "deptIds": [],
            "name": "PJPJ",
            "current": 1,
            "size": 20
        }
    },
    "客户列表": {
        "uri": "/es/customer/list2",
        "method": "post",
        "be_from_data": {
            "data_type": "json",
            "customerNumber": "",
            "fullName": "",
            "contactName": "",
            "employeeId": {
                "data_from": {
                    "interface_name": "员工列表",
                    "value_path": ["data", "records", 0, "employeeId"]
                }
            },
            "customerManagerId": "",
            "organizationIds": [],
            "labelIds": [],
            "current": 1,
            "size": 100
        }
    },
    "test": {
        "uri": "",
        "name": "",
        "method": "",
        "data_type": "json",
        "json": {
            "interface_data": {"data_from": {
                "interface_name": "客户列表",
                "value_path": ["data", "records", 0, "id"]
            }},
            "list_data": [{
                "list_mark": "list_data_1",
                "is_dict": 1,
                "str": {"data_length": 10, "data_type": "str"},
                "int": {"data_range": [0, 1000], "data_type": "int"},
                "float": {"data_range": [0, 1000], "decimal_range": [0, 999], "data_type": "float"},
            }, {"list_mark": "list_data_2", "data_length": 10, "data_type": "str"},
                {"list_mark": "list_data_3", "data_range": [0, 1000], "data_type": "int"}],
            "str": {"data_length": 10, "data_type": "str"},
            "int": {"data_range": [0, 1000], "data_type": "int"},
            "float": {"data_range": [0, 1000], "decimal_range": [0, 999], "data_type": "float"},
            "dict_data": {
                "is_dict": 1,
                "str": {"data_length": 10, "data_type": "str"},
                "int": {"data_range": [0, 1000], "data_type": "int"},
                "float": {"data_range": [0, 1000], "decimal_range": [0, 999], "data_type": "float"},
            }
        }
    },
    "新增产品类别": {
        "uri": "/es/sparePartsType/saveOrUpdate",
        "name": "新增产品类别",
        "method": "post",
        "data_type": "json",
        "json": {
            "typeName": {"data_length": 20, "data_type": "str"},
            "typeCode": {"data_length": 8, "data_type": "str"},
            "remark": {"data_length": 100, "data_type": "str"},
            "parentName": "",
            "parentId": 0,
        }
    }
}
