from dataclasses import dataclass, field


@dataclass
class Tool:

    title: str
    command: str
    mode: str = ""
    args: tuple = ()
    tooltip: str = ""


@dataclass
class Category:

    title: str
    icon: str = ""
    collapsed: bool = False
    tools: list = field(default_factory=list)


UI_REGISTRY = [

    Category(
        title="Terrain",
        tools=[
            Tool("Raise", "set_mode", "raise", ("raise",), "Raise terrain"),
            Tool("Lower", "set_mode", "lower", ("lower",), "Lower terrain"),
            Tool("Smooth", "set_mode", "smooth", ("smooth",), "Smooth terrain"),
            Tool("Flatten", "set_mode", "flatten", ("flatten",), "Flatten terrain"),
        ],
    ),

    Category(
        title="Textures",
        tools=[
            Tool("Grass", "set_texture_layer", "grass", (0,), "Grass texture"),
            Tool("Rock", "set_texture_layer", "rock", (1,), "Rock texture"),
            Tool("Sand", "set_texture_layer", "sand", (2,), "Sand texture"),
            Tool("Snow", "set_texture_layer", "snow", (3,), "Snow texture"),
        ],
    ),

    Category(
        title="Objects",
        collapsed=True,
        tools=[],
    ),

    Category(
        title="Roads",
        collapsed=True,
        tools=[],
    ),

    Category(
        title="Water",
        collapsed=True,
        tools=[],
    ),

    Category(
        title="Vegetation",
        collapsed=True,
        tools=[],
    ),

    Category(
        title="SpringRTS",
        collapsed=True,
        tools=[],
    ),

    Category(
        title="AI",
        collapsed=True,
        tools=[],
    ),
]