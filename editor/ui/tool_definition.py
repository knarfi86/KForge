from dataclasses import dataclass, field


@dataclass(slots=True)
class Tool:

    id: str
    title: str
    category: str

    command: str

    mode: str | None = None

    icon: str = ""

    tooltip: str = ""

    shortcut: str = ""

    args: tuple = field(default_factory=tuple)

    enabled: bool = True