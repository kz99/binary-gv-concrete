from __future__ import annotations

import argparse
import json

from .campaign import Campaign, launch_campaign


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="binary-gv-research")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("init", "initialize durable campaign state"),
        ("run", "run or resume the campaign in the foreground"),
        ("launch", "launch the campaign in the background"),
        ("status", "show durable campaign progress"),
        ("genius-checkpoint", "run one requested GENIUS integration checkpoint"),
    ):
        item = sub.add_parser(name, help=help_text)
        item.add_argument("config")
    item = sub.add_parser("add-researchers", help="append ultra-reasoning researcher seats")
    item.add_argument("config")
    item.add_argument("count", type=int)
    item = sub.add_parser("add-team", help="append one named ten-agent research team")
    item.add_argument("config")
    item.add_argument("team")
    args = parser.parse_args(argv)
    if args.command == "launch":
        payload = launch_campaign(args.config)
    else:
        campaign = Campaign(args.config)
        if args.command == "init":
            payload = campaign.initialize()
        elif args.command == "run":
            payload = campaign.run()
        elif args.command == "add-researchers":
            payload = campaign.add_researchers(args.count)
        elif args.command == "add-team":
            payload = campaign.add_team(args.team)
        elif args.command == "genius-checkpoint":
            payload = campaign.run_genius_checkpoint()
        else:
            payload = campaign.status()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0
