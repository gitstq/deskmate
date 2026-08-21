#!/usr/bin/env python3
"""
DeskMate CLI 入口 / DeskMate CLI entry point
支持命令行参数启动 / Supports command-line arguments
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    parser = argparse.ArgumentParser(
        prog="deskmate",
        description="DeskMate - 跨平台桌面虚拟伴侣 / Cross-Platform Desktop Virtual Companion"
    )
    parser.add_argument(
        "--pet", "-p",
        choices=["cat", "dog", "bunny", "fox"],
        help="指定宠物种类 / Specify pet species"
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        help="宠物名字 / Pet name"
    )
    parser.add_argument(
        "--scale", "-s",
        type=float,
        default=1.0,
        help="显示缩放比例 / Display scale (default: 1.0)"
    )
    parser.add_argument(
        "--no-pomodoro",
        action="store_true",
        help="禁用番茄钟 / Disable pomodoro timer"
    )
    parser.add_argument(
        "--no-monitor",
        action="store_true",
        help="禁用系统监控 / Disable system monitor"
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="显示版本号 / Show version"
    )
    parser.add_argument(
        "--list-pets",
        action="store_true",
        help="列出可用宠物 / List available pets"
    )

    args = parser.parse_args()

    if args.version:
        from deskmate import __version__
        print(f"DeskMate v{__version__}")
        return

    if args.list_pets:
        from deskmate.pets import PET_DISPLAY_NAMES
        print("可用宠物 / Available pets:")
        for species, display in PET_DISPLAY_NAMES.items():
            print(f"  {species:8s} - {display}")
        return

    # 应用命令行配置到配置文件 / Apply CLI config to config file
    from deskmate.utils.config import ConfigManager
    config_mgr = ConfigManager()

    updates = {}
    if args.pet:
        updates["pet_species"] = args.pet
    if args.name:
        updates["pet_name"] = args.name
    if args.scale:
        updates["scale"] = args.scale
    if args.no_pomodoro:
        updates["enable_pomodoro"] = False
    if args.no_monitor:
        updates["enable_system_monitor"] = False

    if updates:
        config_mgr.update(**updates)

    # 启动GUI / Launch GUI
    from deskmate.main import main as gui_main
    gui_main()


if __name__ == "__main__":
    main()
