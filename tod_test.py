from tod import *
import unittest


class TestTaskListMethods(unittest.TestCase):

    test_tasks = [
        ('First task', '0:25', False),
        ('Second task', '0:25', True),
        ('Third task', '0:25', False)
    ]

    def test_add_task(self):
        test_tasks = [
            ('First task', '0:25', False),
            ('Second task', '0:25', True),
            ('Third task', '0:25', False),
            ('Last', '1:00', False)
        ]
        self.assertEqual(test_tasks, add_task(test_tasks, 'Last', '1:00', 4))


if __name__ == '__main__':
    unittest.main()
