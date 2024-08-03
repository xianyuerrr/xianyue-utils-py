import json
import os
from collections import defaultdict
from os.path import join as pjoin

from .exam import Exam
from .exam import load_from_response
from .repo import QuestionRepo


def serialize_obj(obj):
    """
    序列化对象函数，将对象转换为字典或列表的形式

    参数:
        obj: 需要序列化的对象

    返回:
        序列化后的对象
    """
    if isinstance(obj, dict):
        return {k: serialize_obj(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {
            k: serialize_obj(v)
            for k, v in obj.__dict__.items()
            if not callable(v) and not k.startswith("_")
        }
    elif isinstance(obj, list):
        return [serialize_obj(elem for elem in obj)]
    elif isinstance(obj, types.GeneratorType):
        return list(obj).sort()
    elif isinstance(obj, set):
        return list(obj).sort()
    else:
        return obj


def parse_exam_result(exam_result_dir: str) -> None:
    if not os.path.exists(exam_result_dir):
        print("exam_result_path doesn't exist: {}".format(exam_result_dir))
        return
    exam_dict: defaultdict[str, list[Exam]] = defaultdict(list)
    if os.path.isdir(exam_result_dir):
        for filename in os.listdir(exam_result_dir):
            parsed_path = pjoin(exam_result_dir, "parsed/")
            if filename.endswith('.json'):
                exam = load_from_response(pjoin(exam_result_dir, filename))
                exam_dict[exam.id].append(exam)

                parsed_file_name = pjoin(parsed_path, filename.rstrip(".json") + ".txt")
                os.makedirs(os.path.dirname(parsed_file_name), exist_ok=True)
                with open(parsed_path + filename.rstrip(".json") + ".txt", 'w', encoding='utf-8') as f:
                    f.write(str(exam))
    else:
        print("exam_result_path doesn't is a dir: {}".format(exam_result_dir))
        return

    exam_repo_path = pjoin(os.path.dirname(exam_result_dir), "repo")
    for exam_id, exams in exam_dict.items():
        repo = QuestionRepo()
        repo_file_path = pjoin(exam_repo_path, exam_id + ".json")
        # repo.load()
        for exam in exams:
            repo.update(exam)
        os.makedirs(os.path.dirname(repo_file_path), exist_ok=True)
        with open(repo_file_path + ".json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(serialize_obj(repo), indent=4, ensure_ascii=False))
        repo_view_file_path = pjoin(exam_repo_path, exam_id + ".txt")
        os.makedirs(os.path.dirname(repo_view_file_path), exist_ok=True)
        with open(repo_view_file_path, 'w', encoding='utf-8') as f:
            f.write(str(repo))
