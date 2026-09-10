"""Plot a temperature field exported as CSV.

Expected columns are x, y, and temperature. Common aliases are accepted:
    x / X, y / Y, temperature / Temperature / T

Example:
    python plot_temperature.py temperature.csv --output temperature.png
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def find_column(fieldnames: list[str], aliases: tuple[str, ...]) -> str | None:
    columns = {field.strip().lower(): field for field in fieldnames}
    for alias in aliases:
        if alias.lower() in columns:
            return columns[alias.lower()]
    return None


def read_temperature_csv(path: Path) -> tuple[list[float], list[float], list[float]]:
    with path.open("r", newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        if not reader.fieldnames:
            raise ValueError("CSV file must contain a header row")

        x_column = find_column(reader.fieldnames, ("x", "x_coordinate"))
        y_column = find_column(reader.fieldnames, ("y", "y_coordinate", "z"))
        temperature_column = find_column(
            reader.fieldnames,
            ("temperature", "Temperature", "T", "temp"),
        )

        missing = []
        if x_column is None:
            missing.append("x")
        if y_column is None:
            missing.append("y or z")
        if temperature_column is None:
            missing.append("temperature or T")
        if missing:
            available = ", ".join(reader.fieldnames)
            raise ValueError(
                f"Missing column(s): {', '.join(missing)}. Available columns: {available}"
            )

        x_values: list[float] = []
        y_values: list[float] = []
        temperature_values: list[float] = []
        for line_number, row in enumerate(reader, start=2):
            try:
                x_values.append(float(row[x_column]))
                y_values.append(float(row[y_column]))
                temperature_values.append(float(row[temperature_column]))
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid numeric value on CSV line {line_number}") from error

    if not temperature_values:
        raise ValueError("CSV file contains no data rows")
    return x_values, y_values, temperature_values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plot a temperature field from a CSV file.")
    parser.add_argument("input", type=Path, help="CSV file containing x, y, and temperature columns")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="PNG output path (default: <input>_temperature.png)",
    )
    parser.add_argument("--title", default="Temperature field", help="Plot title")
    parser.add_argument("--levels", type=int, default=20, help="Number of contour levels")
    parser.add_argument("--cmap", default="inferno", help="Matplotlib colormap")
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    output_path = arguments.output or arguments.input.with_name(
        f"{arguments.input.stem}_temperature.png"
    )

    try:
        x_values, y_values, temperature_values = read_temperature_csv(arguments.input)
        import matplotlib.pyplot as pyplot
        import numpy as np
    except FileNotFoundError:
        print(f"Input file not found: {arguments.input}", file=sys.stderr)
        return 1
    except ImportError:
        print("Matplotlib and NumPy are required: python -m pip install matplotlib numpy", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Invalid temperature data: {error}", file=sys.stderr)
        return 1

    figure, axis = pyplot.subplots(figsize=(9, 6), constrained_layout=True)
    contour = axis.tricontourf(
        np.asarray(x_values),
        np.asarray(y_values),
        np.asarray(temperature_values),
        levels=max(2, arguments.levels),
        cmap=arguments.cmap,
    )
    scatter = axis.scatter(
        x_values,
        y_values,
        c=temperature_values,
        cmap=arguments.cmap,
        s=8,
        edgecolors="none",
    )
    colorbar = figure.colorbar(contour, ax=axis)
    colorbar.set_label("Temperature")
    axis.set_title(arguments.title)
    axis.set_xlabel("x")
    axis.set_ylabel("y / z")
    axis.set_aspect("equal", adjustable="box")
    axis.grid(alpha=0.2)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200)
    pyplot.close(figure)
    print(f"Temperature plot saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
