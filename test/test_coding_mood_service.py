from codingmoodserver.coding_mood_service import (
    extract_number_of_failures,
    get_new_state,
)


class TestExtractNumberOfFailures:
    def test_no_failures(self):
        test_run_output = """
            ============================= test session starts ==============================
            platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
            rootdir: /home/mikeym/code/personal/AoS/add_drama_to_coding_session/CodingMoodServer
            plugins: asyncio-0.14.0
            collected 2 items

            test/test_websocket_manager.py ..                                        [100%]

            ============================== 2 passed in 0.03s ==============================="""

        assert extract_number_of_failures(test_run_output) == 0

    def test_some_failures(self):
        test_run_output = """
            ============================= test session starts ==============================
            platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
            rootdir: /home/mikeym/code/personal/AoS/add_drama_to_coding_session/CodingMoodServer
            plugins: asyncio-0.14.0
            collected 3 items

            test/test_coding_mood_service.py .                                       [ 33%]
            test/test_websocket_manager.py .F                                        [100%]

            =========================== short test summary info ============================
            FAILED test/test_websocket_manager.py::test_unregister_websockets - Assertion...
            ========================= 1 failed, 2 passed in 0.09s =========================="""

        assert extract_number_of_failures(test_run_output) == 1


class TestGetNewState:
    def test_unchanged_state(self):
        assert get_new_state(last_num_of_failures=0, num_of_failures=0) is None

    def test_broken_state(self):
        assert get_new_state(last_num_of_failures=0, num_of_failures=1) == {"state": "broken"}

    def test_working_state(self):
        assert get_new_state(last_num_of_failures=1, num_of_failures=0) == {"state": "working"}

    def test_fixing_state(self):
        assert get_new_state(last_num_of_failures=2, num_of_failures=1) == {"state": "fixing"}
