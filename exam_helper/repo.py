from .exam import Exam
from .question import Question


class QuestionRepo:
    def __init__(self):
        self.question_dict: dict[int | str, Question] = {}
        return

    def load(self, path) -> None:
        return

    def update(self, exam: Exam) -> None:
        dic = exam.question_dict
        dic = {k: dic[k] for k in filter(lambda x: x not in self.question_dict and dic[x].is_right, dic.keys())}
        self.question_dict.update(dic)

    def query(self, id: int | str) -> Question:
        return self.question_dict[id]

    def __str__(self):
        return "\n\n".join(map(lambda x: f"{x[0]}. {str(x[1])}", enumerate(self.question_dict.values(), 1)))
