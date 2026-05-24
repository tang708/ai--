"""MySQL 辅助工具，用于数据一致性校验

为什么需要这层：接口测试不仅要验证 HTTP 响应，还要确认数据库真实落库。
例如注册接口返回成功，但需要查 j_user 表确认记录确实写入。
"""
import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from base_Tool.my_logger import mylogger


def get_connection():
    """创建新的 MySQL 连接 — 测试场景并发低，不需要连接池"""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,  # 返回字典，方便字段名访问
    )


def query_one(sql, params=None):
    """执行查询并返回单条结果"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()
    finally:
        conn.close()


def query_all(sql, params=None):
    """执行查询并返回全部结果"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def execute(sql, params=None):
    """执行写操作（INSERT/UPDATE/DELETE），自动 commit"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            affected = cur.execute(sql, params)
            conn.commit()
            return affected
    finally:
        conn.close()


def user_exists(username):
    """检查指定用户名是否存在（仅查未删除用户）"""
    row = query_one("SELECT id FROM j_user WHERE username=%s AND deleted=0", (username,))
    return row is not None


def get_user_by_username(username, include_deleted=False):
    """根据用户名获取用户完整信息

    include_deleted=False: 只查活跃用户（业务校验用）
    include_deleted=True: 含已删除用户（清理函数用，避免 deleted=1 的用户无法被清理）
    """
    sql = "SELECT * FROM j_user WHERE username=%s"
    if not include_deleted:
        sql += " AND deleted=0"
    return query_one(sql, (username,))


def delete_user_by_username(username):
    """硬删除测试用户，按外键依赖顺序清理四张表

    为什么硬删而非逻辑删：测试用户是临时数据，逻辑删会导致用户名唯一约束冲突。
    """
    user = get_user_by_username(username, include_deleted=True)
    if user:
        mylogger.info("清理测试用户: {}".format(username))
        execute("DELETE FROM j_user_role WHERE user_id=%s", (user["id"],))
        execute("DELETE FROM j_body WHERE id=%s", (user["id"],))
        execute("DELETE FROM j_body_notes WHERE name=%s", (user["username"],))
        execute("DELETE FROM j_user WHERE id=%s", (user["id"],))


def get_user_roles(user_id):
    """查询用户拥有的角色名列表，用于验证注册默认角色分配"""
    sql = """
        SELECT r.role_name FROM j_role r
        JOIN j_user_role ur ON r.role_id = ur.role_id
        WHERE ur.user_id = %s
    """
    rows = query_all(sql, (user_id,))
    return [r["role_name"] for r in rows]


def get_user_menus(user_id):
    """查询用户可见的菜单列表，用于验证 RBAC 权限分配"""
    sql = """
        SELECT m.title FROM j_menu m
        JOIN j_role_menu rm ON m.menu_id = rm.menu_id
        JOIN j_user_role ur ON rm.role_id = ur.role_id
        WHERE ur.user_id = %s
    """
    rows = query_all(sql, (user_id,))
    return [r["title"] for r in rows]
