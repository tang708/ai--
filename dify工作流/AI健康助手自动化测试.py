import os
from dotenv import load_dotenv
load_dotenv('F:/jinAI/.env')

# 配置文件（从环境变量读取）
DIFY_API_KEY = os.getenv('DIFY_API_KEY')
DIFY_API_URL = os.getenv('DIFY_API_URL', 'https://api.dify.ai/v1/chat-messages')
RUN_TIMES = 3  # 每个用例跑几次

# ============================================================

import csv
import json
import time
import sys
import requests
from datetime import datetime
from collections import defaultdict


# ============= 函数1：调用 AI 助手的 chat-messages API =============
def call_ai_assistant(question):
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": question,
        "user": "ai_test_user",
        "response_mode": "blocking",
        "inputs": {
            "user_message": question,
            "username": "ai_test_user",
            "health_data": ""
        }
    }

    last_error = None
    for retry in range(3):
        try:
            start = time.time()
            response = requests.post(DIFY_API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            elapsed = time.time() - start
            data = response.json()
            answer = data.get("answer", "")
            # 去掉 think 标签只保留正文
            if "</think>" in answer:
                answer = answer.split("</think>", 1)[-1].strip()
            return answer, elapsed
        except requests.RequestException as e:
            last_error = e
            time.sleep(2)

    return f"[调用失败] {last_error}", 0


# ============= 函数2：分割关键字 =============
def split_keywords(text):
    if not text:
        return []
    return [w.strip() for w in text.split("|") if w.strip()]


# ============= 函数3：关键字校验 =============
def keyword_check(answer, must_have_str, must_not_have_str):
    must_have_words = split_keywords(must_have_str)
    must_not_have_words = split_keywords(must_not_have_str)

    missing = [w for w in must_have_words if w not in answer]
    forbidden = [w for w in must_not_have_words if w in answer]

    passed = len(missing) == 0 and len(forbidden) == 0
    return {
        "passed": passed,
        "missing": missing,
        "forbidden": forbidden,
    }


# ============= 函数4：主执行流程 =============
def run_eval(csv_file, output_file):
    results = []
    elapsed_times = []

    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cases = list(reader)

    total_runs = len(cases) * RUN_TIMES
    current = 0

    for case in cases:
        case_id = case["case_id"]
        question = case["question"]
        case_type = case["type"]
        category = case["category"]
        must_have = case["must_have"]
        must_not_have = case["must_not_have"]

        case_results = []

        for i in range(RUN_TIMES):
            current += 1
            print(f"[{current}/{total_runs}] {case_id} 第{i+1}次: {question}", end=" ")

            try:
                answer, elapsed = call_ai_assistant(question)
                elapsed_times.append(elapsed)
                check = keyword_check(answer, must_have, must_not_have)

                status = "PASS" if check["passed"] else "FAIL"
                print(f"{status} ({elapsed:.1f}s)", end="")
                if not check["passed"]:
                    if check["missing"]:
                        print(f" 缺失:{check['missing']}", end="")
                    if check["forbidden"]:
                        print(f" 违禁:{check['forbidden']}", end="")
                print()

                case_results.append({
                    "run": i + 1,
                    "passed": check["passed"],
                    "answer": answer[:300],
                    "missing": check["missing"],
                    "forbidden": check["forbidden"],
                    "elapsed": elapsed,
                })
            except Exception as e:
                print(f"异常: {e}")
                case_results.append({
                    "run": i + 1,
                    "passed": False,
                    "answer": f"异常: {e}",
                    "missing": [],
                    "forbidden": [],
                    "elapsed": 0,
                })

            time.sleep(0.5)  # 避免限流

        pass_count = sum(1 for r in case_results if r["passed"])
        results.append({
            "case_id": case_id,
            "type": case_type,
            "category": category,
            "question": question,
            "must_have": must_have,
            "must_not_have": must_not_have,
            "pass_rate": f"{pass_count}/{RUN_TIMES}",
            "details": case_results,
        })

    # ============= 生成报告 =============
    print("\n" + "=" * 60)
    print("           AI健康助手 自动化测试报告")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"用例总数: {len(cases)}  每个跑 {RUN_TIMES} 次  共 {total_runs} 次\n")

    # 按类型统计
    type_stats = defaultdict(lambda: {"pass": 0, "total": 0})
    for r in results:
        t = r["type"]
        for d in r["details"]:
            type_stats[t]["total"] += 1
            if d["passed"]:
                type_stats[t]["pass"] += 1

    print("类型              通过     总数    通过率")
    print("-" * 45)
    for t in sorted(type_stats.keys()):
        s = type_stats[t]
        rate = s["pass"] / s["total"] * 100 if s["total"] else 0
        print(f"{t:<16} {s['pass']}/{s['total']:<5}  {rate:.0f}%")

    total_pass = sum(s["pass"] for s in type_stats.values())
    total_all = sum(s["total"] for s in type_stats.values())
    print("-" * 45)
    print(f"{'总计':<16} {total_pass}/{total_all:<5}  {total_pass/total_all*100:.0f}%")

    print(f"\n响应时间: 平均 {sum(elapsed_times)/len(elapsed_times):.1f}s  最慢 {max(elapsed_times):.1f}s  最快 {min(elapsed_times):.1f}s")

    # 失败用例汇总
    failed = [r for r in results if any(not d["passed"] for d in r["details"])]
    if failed:
        print(f"\n失败用例 ({len(failed)} 个):")
        for r in failed:
            print(f"  {r['case_id']} - {r['question'][:40]}")
            for d in r["details"]:
                if not d["passed"]:
                    print(f"    第{d['run']}次: 缺失={d['missing']} 违禁={d['forbidden']}")

    # 保存 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n详细结果: {output_file}")


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "AI健康助手测试用例.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "AI健康助手测试报告.json"
    run_eval(csv_file, output_file)
