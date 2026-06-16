import unittest

from student_platform.web import app


class StudentPlatformRoutesTest(unittest.TestCase):
    def test_student_routes_are_registered(self) -> None:
        paths = [getattr(route, "path", "") for route in app.routes]

        self.assertIn("/", paths)
        self.assertIn("/practice/{section}/{task_type}/{question_id}", paths)
        self.assertIn("/attempts", paths)
        self.assertIn("/health", paths)


if __name__ == "__main__":
    unittest.main()
