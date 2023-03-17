from Flask_part.flask_job import permission
from SQLconnect.db_file import *


@app.route('/createEnv', methods=['POST'])
@permission
def create_projectenv():
    require_data = ['project_id', 'name', 'host', 'account', 'password']
    full_data = ['project_id', 'name', 'host', 'account', 'password']
    interface_info = request.json
    for require in require_data:
        if require not in interface_info:
            return {"message": f"缺失{require}"}, 400
        elif ProjectEnv.query.filter(ProjectEnv.name == interface_info['name'],
                                     ProjectEnv.project_id == interface_info['project_id']).first():
            return {"message": f"项目环境{interface_info['name']}已存在"}, 400
    add_str = ""
    for data in full_data:
        if data in interface_info:
            exec(f"{data} = interface_info['{data}']")
        else:
            exec(f"{data} = ''")
        add_str += f"{data}={data},"
    project1 = eval(f"ProjectEnv({add_str})")
    db.session.add(project1)
    db.session.commit()
    return {"message": "添加成功"}


@app.route('/updateEnv', methods=['POST'])
@permission
def update_projectenv():
    require_data = ['id']
    full_data = ['id', 'project_id', 'name', 'host', 'account', 'password']
    interface_info = request.json
    for require in require_data:
        if require not in interface_info:
            return {"message": f"缺失{require}"}, 400
        elif ProjectEnv.query.filter(ProjectEnv.name == interface_info['name'],
                                     ProjectEnv.project_id == interface_info['project_id'],
                                     ProjectEnv.id != interface_info['id']).first():
            return {"message": f"项目下{interface_info['name']}已存在"}, 400
        elif not Project.query.filter(Project.id == interface_info['project_id']).first():
            return {"message": f"项目id不存在"}, 404
        else:
            pro1 = ProjectEnv.query.filter(ProjectEnv.id == interface_info['id']).first()
            for data in full_data:
                if data in interface_info:
                    exec(f"pro1.{data} = interface_info['{data}']")
    db.session.commit()
    return {"message": "修改成功"}


@app.route('/deleteEnv', methods=['DELETE'])
@permission
def delete_projectenv():
    del_id = request.args.get("id")
    if not del_id:
        return {"message": "请求params缺少id"}, 400
    elif not ProjectEnv.query.filter(ProjectEnv.id == del_id).first():
        return {"message": "资源不存在"}, 404
    else:
        project1 = ProjectEnv.query.filter(ProjectEnv.id == del_id).first()
        db.session.delete(project1)
        db.session.commit()
    return {"message": "删除成功"}


@app.route('/listEnv', methods=['GET'])
@permission
def list_projectenv():
    select_pam = ['project_id', 'name', 'host']
    select_str = ""
    for pam in select_pam:
        exec(f"{pam} = request.args.get('{pam}')")
        if eval(f"{pam}"):
            select_str += f"ProjectEnv.{pam} == {pam}"
    result = eval(f"ProjectEnv.query.filter({select_str}).all()")
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
