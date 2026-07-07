from .tool_definition import Tool


TOOLS = [

    Tool(
        id="raise",
        title="Raise",
        category="Terrain",
        command="set_mode",
        mode="raise",
        tooltip="Terrain anheben",
        args=("raise",)
    ),

    Tool(
        id="lower",
        title="Lower",
        category="Terrain",
        command="set_mode",
        mode="lower",
        tooltip="Terrain absenken",
        args=("lower",)
    ),

    Tool(
        id="smooth",
        title="Smooth",
        category="Terrain",
        command="set_mode",
        mode="smooth",
        tooltip="Terrain glätten",
        args=("smooth",)
    ),

    Tool(
        id="flatten",
        title="Flatten",
        category="Terrain",
        command="set_mode",
        mode="flatten",
        tooltip="Fläche ebnen",
        args=("flatten",)
    ),

    Tool(
        id="grass",
        title="Grass",
        category="Textures",
        command="set_texture_layer",
        tooltip="Gras",
        args=(0,)
    ),

    Tool(
        id="rock",
        title="Rock",
        category="Textures",
        command="set_texture_layer",
        tooltip="Fels",
        args=(1,)
    ),

    Tool(
        id="sand",
        title="Sand",
        category="Textures",
        command="set_texture_layer",
        tooltip="Sand",
        args=(2,)
    ),

    Tool(
        id="snow",
        title="Snow",
        category="Textures",
        command="set_texture_layer",
        tooltip="Schnee",
        args=(3,)
    ),
]