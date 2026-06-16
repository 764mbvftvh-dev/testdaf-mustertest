import json
import tempfile
import unittest
from pathlib import Path

from shared.question_bank import QuestionBankReader


class QuestionBankReaderTest(unittest.TestCase):
    def test_lists_and_loads_question_bundle_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            question_dir = root / "reading" / "aufgabe_1" / "q_reader"
            question_dir.mkdir(parents=True)
            (question_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "id": "q_reader",
                        "section": "reading",
                        "task_type": "aufgabe_1",
                        "title": "Reader Test",
                        "topic": "Topic",
                        "assets": {"questions": "questions.json", "preview": "preview.md"},
                    }
                ),
                encoding="utf-8",
            )
            (question_dir / "questions.json").write_text(json.dumps([{"number": 1}]), encoding="utf-8")
            (question_dir / "preview.md").write_text("# Preview", encoding="utf-8")

            reader = QuestionBankReader(root)
            questions = reader.list_questions()
            bundle = reader.load_question_bundle(questions[0]["_path"])

            self.assertEqual(questions[0]["id"], "q_reader")
            self.assertEqual(reader.find_by_id("q_reader")["_path"], "reading/aufgabe_1/q_reader")
            self.assertEqual(bundle["questions"], [{"number": 1}])
            self.assertEqual(bundle["preview"], "# Preview")

    def test_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            reader = QuestionBankReader(Path(temp_dir))
            with self.assertRaisesRegex(RuntimeError, "题目路径非法"):
                reader.load_question_bundle("../outside")


if __name__ == "__main__":
    unittest.main()
