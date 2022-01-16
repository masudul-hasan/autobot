from typing import Tuple

from rich import box
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.table import Table
from rich.text import Text

from prettify.prettify_ldma import Header


class ClosePrettify:
    _layout = Layout()
    _table = Table(title="CLOSE STATUS", expand=True, box=box.ROUNDED)

    @classmethod
    def make_layout(cls) -> None:
        cls._layout.split(
            Layout(name="header", size=3),
            Layout(name="body")
        )

        cls._layout["body"].split_row(
            Layout(name="left"),
            Layout(name="tables")
        )
        cls._layout["left"].split_column(
            Layout(name="top"),
            Layout(name="progress")
        )
        cls._layout["header"].update(Header("Close NCR Activity"))
        # cls._layout["top"].update(cls.get_top_layout())

    @classmethod
    def make_table(cls) -> None:
        cls._table.add_column("SL", justify="right", no_wrap=True)
        cls._table.add_column("NCR No", justify="center", no_wrap=True, header_style="green")
        cls._table.add_column("Status", justify="center", no_wrap=True)

    @classmethod
    def add_row_table(cls, sl_id: str, ncr_number: str, status: str) -> None:
        cls._table.add_row(sl_id, ncr_number, status)

    @classmethod
    def get_layout(cls) -> Layout:
        return cls._layout

    @classmethod
    def get_table(cls) -> Table:
        return cls._table

    @classmethod
    def merge_layout(cls, progress, table) -> None:
        cls._layout["progress"].update(Panel(
            Align.center(progress, vertical="middle"), border_style="green", title="Overall Status"))
        cls._layout["tables"].update(Panel(
            Align.center(table, vertical="middle"), border_style="cyan", title="Details"))

    @classmethod
    def progress_bar(cls, tasks_range: int) -> Progress:
        job_progress = Progress(
            "{task.description}",
            SpinnerColumn("dots", finished_text="Done", style="cyan"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        job_progress.add_task("[Closing]:", total=tasks_range)

        progress_table = Table.grid()
        progress_table.add_row(
            Panel.fit(job_progress, title="[b]jobs", padding=(2, 2))
        )
        return job_progress

    def __str__(self):
        return self._layout
