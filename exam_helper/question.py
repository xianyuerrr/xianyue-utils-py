from typing import *


class Question:
    class Option:
        def __init__(self, id: int | str, title: str):
            self.id: int | str = id
            self.title: str = title
            self.is_selected: bool = False

        def select(self) -> None:
            self.is_selected = True

        def un_select(self) -> None:
            self.is_selected = False

        def __str__(self):
            return f"{'[ * ]' if self.is_selected else '[   ]'} {self.id}. {self.title}"

    def __init__(self, id: str, type: int | str, title: str, score: int, answer: Collection[int | str] = (),
                 is_right: bool = False,
                 options: List[Option] = ()):
        self.id = id
        self.title = title
        # 1: 判断, 2: 单选, 3: 多选
        self.type = type
        self.score = score
        self.is_right = is_right
        self.answer: Set = set(answer)
        self.option_dict: dict[int | str, Optional] = {}
        self.add_list(options)

        if type == 1 and not self.option_dict:
            option1 = Question.Option("1", "正确")
            option2 = Question.Option("0", "错误")
            self.add_list([option2, option1])

    def add(self, option: Option) -> None:
        if option.id in self.option_dict:
            return
        if option.id in self.answer:
            option.select()
        self.option_dict[option.id] = option
        return

    def add_list(self, options: List[Option]) -> None:
        for option in options:
            self.add(option)
        return

    def __str__(self) -> str:
        lis = [f"{self.title}", f"isRight:  {self.is_right}"]
        for option in self.option_dict.values():
            lis.append(str(option))
        return "\n".join(line.strip() for line in lis)
