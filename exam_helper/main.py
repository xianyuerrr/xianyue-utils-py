from exam_helper.utils import *
import argparse


def main():
    parser = argparse.ArgumentParser(description='处理测验结果的工具')
    parser.add_argument('path', type=str, help='测验结果文件或目录的路径')
    args = parser.parse_args()

    parse_exam_result(args.path)


if __name__ == '__main__':
    main()
