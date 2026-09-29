"""报社核心逻辑：稿件、版面、记者和印刷。"""

import json


def new_game():
    return {
        "articles": {},
        "layout_capacity": 2,
        "layout_load": 0,
        "day": 1,
        "issue_id": 0,
        "reporters": {"R1": {"leave": False}, "R2": {"leave": True}},
        "assignments": {},
        "printer_fault": False,
        "circulation": 0,
        "score": 100,
        "retracted_issues": [],
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def publish(state, article_id):
    articles = state.setdefault("articles", {})
    if articles.get(article_id):
        return False
    articles[article_id] = True
    return True


def layout(state, article_id):
    articles = state.setdefault("articles", {})
    if not articles.get(article_id):
        return False
    if state.get("layout_load", 0) >= state.get("layout_capacity", 0):
        return False
    state["layout_load"] = state.get("layout_load", 0) + 1
    return True


def fee(state, article_id, end_day):
    return end_day - state.get("day", 1)


def cancel_publish(state, article_id):
    articles = state.setdefault("articles", {})
    if not articles.pop(article_id, False):
        return False
    state.setdefault("assignments", {}).pop(article_id, None)
    if state.get("layout_load", 0) > 0:
        state["layout_load"] -= 1
    return True


def assign(state, article_id, reporter):
    reporters = state.setdefault("reporters", {})
    info = reporters.get(reporter)
    if not info or info.get("leave"):
        return False
    state.setdefault("assignments", {})[article_id] = reporter
    return True


def print_issue(state):
    if state.get("printer_fault"):
        return False
    state["issue_id"] = state.get("issue_id", 0) + 1
    state["circulation"] = state.get("circulation", 0) + state.get("layout_load", 0)
    return True


def retract(state):
    issue_id = state.get("issue_id", 0)
    retracted = state.setdefault("retracted_issues", [])
    if issue_id in retracted:
        return False
    retracted.append(issue_id)
    state["score"] = state.get("score", 0) - 10
    return True


def main():
    print("报社 - 命令: publish/layout/fee/cancel/assign/print/retract/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
