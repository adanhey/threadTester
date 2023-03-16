from SQLconnect.db_file import *
from Flask_part.flask_job import permission


@app.route('/createInterface', methods=['POST'])
@permission
def create_interface():
    require_data = ['name', 'method', 'uri', 'data_type', 'project_id']
    full_data = ['name', 'method', 'uri', 'data_type', 'project_id']
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
            elif Interface.query.filter(Interface.name == interface_info[i]['name']).first():
                add_result.append(f"第{i + 1}条数据：名称{interface_info[i]['name']}已存在")
            elif not Project.query.filter(Project.id == interface_info[i]['project_id']).first():
                add_result.append(f"第{i + 1}条数据：项目id{interface_info[i]['project_id']}不存在")
            else:
                for data in full_data:
                    if data in interface_info[i]:
                        exec(f"{data} = interface_info[i]['{data}']")
                    else:
                        exec(f"{data} = ''")
                interface1 = eval(
                    "Interface(name=name, method=method, uri=uri, data_type=data_type, project_id=project_id)")
                db.session.add(interface1)
        db.session.commit()
        return {"失败结果": add_result}
    else:
        return {"message": "请求体错误"}, 400


@app.route('/updateInterface', methods=['POST'])
@permission
def update_interface():
    require_data = ['id']
    full_data = ['name', 'method', 'uri', 'data_type', 'project_id']
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
            elif Interface.query.filter(Interface.name == interface_info[i]['name'],
                                        Interface.id != interface_info[i]['id']).first():
                add_result.append(f"第{i + 1}条数据：名称{interface_info[i]['name']}已存在")
            elif not Project.query.filter(Project.id == interface_info[i]['project_id']).first():
                add_result.append(f"第{i + 1}条数据：项目id{interface_info[i]['project_id']}不存在")
            elif not Interface.query.filter(Interface.id == interface_info[i]['id']).first():
                add_result.append(f"第{i + 1}条数据：id不存在")
            else:
                interface1 = Interface.query.filter(Interface.id == interface_info[i]['id']).first()
                for data in full_data:
                    if data in interface_info[i]:
                        exec(f"interface1.{data} = interface_info[i]['{data}']")
        db.session.commit()
        return {"失败结果": add_result}
    else:
        return {"message": "请求体错误"}, 400


@app.route('/deleteInterface', methods=['DELETE'])
@permission
def delete_interface():
    del_id = request.args.get("id")
    if not del_id:
        return {"message": "请求params缺少id"}, 400
    elif not Interface.query.filter(Interface.id == del_id).first():
        return {"message": "资源不存在"}, 404
    else:
        Interface1 = Interface.query.filter(Interface.id == del_id).first()
        db.session.delete(Interface1)
        db.session.commit()
    return {"message": "删除成功"}


@app.route('/listInterface', methods=['GET'])
@permission
def list_interface():
    select_pam = ['project_id', 'title', 'publishing_office', 'isbn']
    select_str = ""
    if not request.args.get('project_id'):
        return {"message": "缺失项目id"}
    for pam in select_pam:
        exec(f"{pam} = request.args.get('{pam}')")
        if eval(f"{pam}"):
            select_str += f"Interface.{pam} == {pam}"
    result = eval(f"Interface.query.filter({select_str}).all()")
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
