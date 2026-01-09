from dataclasses import dataclass

INFO_LIMIT = 20

@dataclass
class Command:
    name: str
    args: tuple


class ProtocolError(Exception):
    pass


def parse_command(raw: str) -> Command:
    raw = raw.strip()
    if not raw:
        raise ProtocolError("Empty command")

    parts = raw.split()
    name = parts[0].upper()

    try:
        if name == "MOVE":
            if len(parts) != 3:
                raise ProtocolError("MOVE requires 2 args")
            v = float(parts[1])
            omega = float(parts[2])
            return Command("MOVE", (v, omega))

        elif name == "STOP":
            return Command("STOP", ())

        elif name == "PING":
            return Command("PING", ())

        elif name == "INFO":
            if len(parts) > INFO_LIMIT:
                raise ProtocolError(f"INFO requires less than {INFO_LIMIT} args")
            return Command("INFO", parts[1:])

        else:
            raise ProtocolError(f"Unknown command: {name}")

    except ValueError:
        raise ProtocolError("Invalid numeric value")


def format_command(cmd: Command) -> bytes:
    if not isinstance(cmd, Command):
        raise ProtocolError("Expected a Command object")

    if cmd.name == "MOVE":
        cmd_str = f"{cmd.name} {cmd.args[0]} {cmd.args[1]}"
    elif cmd.name == "INFO":
        if not all(isinstance(a, str) for a in cmd.args):
            raise ProtocolError("INFO args must be strings")
        cmd_str = f"{cmd.name} {' '.join(cmd.args)}"
    else:
        cmd_str = f"{cmd.name}"

    return (cmd_str + "\n").encode("utf-8")
