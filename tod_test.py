import unittest

import tasks
from tasks import *
from utilities import *


class TestTasksFunctions(unittest.TestCase):

    def test_tasks_add(self):
        test1_add_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'REALLY first',
             'time_spent': '1:00',
             'completed': False},
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_actual = tasks.add(test1_add_list, 'REALLY first', '1:00', 0)
        self.assertEqual(test1_expected, test1_actual)

        # test adding to empty list
        test2_add_list = []
        test2_expected = [
            {'name': 'First',
             'time_spent': '0:25',
             'completed': False}
        ]
        test2_actual = tasks.add(test2_add_list, 'First', '0:25')
        self.assertEqual(test2_expected, test2_actual)

    def test_update_task(self):
        test1_update_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'Number 1',
             'time_spent': '1:00',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_actual = update_task(test1_update_list, 'Number 1', '1:00', 0)
        self.assertEqual(test1_expected, test1_actual)

    def test_set_completion(self):
        test1_set_completion_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_actual = tasks.set_completion(test1_set_completion_list, 0)
        self.assertEqual(test1_expected, test1_actual)

    def test_delete_task(self):
        test1_delete_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True}
        ]
        test1_actual = delete_task(test1_delete_list, 2)
        self.assertEqual(test1_expected, test1_actual)

    def test_move_task(self):
        test1_move_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True}
        ]
        test1_actual = move_task(test1_move_list, 2, 0)
        self.assertEqual(test1_expected, test1_actual)

    def test_reduce_tasks(self):
        test1_reduce_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_actual = reduce_tasks(test1_reduce_list)
        self.assertEqual(test1_expected, test1_actual)


class TestUtilitiesFunctions(unittest.TestCase):

    def test_get_tasks(self):
        test1_tod_file = '[ ] Example 1 (0:00)\n[X] Example 2 (1:01)'
        test1_expected = [
            {'name': 'Example 1',
             'time_spent': '0:00',
             'completed': False},
            {'name': 'Example 2',
             'time_spent': '1:01',
             'completed': True}
        ]
        test1_actual = get_tasks(test1_tod_file)
        self.assertEqual(test1_actual, test1_expected)

        test2_tod_file = ' '
        test2_expected = []
        test2_actual = get_tasks(test2_tod_file)
        self.assertEqual(test2_expected, test2_actual)

    def test_format_seconds_to_time_spent(self):
        test1_time_input = 3660
        test1_expected = '1:01'
        test1_actual = format_seconds_to_time_spent(test1_time_input)
        self.assertEqual(test1_expected, test1_actual)

    def test_format_tasks_to_plaintext(self):
        test1_tasks = [
            {'name': 'First task',
             'time_spent': '0:25',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'completed': False}
        ]
        test1_expected = ("[ ] First task (0:25)\n" +
                          "[X] Second task (0:25)\n" +
                          "[ ] Third task (0:25)")
        test1_actual = format_tasks_to_plaintext(test1_tasks)
        self.assertEqual(test1_expected, test1_actual)

    def test_convert_time_spent_to_seconds(self):
        test1_time_spent = '1:01'
        test1_expected = 3660
        test1_actual = convert_time_spent_to_seconds(test1_time_spent)
        self.assertEqual(test1_expected, test1_actual)


if __name__ == '__main__':
    unittest.main()
