import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_publish(self):
        state = core.new_game()
        self.assertTrue(core.publish(state, "A1"))
        self.assertFalse(core.publish(state, "A1"))

    def test_02_layout_capacity(self):
        state = core.new_game()
        core.layout(state, "A1")
        core.layout(state, "A2")
        result = core.layout(state, "A3")
        self.assertFalse(result)

    def test_03_fee_exact(self):
        state = core.new_game()
        self.assertEqual(core.fee(state, "A1", 4), 3)

    def test_04_cancel_publish_releases_layout(self):
        state = core.new_game()
        core.layout(state, "A1")
        core.cancel_publish(state, "A1")
        self.assertEqual(state["layout_load"], 0)

    def test_05_no_assign_to_offline_reporter(self):
        state = core.new_game()
        result = core.assign(state, "A1", "R2")
        self.assertFalse(result)

    def test_06_no_print_on_fault(self):
        state = core.new_game()
        state["printer_fault"] = True
        result = core.print_issue(state)
        self.assertFalse(result)

    def test_07_retract_once(self):
        state = core.new_game()
        state["score"] = 100
        core.retract(state)
        self.assertEqual(state["score"], 90)

    def test_08_load_preserves_issue(self):
        state = core.new_game()
        state["issue_id"] = 3
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["issue_id"], 3)


if __name__ == "__main__":
    unittest.main()
