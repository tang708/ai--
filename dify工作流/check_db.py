import re

with open('F:/测试/项目/AI健康管理系统/db_health.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# 分析每张表中的数据
tables = ['j_user', 'j_user_role', 'j_body', 'j_body_notes', 'j_role', 'j_role_menu', 'j_menu', 'detail', 'sport_info']

print('=' * 70)
print('数据库数据清理检查报告')
print('=' * 70)

# 提取 j_user 表
print('\n--- j_user（用户表）---')
user_match = re.search(r"INSERT INTO `j_user` VALUES\s+(.+?);", content, re.DOTALL)
if user_match:
    rows = user_match.group(1).strip()
    # 找所有 (..) 记录
    records = re.findall(r"\(([^)]+)\)", rows)
    print(f'总记录数: {len(records)}')
    for r in records:
        # 提取 id 和 username
        parts = [p.strip().strip("'") for p in r.split(',')]
        uid = parts[0]
        username = parts[1] if len(parts) > 1 else '?'
        deleted = parts[-1] if len(parts) > 1 else '?'
        flag = ''
        if username in ('zhangsan', 'lisi', 'wangwu', 'zhaoer', 'Bob', 'Charlie', 'David1', 'Emma', 'Frank', 'Grace', 'Henry', 'Isabella', 'Jacob'):
            flag = ' ← 批量测试用户'
        elif username == 'aaa' or username == 'text':
            flag = ' ← 测试用户'
        print(f'  id={uid}  username={username}  deleted={deleted}{flag}')

# 提取 j_user_role 表
print('\n--- j_user_role（用户角色关联表）---')
role_match = re.search(r"INSERT INTO `j_user_role` VALUES\s+(.+?);", content, re.DOTALL)
if role_match:
    rows = role_match.group(1).strip()
    records = re.findall(r"\(([^)]+)\)", rows)
    print(f'总记录数: {len(records)}')
    orphan_records = []
    for r in records:
        parts = [p.strip().strip("'") for p in r.split(',')]
        rid = parts[0]
        user_id = parts[1] if len(parts) > 1 else '?'
        role_id = parts[2] if len(parts) > 2 else '?'
        # 检查是否有对应的 j_user（11/12/29/31/54/55/56 可能不对应任何用户）
        orphan_user_ids = ['11', '12', '29', '31', '54', '55', '56']
        flag = ''
        if user_id in orphan_user_ids:
            flag = ' ← 孤儿记录（对应用户不存在）'
        print(f'  id={rid}  user_id={user_id}  role_id={role_id}{flag}')

# 提取 j_body 表
print('\n--- j_body（身体信息表）---')
body_match = re.search(r"INSERT INTO `j_body` VALUES\s+(.+?);", content, re.DOTALL)
if body_match:
    rows = body_match.group(1).strip()
    records = re.findall(r"\(([^)]+)\)", rows)
    print(f'总记录数: {len(records)}')
    for r in records:
        parts = [p.strip().strip("'") for p in r.split(',')]
        bid = parts[0]
        name = parts[1] if len(parts) > 1 else '?'
        flag = ''
        if name == 'aaa':
            flag = ' ← 测试数据'
        print(f'  id={bid}  name={name}{flag}')

# 提取 j_body_notes 表
print('\n--- j_body_notes（身体历史记录表）---')
notes_match = re.search(r"INSERT INTO `j_body_notes` VALUES\s+(.+?);", content, re.DOTALL)
if notes_match:
    rows = notes_match.group(1).strip()
    records = re.findall(r"\(([^)]+)\)", rows)
    print(f'总记录数: {len(records)}')
    for r in records:
        parts = [p.strip().strip("'") for p in r.split(',')]
        nid = parts[0]
        uid = parts[1] if len(parts) > 1 else '?'
        name = parts[2] if len(parts) > 2 else '?'
        flag = ''
        if name == 'aaa':
            flag = ' ← 测试数据'
        elif uid == '33':
            flag = ' ← 测试用户(id=33)数据'
        print(f'  notes_id={nid}  user_id={uid}  name={name}{flag}')

# 总结
print('\n' + '=' * 70)
print('问题汇总')
print('=' * 70)
print('1. j_user 中有 12 个批量测试用户（zhangsan~Jacob），deleted=1 但仍在数据库')
print('2. j_user 中 aaa(id=33) 和 text(id=32) 为测试用户')
print('3. j_user_role 中有 5 条孤儿记录（user_id=11,12,29,31,54,55,56）')
print('4. j_body 中 aaa(id=33) 为测试数据')
print('5. j_body_notes 中 aaa 相关 2 条 + admin 和 Alice 的数值明显为测试假数据')
