from tod import *
import unittest


class TestTaskListMethods(unittest.TestCase):

    def test_add_task(self):
        test1_add_list = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False),
        ]
        test1_add_expected = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False),
            ('Last', '1:00', False)
        ]
        test1_add_actual = add_task(test1_add_list, 'Last', '1:00', 4)
        self.assertEqual(test1_add_expected, test1_add_actual)

        # test adding to empty list
        test2_add_list = []
        test2_add_expected = [('First', '0:25', False)]
        test2_add_actual = add_task(test2_add_list, 'First', '0:25', 0)
        self.assertEqual(test2_add_expected, test2_add_actual)

    def test_update_task(self):
        test1_update_list = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_update_expected = [
            ('Number 1', '1:00', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_update_actual = update_task(test1_update_list, 'Number 1', '1:00', 0)
        self.assertEqual(test1_update_actual, test1_update_expected)

    def test_set_completion(self):
        test1_set_completion_list = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_set_completion_expected = [
            ('First task', '0:25', True),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_set_completion_actual = set_completion(
            test1_set_completion_list, 0)
        self.assertEqual(
            test1_set_completion_actual, test1_set_completion_expected)

    def test_delete_task(self):
        test1_delete_list = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_delete_expected = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True)
        ]
        test1_delete_actual = delete_task(test1_delete_list, 2)
        self.assertEqual(test1_delete_actual, test1_delete_expected)

    def test_move_task(self):
        test1_move_list = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_move_expected = [
            ('Third task', '0:25', False),
            ('First task', '0:25', False),
            ('Second task', '0:25', True)
        ]
        test1_move_actual = move_task(test1_move_list, 2, 0)
        self.assertEqual(test1_move_actual, test1_move_expected)

    def test_reduce_tasks(self):
        test1_reduce_list = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False)
        ]
        test1_reduce_expected = [
            ('First task', '0:25', False),
            ('Third task', '0:25', False)
        ]
        test1_reduce_actual = reduce_tasks(test1_reduce_list)
        self.assertEqual(test1_reduce_actual, test1_reduce_expected)


if __name__ == '__main__':
    unittest.main()
