"""测试入口：pytest + Allure 报告生成

使用方式：
  python main.py              # 交互菜单
  python main.py 1            # 直接运行全部接口测试
  python main.py 5            # 全部测试 + 生成 HTML 报告
"""
import os
import sys
import pytest
from base_Tool.my_logger import mylogger

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(TESTS_DIR, "report", "json")
HTML_DIR = os.path.join(TESTS_DIR, "report", "html")
os.chdir(TESTS_DIR)


def run_all():
    """运行全部接口测试（case/ 下所有模块）"""
    mylogger.info("开始执行接口自动化测试用例".center(50, "*"))
    ret = pytest.main(["case/"])
    mylogger.info("接口自动化测试用例执行完成".center(50, "*"))
    print("\n{}".format("测试全部通过" if ret == 0 else "存在失败用例"))
    return ret


def run_module(module):
    """运行指定测试模块"""
    mylogger.info("开始执行: {}".format(module))
    ret = pytest.main([module])
    print("\n{}".format("通过" if ret == 0 else "存在失败用例"))
    return ret


def generate_report():
    """调用 allure CLI 生成 HTML 报告（需提前安装 allure 命令行工具）"""
    mylogger.info("开始生成测试报告。。。。。。。。。。。")
    cmd = "allure generate {} -o {} --clean".format(JSON_DIR, HTML_DIR)
    ret = os.system(cmd)
    if ret == 0:
        mylogger.info("测试报告生成成功。。。。。。。。。。。")
        print("  报告已生成: {}".format(HTML_DIR))
        print("  打开: {}".format(os.path.join(HTML_DIR, "index.html")))
    else:
        print("\n[!] Allure CLI 未安装，跳过 HTML 报告")
        print("    安装: scoop install allure")
    return ret


def print_menu():
    """打印交互式菜单"""
    print("=" * 50)
    print("  AI健康管理系统 — 接口自动化测试")
    print("=" * 50)
    print("  1. 运行全部接口测试")
    print("  2. 运行登录注册测试")
    print("  3. 运行用户管理测试")
    print("  4. 运行核心业务链路测试")
    print("  5. 全部测试 + 生成 HTML 报告")
    print("  0. 退出")
    print("=" * 50)


def main():
    """入口函数：支持命令行参数或交互菜单两种模式"""
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print_menu()
        choice = input("请选择: ").strip()

    if choice == "1":
        sys.exit(run_all())
    elif choice == "2":
        sys.exit(run_module("case/登录注册/test_登录注册.py"))
    elif choice == "3":
        sys.exit(run_module("case/用户管理/test_用户管理.py"))
    elif choice == "4":
        sys.exit(run_module("case/核心流程/test_核心流程.py"))
    elif choice == "5":
        ret = run_all()
        if ret == 0:
            generate_report()
        sys.exit(ret)
    elif choice == "0":
        print("退出")
    else:
        print("无效选项")


if __name__ == "__main__":
    main()
