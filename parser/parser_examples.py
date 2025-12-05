"""
Argparse 使用示例（简洁、可直接运行）

说明：
- 演示常见参数类型（布尔开关、整型、字符串、选择项、列表）
- 演示 `parse_known_args` 如何把未知参数（例如 Hydra 风格参数）分离出来
- 演示如何把外部模块把参数添加进来（用本文件的模拟函数替代真实模块）
- 演示如何以编程方式传入 `argv`（便于测试）

运行：
    python3 parser_examples.py

也可以通过传参模拟命令行，例如：
    python3 parser_examples.py --video --video_length 300 --task push

"""

import argparse
from argparse import ArgumentDefaultsHelpFormatter
from typing import List, Tuple
import pprint


def add_rsl_rl_args(parser: argparse.ArgumentParser) -> None:
    """模拟外部模块 `cli_args.add_rsl_rl_args(parser)` 的行为。
    在真实项目中，这个函数会往 parser 添加一组与 RSL-RL 相关的选项。
    这里只是演示："num_workers" 和 "policy" 两个参数。
    """
    group = parser.add_argument_group("rsl_rl options")
    group.add_argument("--num_workers", type=int, default=1, help="Number of worker processes.")
    group.add_argument("--policy", type=str, default="default_policy", help="Policy name to use.")


def add_app_launcher_args(parser: argparse.ArgumentParser) -> None:
    """模拟 `AppLauncher.add_app_launcher_args(parser)`。演示添加分布式/launcher 相关参数。"""
    group = parser.add_argument_group("app launcher")
    group.add_argument("--distributed", action="store_true", default=False, help="Run in distributed mode.")
    group.add_argument("--gpus", type=int, default=1, help="Number of GPUs to use.")


# ---------- 构建主 parser ----------

def build_main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train an RL agent with RSL-RL (argparse examples)",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    # 基本参数（与用户提供的代码一致）
    parser.add_argument("--video", action="store_true", default=False, help="Record videos during training.")
    parser.add_argument("--video_length", type=int, default=200, help="Length of the recorded video (in steps).")
    parser.add_argument("--video_interval", type=int, default=2000, help="Interval between video recordings (in steps).")
    parser.add_argument("--num_envs", type=int, default=None, help="Number of environments to simulate.")
    parser.add_argument("--task", type=str, default=None, choices=[None, "push", "pick", "place"], help="Name of the task.")
    parser.add_argument(
        "--agent",
        type=str,
        default="rsl_rl_cfg_entry_point",
        help="Name of the RL agent configuration entry point.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment")
    parser.add_argument("--max_iterations", type=int, default=None, help="RL Policy training iterations.")

    # 演示如何让外部模块添加参数（模拟）
    add_rsl_rl_args(parser)
    add_app_launcher_args(parser)

    return parser


# ---------- 演示函数 ----------

def demo_parse(argv: List[str] = None) -> Tuple[argparse.Namespace, List[str]]:
    """解析传入的 argv（若为 None 则解析真实命令行）。
    返回 (known_args_namespace, unknown_args_list)
    """
    parser = build_main_parser()

    # parse_known_args 将已知参数解析到 args_cli，剩下的放到 hydra_args（或 unknown）
    if argv is None:
        args_cli, unknown = parser.parse_known_args()
    else:
        args_cli, unknown = parser.parse_known_args(argv)

    return args_cli, unknown


def pretty_print_parse(argv: List[str] = None) -> None:
    args, unknown = demo_parse(argv)
    print("Parsed known args:")
    pprint.pprint(vars(args))
    print("Unknown args (leftover):", unknown)
    print()


# ---------- 主运行，展示几个示例 ----------

if __name__ == "__main__":
    print("Example A: parse default (no extra argv)")
    pretty_print_parse([])  # empty list => use defaults

    print("Example B: simulate CLI input (video + task + custom extra args)")
    argv = [
        "--video",
        "--video_length",
        "300",
        "--task",
        "push",
        "--num_workers",
        "8",
        "--gpus",
        "2",
        # unknown / hydra-like args that will be left in 'unknown'
        "hydra.run.dir=/tmp/run1",
        "some.other.override=1",
    ]
    pretty_print_parse(argv)

    print("Example C: show how to access values in code")
    args, _ = demo_parse(["--video", "--video_interval", "1000", "--agent", "my_agent"])
    if args.video:
        print(f"  will record videos (length={args.video_length}, interval={args.video_interval})")
    print(f"  agent: {args.agent}")
    print()

    print("Done. See above examples for usage of argparse and parse_known_args.")
