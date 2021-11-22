import unittest

import tasks
from textwrap import dedent
from utilities import *


class TestTasksFunctions(unittest.TestCase):

    def test_tasks_add(self):
        test1_add_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'REALLY first',
             'time_spent': '1:00',
             'notes': '',
             'completed': False},
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_new_task = {
            'name': 'REALLY first',
            'time_spent': '1:00',
            'notes': '',
            'completed': False
        }
        test1_actual = tasks.add(test1_add_list, test1_new_task, 0)
        self.assertEqual(test1_expected, test1_actual)

        # test adding to empty list
        test2_add_list = []
        test2_expected = [
            {'name': 'First',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test2_new_task = {
            'name': 'First',
            'time_spent': '0:25',
            'notes': '',
            'completed': False
        }
        test2_actual = tasks.add(test2_add_list, test2_new_task)
        self.assertEqual(test2_expected, test2_actual)

    def test_tasks_update(self):
        test1_update_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'Number 1',
             'time_spent': '1:00',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_updated_task = {**test1_update_list[0],
                              'name': 'Number 1',
                              'time_spent': '1:00'}
        test1_actual = tasks.update(test1_update_list, test1_updated_task, 0)
        self.assertEqual(test1_expected, test1_actual)

    def test_set_completion(self):
        test1_set_completion_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_actual = tasks.set_completion(test1_set_completion_list, 0)
        self.assertEqual(test1_expected, test1_actual)

    def test_tasks_delete(self):
        test1_delete_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True}
        ]
        test1_actual = tasks.delete(test1_delete_list, 2)
        self.assertEqual(test1_expected, test1_actual)

    def test_tasks_move(self):
        test1_move_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True}
        ]
        test1_actual = tasks.move(test1_move_list, 2, 0)
        self.assertEqual(test1_expected, test1_actual)

    def test_tasks_reduce(self):
        test1_reduce_list = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Second task',
             'time_spent': '0:25',
             'notes': '',
             'completed': True},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_expected = [
            {'name': 'First task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False},
            {'name': 'Third task',
             'time_spent': '0:25',
             'notes': '',
             'completed': False}
        ]
        test1_actual = tasks.reduce(test1_reduce_list)
        self.assertEqual(test1_expected, test1_actual)


class TestUtilitiesFunctions(unittest.TestCase):

    def test_parse_tasks(self):
        test1_tod_file = dedent('''\
            [MAIN]
            [ ] Example 1 (0:00)
            [X] Example 2 (1:01)''')

        test1_expected = {
            'MAIN': [
                {'name': 'Example 1',
                 'time_spent': '0:00',
                 'notes': '',
                 'completed': False},
                {'name': 'Example 2',
                 'time_spent': '1:01',
                 'notes': '',
                 'completed': True}
            ]
        }
        test1_actual = parse_tasks(test1_tod_file)
        self.assertEqual(test1_actual, test1_expected)

        test2_tod_file = ' '
        test2_expected = {
            'MAIN': list()
        }
        test2_actual = parse_tasks(test2_tod_file)
        self.assertEqual(test2_expected, test2_actual)

    def test_parse_tasks_with_notes(self):
        test1_tod_file = dedent('''\
            [MAIN]
            [ ] Example 1 (0:00)
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            [X] Example 2 (1:01)''')
        test1_expected = {
            'MAIN': [
                {'name': 'Example 1',
                 'time_spent': '0:00',
                 'notes': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                 'completed': False},
                {'name': 'Example 2',
                 'time_spent': '1:01',
                 'notes': '',
                 'completed': True}
            ]
        }
        test1_actual = parse_tasks(test1_tod_file)
        self.assertEqual(test1_actual, test1_expected)

    def test_format_seconds_to_time_spent(self):
        test1_time_input = 3660
        test1_expected = '1:01'
        test1_actual = format_seconds_to_time_spent(test1_time_input)
        self.assertEqual(test1_expected, test1_actual)

    def test_format_all_tasks_to_plaintext(self):
        test1_tasks = {
            'MAIN': [
                {'name': 'First task',
                 'time_spent': '0:25',
                 'notes': '',
                 'completed': False},
                {'name': 'Second task',
                 'time_spent': '0:25',
                 'notes': '',
                 'completed': True},
                {'name': 'Third task',
                 'time_spent': '0:25',
                 'notes': '',
                 'completed': False}
            ]
        }
        test1_expected = ("[ ] First task (0:25)\n" +
                          "[X] Second task (0:25)\n" +
                          "[ ] Third task (0:25)\n")
        test1_actual = format_all_tasks_to_plaintext(test1_tasks)
        self.assertEqual(test1_expected, test1_actual)

        test2_tasks = {
            'MAIN': [
                {'name': 'First task',
                 'time_spent': '0:25',
                 'notes': 'Lorem ipsum',
                 'completed': False},
                {'name': 'Second task',
                 'time_spent': '0:25',
                 'notes': '',
                 'completed': True},
                {'name': 'Third task',
                 'time_spent': '0:25',
                 'notes': '',
                 'completed': False}
            ]
        }
        test2_expected = ("[ ] First task (0:25)\n" +
                          "    Lorem ipsum\n"
                          "[X] Second task (0:25)\n" +
                          "[ ] Third task (0:25)\n")
        test2_actual = format_all_tasks_to_plaintext(test2_tasks)
        self.assertEqual(test2_expected, test2_actual)

    def test_convert_time_spent_to_seconds(self):
        test1_time_spent = '1:01'
        test1_expected = 3660
        test1_actual = convert_time_spent_to_seconds(test1_time_spent)
        self.assertEqual(test1_expected, test1_actual)


if __name__ == '__main__':
    unittest.main()
