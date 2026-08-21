"""
DeskMate setup.py / 安装配置
"""

from setuptools import setup, find_packages
import os

# 读取README / Read README
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="deskmate",
    version="1.0.0",
    description="跨平台桌面虚拟伴侣 - Cross-Platform Desktop Virtual Companion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DeskMate Team",
    author_email="fy.suntianqi@gmail.com",
    url="https://github.com/suntianqi/deskmate",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    extras_require={
        "monitor": ["psutil>=5.9.0"],
        "build": ["pyinstaller>=5.0"],
    },
    entry_points={
        "console_scripts": [
            "deskmate=deskmate.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
    keywords="desktop pet virtual companion pomodoro system-monitor cross-platform",
)
