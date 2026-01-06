from dataclasses import dataclass


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

        else:
            raise ProtocolError(f"Unknown command: {name}")

    except ValueError:
        raise ProtocolError("Invalid numeric value")
