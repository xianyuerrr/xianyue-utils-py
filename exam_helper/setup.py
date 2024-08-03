from setuptools import setup, find_packages
from .__init__ import __version__

setup(
    name='exam_helper',
    version=__version__,
    author='xianyue',
    description='测验结果处理工具，可以将结果转换为可读的格式，并将正确答案保存到本地',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'exam_helper = exam_helper.utils:parse_exam_result',
        ],
    },
)
