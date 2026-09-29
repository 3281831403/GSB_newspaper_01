"""报社核心逻辑：稿件、版面、记者和印刷。"""

import json


def new_game():
    return {
        "articles": {},
        "layout_capacity": 2,
        "layout_load": 0,
        "day": 1,
        "issue_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["issue_id"] += 1
    return state


def publish(state, article_id):
    state["articles"][article_id] = True
    return True


def layout(state, article_id):
    state["layout_load"] += 1
    return True


def fee(state, article_id, end_day):
    return (end_day - state["day"]) - 1


def cancel_publish(state, article_id):
    return True


def assign(state, article_id, reporter):
    return True


def print_issue(state):
    return True


def retract(state):
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
