"""
健康助手评测主程序
功能：读取测试用例 → 调用健康助手 → 关键词校验 → AI评委评分 → 生成报告
"""

import csv
import json
import os
import time
from datetime import datetime

import requests

from health_assistant_eval.ai_judge import llm_judge

# ============== 配置 ==============
DIFY_API_KEY = os.environ["DIFY_API_KEY"]
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"


# ============== 函数1: 调用健康助手 ==============
def call_health_assistant(question, health_data=""):
    """调用Dify工作流获取回答"""
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {
            "user_message": question,
            "username": "ai_test_user",
            "health_data": health_data
        },
        "query": question,
        "user": "ai_test_user",
        "response_mode": "blocking",
    }

    last_error = None
    for retry in range(3):
        try:
            response = requests.post(
                DIFY_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "")
            return answer
        except requests.RequestException as e:
            last_error = e
            time.sleep(1)

    return f"调用dify失败: {last_error}"


# ============== 函数2: 清洗AI回答 ==============
def clean_answer(answer):
    """清洗思考过程，只保留最终回答"""
    if answer is None:
        return ""

    end_tag = "</think>"
    if end_tag in answer:
        return answer.split(end_tag, 1)[1].strip()

    return answer.strip()


# ============== 函数3: 分割关键词 ==============
def split_words(text):
    """按|分割关键词"""
    if not text:
        return []
    return [item.strip() for item in text.split("|") if item.strip()]


# ============== 函数4: 关键词校验 ==============
def keyword_check(answer, must_have, must_not_have):
    """校验回答中的关键词"""
    must_have_words = split_words(must_have)
    must_not_have_words = split_words(must_not_have)

    missing_words = [word for word in must_have_words if word not in answer]
    forbidden_words = [word for word in must_not_have_words if word in answer]

    passed = len(missing_words) == 0 and len(forbidden_words) == 0

    return {
        "passed": passed,
        "forbidden": forbidden_words,
        "missing_words": missing_words,
    }


# ============== 函数5: 处理单个用例 ==============
def process_one_case(row):
    """处理单个测试用例（可并发执行）"""
    question = row["question"]

    # 1. 调用健康助手
    raw_answer = call_health_assistant(question)
    answer = clean_answer(raw_answer)

    # 2. 关键词校验
    kw_check = keyword_check(
        answer=answer,
        must_have=row["must_have"],
        must_not_have=row["must_not_have"]
    )

    # 3. AI评委评分
    judge = llm_judge(
        question=question,
        expected_intent=row["expected_intent"],
        expected_keywords=row["expected_keywords"],
        actual_answer=answer
    )

    # 4. 汇总结果
    llm_passed = judge.get("passed", False)
    final_passed = kw_check["passed"] and llm_passed

    return {
        "case_id": row["case_id"],
        "category": row["category"],
        "question": question,
        "expected_intent": row["expected_intent"],
        "actual_answer": answer,
        "kw_passed": "PASS" if kw_check["passed"] else "FAIL",
        "missing_words": "|".join(kw_check["missing_words"]),
        "forbidden_words": "|".join(kw_check["forbidden"]),
        "intent_correct": "PASS" if judge.get("intent_correct", False) else "FAIL",
        "intent_score": judge.get("intent_score", 0),
        "relevance_score": judge.get("relevance_score", 0),
        "safety_score": judge.get("safety_score", 0),
        "format_score": judge.get("format_score", 0),
        "llm_score": judge.get("overall_score", 0),
        "llm_passed": "PASS" if llm_passed else "FAIL",
        "llm_reason": judge.get("reason", ""),
        "suggestion": judge.get("suggestion", ""),
        "final_passed": "PASS" if final_passed else "FAIL",
        "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ============== 函数6: 执行评测（并发版） ==============
def run_eval(input_file, output_file):
    """串行执行评测流程"""
    # 读取所有用例
    with open(input_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    print(f"共 {total} 个用例，逐个执行")

    results = []
    start_time = time.time()

    # 逐个执行
    for i, row in enumerate(rows, 1):
        try:
            result = process_one_case(row)
            results.append(result)
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = avg_time * (total - i)
            print(f"[{i}/{total}] {result['question'][:25]}... | 耗时: {elapsed:.1f}s | 预计剩余: {remaining:.0f}s")
        except Exception as e:
            print(f"[{i}/{total}] {row['question'][:25]}... | 错误: {e}")
            results.append({
                "case_id": row["case_id"],
                "category": row["category"],
                "question": row["question"],
                "expected_intent": row["expected_intent"],
                "actual_answer": f"测试失败: {e}",
                "kw_passed": "FAIL",
                "missing_words": "",
                "forbidden_words": "",
                "intent_correct": "FAIL",
                "intent_score": 0,
                "relevance_score": 0,
                "safety_score": 0,
                "format_score": 0,
                "llm_score": 0,
                "llm_passed": "FAIL",
                "llm_reason": str(e),
                "suggestion": "",
                "final_passed": "FAIL",
                "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

    total_time = time.time() - start_time

    # 写入CSV报告
    fieldnames = [
        "case_id", "category", "question", "expected_intent",
        "actual_answer", "kw_passed", "missing_words", "forbidden_words",
        "intent_correct", "intent_score", "relevance_score", "safety_score",
        "format_score", "llm_score", "llm_passed", "llm_reason",
        "suggestion", "final_passed", "run_time"
    ]

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # 打印统计
    total = len(results)
    kw_passed = sum(1 for r in results if r["kw_passed"] == "PASS")
    llm_passed = sum(1 for r in results if r["llm_passed"] == "PASS")
    final_passed = sum(1 for r in results if r["final_passed"] == "PASS")
    intent_correct = sum(1 for r in results if r["intent_correct"] == "PASS")

    avg_score = sum(r["llm_score"] for r in results) / total if total else 0
    avg_safety = sum(r["safety_score"] for r in results) / total if total else 0

    print("\n" + "=" * 50)
    print("健康助手评测报告")
    print("=" * 50)
    print(f"总用例数: {total}")
    print(f"总耗时: {total_time:.1f}秒")
    print(f"平均每用例: {total_time/total:.1f}秒")
    print(f"关键词通过: {kw_passed} ({kw_passed/total*100:.1f}%)")
    print(f"意图识别正确: {intent_correct} ({intent_correct/total*100:.1f}%)")
    print(f"AI评分通过: {llm_passed} ({llm_passed/total*100:.1f}%)")
    print(f"最终通过: {final_passed} ({final_passed/total*100:.1f}%)")
    print(f"平均分: {avg_score:.1f}")
    print(f"安全性平均分: {avg_safety:.1f}")
    print(f"结果文件: {output_file}")

    # 生成JSON格式报告（用于LangSmith记录）
    report = {
        "total": total,
        "keyword_pass_rate": f"{kw_passed/total*100:.1f}%",
        "intent_accuracy": f"{intent_correct/total*100:.1f}%",
        "llm_pass_rate": f"{llm_passed/total*100:.1f}%",
        "final_pass_rate": f"{final_passed/total*100:.1f}%",
        "avg_score": round(avg_score, 1),
        "avg_safety_score": round(avg_safety, 1),
        "results": results
    }

    with open(output_file.replace(".csv", ".json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


if __name__ == "__main__":
    run_eval("health_eval_cases.csv", "health_eval_results.csv")
