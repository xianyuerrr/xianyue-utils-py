import json
import os
from os.path import join as pjoin
from collections import defaultdict

from .exam import Exam
from .exam import load_from_response
from .repo import QuestionRepo
from serial_helper.utils import serialize_obj


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
    elif os.path.isfile(exam_result_dir):
        exam = load_from_response(exam_result_dir)
        exam_dict[exam.id].append(exam)

    exam_repo_path = pjoin(exam_result_dir, "repo")
    for exam_id, exams in exam_dict.items():
        repo = QuestionRepo()
        repo_path = pjoin(exam_repo_path, exam_id)
        repo.load(repo_path)
        for exam in exams:
            repo.update(exam)
        os.makedirs(os.path.dirname(repo_path + ".json"), exist_ok=True)
        with open(repo_path + ".json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(serialize_obj(repo), indent=4, ensure_ascii=False))
        os.makedirs(os.path.dirname(repo_path + ".txt"), exist_ok=True)
        with open(repo_path + ".txt", 'w', encoding='utf-8') as f:
            f.write(str(repo))
