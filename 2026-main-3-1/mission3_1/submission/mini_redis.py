#!/usr/bin/env python3
"""Executable entry point for the Mini Redis CLI."""

from mini_redis.cli import MiniRedisCLI


def main():
    MiniRedisCLI().run()


if __name__ == "__main__":
    main()
