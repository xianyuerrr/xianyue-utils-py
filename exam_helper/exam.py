import json
from typing import *

from .question import Question


class Exam:
    def __init__(
            self,
            id: int | str,
            name: str,
            score: int,
            pass_score: int,
            questions: List[Question] = (),
    ):
        self.id = id
        self.name = name
        self.score = score
        self.pass_score = pass_score
        self.question_dict: Dict[int | str, Question] = {}
        self.add_list(questions)

    def add(self, question: Question) -> None:
        if question.id in self.question_dict.keys():
            return
        self.question_dict[question.id] = question
        return

    def add_list(self, questions: List[Question]) -> None:
        for question in questions:
            if question.id in self.question_dict.keys():
                continue
            self.question_dict[question.id] = question
        return

    def __str__(self):
        lis = [
            f"{self.name}",
            f"得分: {self.pass_score}, 通过: {self.pass_score}, 满分: {self.score}",
        ]
        lis += map(
            lambda x: f"{x[0]}. {str(x[1])}", enumerate(self.question_dict.values(), 1)
        )
        return "\n\n".join(lis)


def load_from_response(result_path) -> Exam:
    with open(result_path, "r", encoding="utf-8") as f:
        resp = json.load(f)
    out_put = []

    data = resp["data"]
    exam_name = data["examName"]
    exam_id = data["examId"]
    paperScore = data["paperScore"]
    pass_score = data["passScore"]

    exam = Exam(exam_id, exam_name, paperScore, pass_score)

    items = data["subjectList"]
    for nu, item in enumerate(items):
        title = item["subjectTitle"]
        # 1: 判断, 2: 单选, 3: 多选
        subjectType = item["subjectType"]
        # 1. 判断: 0, 1
        # 2. 选择: optionId (多个时以&分隔)
        answer: str = item["answer"]
        id = item["subjectId"]
        subject_score = item["subjectScore"]
        answer_right = item["answerRight"] == 1
        subject_option_list = item["subjectOptionVOList"]

        question = Question(
            id, subjectType, title, subject_score, answer.split("&"), answer_right
        )
        question.add_list(
            list(
                map(
                    lambda x: Question.Option(x["optionId"], x["optionTitle"]),
                    subject_option_list,
                )
            )
        )
        exam.add(question)
    return exam
