"""报社核心逻辑：稿件、版面、记者和印刷。"""

import json


def new_game():
    return {
        "articles": {},
        "layout_articles": [],
        "layout_capacity": 2,
        "layout_load": 0,
        "day": 1,
        "issue_id": 0,
        "reporters": {
            "R1": {"on_leave": False},
            "R2": {"on_leave": True},
        },
        "assignments": {},
        "printer_fault": False,
        "circulation": 0,
        "score": 100,
        "retracted": False,
    }


def _ensure_fields(state):
    state.setdefault("articles", {})
    state.setdefault("layout_articles", [])
    state.setdefault("layout_capacity", 2)
    state["layout_load"] = len(state["layout_articles"])
    state.setdefault("day", 1)
    state.setdefault("issue_id", 0)
    state.setdefault("reporters", {})
    state.setdefault("assignments", {})
    state.setdefault("printer_fault", False)
    state.setdefault("circulation", 0)
    state.setdefault("score", 100)
    state.setdefault("retracted", False)
    return state


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return _ensure_fields(json.loads(text))


def publish(state, article_id):
    if article_id in state["articles"]:
        return False
    state["articles"][article_id] = True
    return True


def layout(state, article_id):
    if article_id in state["layout_articles"]:
        return False
    if state["layout_load"] >= state["layout_capacity"]:
        return False
    state["layout_articles"].append(article_id)
    state["layout_load"] += 1
    return True


def fee(state, article_id, end_day):
    return end_day - state["day"]


def cancel_publish(state, article_id):
    if article_id in state["layout_articles"]:
        state["layout_articles"].remove(article_id)
        state["layout_load"] = len(state["layout_articles"])
    state["articles"].pop(article_id, None)
    return True


def assign(state, article_id, reporter):
    reporter_info = state["reporters"].get(reporter)
    if reporter_info is None or reporter_info.get("on_leave"):
        return False
    state["assignments"][article_id] = reporter
    return True


def print_issue(state):
    if state.get("printer_fault"):
        return False
    state["issue_id"] += 1
    state["circulation"] += state["layout_load"]
    state["layout_articles"] = []
    state["layout_load"] = 0
    state["articles"] = {}
    state["retracted"] = False
    return True


def retract(state):
    if state.get("retracted"):
        return False
    state["score"] = state.get("score", 100) - 10
    state["retracted"] = True
    return True


def main():
    state = new_game()
    print("报社 - 命令: publish/layout/fee/cancel/assign/print/retract/save/load/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        command, args = parts[0], parts[1:]
        try:
            if command == "publish":
                print(publish(state, args[0]))
            elif command == "layout":
                print(layout(state, args[0]))
            elif command == "fee":
                print(fee(state, args[0], int(args[1])))
            elif command == "cancel":
                print(cancel_publish(state, args[0]))
            elif command == "assign":
                print(assign(state, args[0], args[1]))
            elif command == "print":
                print(print_issue(state))
            elif command == "retract":
                print(retract(state))
            elif command == "save":
                print(save_state(state))
            elif command == "load":
                state = load_state(input("存档: "))
                print("ok")
            else:
                print("unknown command")
        except (IndexError, ValueError):
            print("bad arguments")


if __name__ == "__main__":
    main()
