from Flask_part.flask_job import permission
from SQLconnect.db_file import *


@app.route('/createProject', methods=['POST'])
@permission
def create_project():
    require_data = ['name', 'host', 'account', 'password']
    full_data = ['name', 'host', 'account', 'password', 'auth_method']
    interface_info = request.json
    for require in require_data:
        if require not in interface_info:
            return {"message": f"缺失{require}"}, 400
        elif Project.query.filter(Project.name == interface_info['name']).first():
            return {"message": f"环境{interface_info['name']}已存在"}, 400
    for data in full_data:
        if data in interface_info:
            exec(f"{data} = interface_info['{data}']")
        else:
            exec(f"{data} = ''")
    project1 = eval("Project(name=name, host=host, account=account, password=password, auth_method=auth_method)")
    db.session.add(project1)
    db.session.commit()
    return {"message": "添加成功"}


@app.route('/updateProject', methods=['POST'])
@permission
def update_project():
    require_data = ['id']
    full_data = ['name', 'host', 'account', 'password', 'auth_method']
    interface_info = request.json
    for require in require_data:
        if require not in interface_info:
            return {"message": f"缺失{require}"}, 400
        elif Project.query.filter(Project.name == interface_info['name'],
                                  Project.id != interface_info['id']).first():
            return {"message": f"{interface_info['name']}已存在"}, 400
        elif not Project.query.filter(Project.id == interface_info['id']).first():
            return {"message": f"id不存在"}, 404
        else:
            pro1 = Project.query.filter(Project.id == interface_info['id']).first()
            for data in full_data:
                if data in interface_info:
                    exec(f"pro1.{data} = interface_info['{data}']")
    db.session.commit()
    return {"message": "修改成功"}


@app.route('/deleteProject', methods=['DELETE'])
@permission
def delete_project():
    del_id = request.args.get("id")
    if not del_id:
        return {"message": "请求params缺少id"}, 400
    elif not Project.query.filter(Project.id == del_id).first():
        return {"message": "资源不存在"}, 404
    else:
        project1 = Project.query.filter(Project.id == del_id).first()
        db.session.delete(project1)
        db.session.commit()
    return {"message": "删除成功"}


@app.route('/listProject', methods=['GET'])
@permission
def list_project():
    select_pam = ['name', 'host']
    select_str = ""
    for pam in select_pam:
        exec(f"{pam} = request.args.get('{pam}')")
        if eval(f"{pam}"):
            select_str += f"Project.{pam} == {pam}"
    result = eval(f"Project.query.filter({select_str}).all()")
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