from SQLconnect.db_file import *
from Flask_part.flask_job import permission


@app.route('/createField', methods=['POST'])
@permission
def create_field():
    require_data = ['interface_id', 'filed_name', 'data_type']
    full_data = ['interface_id', 'filed_name', 'data_type', 'data_from_interface', 'data_from_value_path',
                 'data_length', 'data_range', 'decimal_range', 'parent_field']
    interface_info = request.json
    if isinstance(interface_info, list):
        add_result = []
        for i in range(len(interface_info)):
            a = 0
            for require in require_data:
                if require not in interface_info[i]:
                    add_result.append(f"第{i + 1}条数据缺少{require}")
                    a = 1
                    break
            if a == 1:
                continue
            elif InterfaceField.query.filter(InterfaceField.filed_name == interface_info[i]['filed_name'],
                                             InterfaceField.interface_id == interface_info[i]['interface_id']).first():
                add_result.append(f"第{i + 1}条数据：接口下字段{interface_info[i]['name']}已存在")
            elif not Interface.query.filter(Interface.id == interface_info[i]['interface_id']).first():
                add_result.append(f"第{i + 1}条数据：接口id{interface_info[i]['interface_id']}不存在")
            else:
                add_str = ""
                for data in full_data:
                    if data in interface_info[i]:
                        exec(f"{data} = interface_info[i]['{data}']")
                    else:
                        exec(f"{data} = None")
                    add_str += f"{data}={data},"
                print(add_str)
                interface_field1 = eval(f"InterfaceField({add_str})")
                db.session.add(interface_field1)
        db.session.commit()
        return {"失败结果": add_result}
    else:
        return {"message": "请求体错误"}, 400


@app.route('/updateField', methods=['POST'])
@permission
def update_field():
    require_data = ['id']
    full_data = ['interface_id', 'filed_name', 'data_type', 'data_from_interface', 'data_from_value_path',
                 'data_length', 'data_range', 'decimal_range', 'parent_field']
    interface_info = request.json
    if isinstance(interface_info, list):
        add_result = []
        for i in range(len(interface_info)):
            a = 0
            for require in require_data:
                if require not in interface_info[i]:
                    add_result.append(f"第{i + 1}条数据缺少{require}")
                    a = 1
                    break
            if a == 1:
                continue
            elif InterfaceField.query.filter(InterfaceField.filed_name == interface_info[i]['filed_name'],
                                             InterfaceField.interface_id == interface_info[i]['interface_id'],
                                             InterfaceField.id != interface_info[i]['id']).first():
                add_result.append(f"第{i + 1}条数据：接口字段{interface_info[i]['name']}已存在")
            elif not Interface.query.filter(Interface.id == interface_info[i]['interface_id']).first():
                add_result.append(f"第{i + 1}条数据：接口id{interface_info[i]['interface_id']}不存在")
            elif not InterfaceField.query.filter(InterfaceField.id == interface_info[i]['id']).first():
                add_result.append(f"第{i + 1}条数据：id不存在")
            else:
                interface1 = InterfaceField.query.filter(InterfaceField.id == interface_info[i]['id']).first()
                for data in full_data:
                    if data in interface_info[i]:
                        exec(f"interface1.{data} = interface_info[i]['{data}']")
        db.session.commit()
        return {"失败结果": add_result}
    else:
        return {"message": "请求体错误"}, 400


@app.route('/deleteField', methods=['DELETE'])
@permission
def delete_interface():
    del_id = request.args.get("id")
    if not del_id:
        return {"message": "请求params缺少id"}, 400
    elif not InterfaceField.query.filter(InterfaceField.id == del_id).first():
        return {"message": "资源不存在"}, 404
    else:
        interface1 = InterfaceField.query.filter(InterfaceField.id == del_id).first()
        db.session.delete(interface1)
        db.session.commit()
    return {"message": "删除成功"}


@app.route('/listField', methods=['GET'])
@permission
def list_interface():
    select_pam = ['interface_id', 'filed_name', 'data_type']
    select_str = ""
    if not request.args.get('interface_id'):
        return {"message": "缺失接口id"}
    for pam in select_pam:
        exec(f"{pam} = request.args.get('{pam}')")
        if eval(f"{pam}"):
            select_str += f"InterfaceField.{pam} == {pam}"
    result = eval(f"InterfaceField.query.filter({select_str}).all()")
    res = []
    for i in result:
        mid_dic = {}
        for key, value in i.__dict__.items():
            if key == '_sa_instance_state':
                pass
            elif isinstance(value, datetime):
                mid_dic[key] = str(value)
            else:
                mid_dic[key] = value
        res.append(mid_dic)
    return {"查询结果": res}


if __name__ == "__main__":
    app.run(host='10.53.3.46')
