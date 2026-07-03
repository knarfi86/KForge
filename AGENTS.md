# AGENTS

## Project overview

KForge is a Python-based terrain editor built with Panda3D. It is centered around `main.py` and the `editor/` package, and it exports SpringRTS-compatible map data into `spring_export/`.

## How to run

- Install dependencies: `pip install -r requirements.txt`
- Start the editor: `python main.py`

## Key files and directories

- `main.py`: application entrypoint creating `EditorApp`
- `requirements.txt`: runtime dependency `panda3d>=1.10`
- `editor/app.py`: core editor loop, input handling, brush actions, save/load/export
- `editor/config.py`: global constants for window, terrain, brush, textures, export paths
- `editor/terrain.py`: terrain model, heightmap, textures, metal map, typemap, mesh rebuild logic
- `editor/world.py`: placed objects, start positions, scene markers, serialization
- `editor/exporter.py`: writes `spring_export/` content and `kforge_project.json`
- `editor/ui.py`: Panda3D DirectGUI interface and status updates

## Development notes for AI agents

- Preserve the Panda3D scene graph and input event patterns in `editor/app.py` and `editor/ui.py`.
- Prefer using `config.py` constants instead of introducing hardcoded numeric values.
- Support the existing save/load flow using `kforge_terrain.json` and export flow using `spring_export/`.
- Do not assume there are automated tests; validate changes by running the editor manually.
- The codebase uses simple data serialization to JSON and Lua text generation for SpringRTS export. Maintain that export format.

## Useful hints

- The editor is primarily interactive; changes to brush, terrain, or export logic should keep the in-editor UI and state consistent.
- `EditorApp` inherits from `direct.showbase.ShowBase`, so modifications should respect Panda3D initialization and task management.
- `SpringExporter` generates both image files and Lua config files for SpringRTS maps.
