from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.live import Live
import os


def generate_ui(file_path, output_path, include_resolution, create_link, generate_description, sys_msg, total_files,
                current_file):
    filename_panel = Panel(f"Filename: {os.path.basename(file_path)}", expand=False, width=80)
    output_panel = Panel(f"Output: {output_path}", expand=False, width=80)

    settings = [
        f"Link [{'X' if create_link else ' '}]",
        f"Date Created [X]",
        f"Resolution [{'X' if include_resolution else ' '}]",
        f"AI Description [{'X' if generate_description else ' '}]",
        f"Model: gpt-4-vision-preview"
    ]
    settings_panel = Panel("\n".join(settings), title="Settings / Options", expand=False, width=80)

    sys_msg_panel = Panel(sys_msg, title="Sys Msg", expand=False, width=80)

    progress_panel = Panel(f"File {current_file} of {total_files}", title="Progress", expand=False, width=80)

    layout = Columns([filename_panel, output_panel, settings_panel, sys_msg_panel, progress_panel], equal=True,
                     expand=False)

    return layout


if __name__ == "__main__":
    data_obj = [
        {
            "file_path": "/usr/test/files/image.jpg",
            "output_path": "/usr/test/output/image_2023-06-10_1920-1080.jpg",
            "include_resolution": True,
            "create_link": False,
            "generate_description": True,
            "sys_msg": "*** mov ***: image.jpg -> image_2023-06-10_1920-1080.jpg",
            "total_files": 10,
            "current_file": 3
        }
    ]
    console = Console()
    with Live(console=console, refresh_per_second=10) as live:
        live.update(generate_ui(**data_obj[0]))
