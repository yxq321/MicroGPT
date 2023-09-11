from textwrap import dedent

import argparse


def copyright():
    print(
        dedent(
            """\
        Copyright (c) 1991-2000 ACME Corp
        All Rights Reserved.

             I love you.

        Copyright (c) 2000-2030 Cyberdyne
        All Rights Reserved."""
        ).strip("\n")
    )


def parse_agrs():
    arg = argparse.ArgumentParser(description="A test for argparse.")
    arg.add_argument(
        "--hide-source",
        "-S",
        action="store_true",
        help="Use this flag to disable printing of source documents used for answers.",
    )
    arg.add_argument(
        "--mute-stream",
        "-M",
        action="store_true",
        required=True,  # 必填参数
        help="Use this flag to disable the streaming StdOut callback for LLMs.",
    )
    arg.add_argument(
        "--host",
        "-H",
        default="127.0.0.1",  # 默认参数
        help="Host IP address.",
    )
    arg.add_argument(
        "--copyright",
        "-C",
        action="store_true",
        help="Show Copyright information.",
    )
    return arg.parse_args()


if __name__ == "__main__":
    arg = parse_agrs()
    print(arg.mute_stream)
    print(arg.host)
    if arg.copyright:
        copyright()
