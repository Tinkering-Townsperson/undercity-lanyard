# Undercity eink lanyard WITH GUI

[![Hackatime Badge](https://hackatime-badge.hackclub.com/U081MDA4T24/undercity-lanyard?style=for-the-badge)](https://hackatime.hackclub.com)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json&style=for-the-badge)](https://python-poetry.org/)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FTinkering-Townsperson%2Fundercity-lanyard%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge)
[![GitHub Tag](https://img.shields.io/github/v/tag/Tinkering-Townsperson/undercity-lanyard?style=for-the-badge)](https://github.com/Tinkering-Townsperson/undercity-lanyard)

![Icon](./assets/icon.png)

Ok before we go ahead, I just want to credit [@vracton](https://github.com/vracton/undercity-lanyard), [@JeffreyWangDev](https://github.com/JeffreyWangDev/undercity-lanyard), [@phthallo](https://github.com/phthallo/undercity-lanyard), and especially [@espcaa](https://github.com/espcaa/undercity-lanyard) for creating most of the codebase. I only restructured some things and gave it a somewhat-janky-but-usable GUI.

## Setup

1. Install a venv

```sh
python -m venv .venv
```

2. Activate the venv

Windows:

```cmd
.\.venv\Scripts\activate
```

Mac/Linux:

```sh
chmod +x ./.venv/bin/activate
source ./.venv/bin/activate
```

3. Run

```sh
pip install .[gui]
```

## Usage (Console mode)

1. In the venv, run

```sh
undercity_lanyard_console
```

2. Follow the instructions and answer the prompts
3. **DONE!** ::

## Usage (GUI mode)

1. In the venv, run

```sh
undercity_lanyard_gui
```

![GUI with empty inputs](./assets/gui-1.png)

2. Enter information in the entry boxes

![GUI with filled-out inputs](./assets/gui-2.png)

3. Click `Create!` and watch the preview update

![GUI with preview](./assets/gui-3.png)

4. Click `Flash!` and follow the message boxes.

![GUI with prompt](./assets/gui-4.png)
![GUI with success](./assets/gui-5.png)

5. IT WORKS YAY :exploding_head:

![Lanyard but working!!!](./assets/lanyard%20working.jpg)
