from typing import Dict, Any, List
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

from configLoader import load_config, validate_config
from dataLoader import DataLoader
from dataProcessor import DataProcessor
import draw_bar_chart
import draw_pie_chart


# -----------------------------
# Helpers
# -----------------------------

def _year_columns(df: pd.DataFrame) -> List[str]:
    """Return sorted year columns as strings (e.g., '1960', '1961', ...)"""
    return sorted(
        [str(c) for c in df.columns if str(c).isdigit() and len(str(c)) == 4]
    )


def ensure_year_in_df(df: pd.DataFrame, year: int) -> None:
    year = str(year)
    if year not in map(str, df.columns):
        raise KeyError(f"Year {year} not present in dataset columns")


# -----------------------------
# Line charts
# -----------------------------

def plot_country_timeseries(
    df: pd.DataFrame,
    country: str,
    show: bool = True,
    out_path: str | None = None,
) -> None:

    years = _year_columns(df)
    row = df[df["Country Name"] == country]

    if row.empty:
        raise ValueError(f"Country '{country}' not found in data")

    values = row[years].astype(float).iloc[0].tolist()

    plt.figure(figsize=(10, 5))
    plt.plot([int(y) for y in years], values, marker="o")
    plt.title(f"GDP over time — {country}")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_region_time_series(
    df: pd.DataFrame,
    region: str,
    show: bool = True,
    out_path: str | None = None,
) -> None:
    years = _year_columns(df)
    grouped = df[df["Continent"] == region][years].sum()

    if grouped.empty:
        raise ValueError(f"Region '{region}' not found or has no data")

    values = grouped.astype(float).tolist()

    plt.figure(figsize=(10, 5))
    plt.plot([int(y) for y in years], values, marker="o")
    plt.title(f"Regional GDP over time — {region}")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


# -----------------------------
# Dashboard runner
# -----------------------------

def run_from_config(
    cfg: Dict[str, Any],
    show: bool = True,
    save_dir: str | None = None,
) -> Dict[str, Any]:

    # Validate config
    if not validate_config(cfg):
        raise SystemExit("Invalid configuration")

    # Load data
    loader = DataLoader()
    df = loader.load_csv(cfg.get("data_file", "gdp_cleaned_fixed.csv"))
    if df.empty:
        raise SystemExit("Data file not found or empty")

    df = loader.clean_numeric_columns(df)

    year = cfg["year"]
    ensure_year_in_df(df, year)

    # Process stats
    proc = DataProcessor()
    stats = proc.process_data(df, cfg)

    # Summary
    print("\n=== Dashboard summary ===")
    print(
        f"Config: region={cfg.get('region')}, "
        f"country={cfg.get('country')}, "
        f"year={year}, operation={cfg.get('operation')}"
    )
    print(f"Result ({stats['operation']}): ${stats['result']:,.2f}")

    charts = cfg.get("charts", {})
    saved_files: list[str] = []

    # -----------------------------
    # Region-level chart
    # -----------------------------
    rc = charts.get("region_chart")
    if rc and cfg.get("region"):
        try:
            region = cfg["region"]

            if rc.lower() == "bar":
                draw_bar_chart.regional_gdp_bar(df, region, year)
            elif rc.lower() == "pie":
                draw_pie_chart.regional_gdp_pie(df, region, year)
            elif rc.lower() == "line":
                plot_region_time_series(
                    df,
                    region,
                    show=show,
                    out_path=(
                        os.path.join(save_dir, f"region_line_{region}_{year}.png")
                        if save_dir
                        else None
                    ),
                )
                rc = None  # already handled
            else:
                print(f"Unknown region_chart type: {rc}")
                rc = None

            if rc:
                if save_dir:
                    out = os.path.join(save_dir, f"region_{rc}_{region}_{year}.png")
                    plt.savefig(out, bbox_inches="tight")
                    saved_files.append(out)

                if show:
                    plt.show()
                else:
                    plt.close()

        except Exception as e:
            print(f"Could not draw region chart: {e}")

    # -----------------------------
    # Year-level chart
    # -----------------------------
    yc = charts.get("year_chart")
    if yc:
        try:
            if yc.lower() == "bar":
                draw_bar_chart.yearly_gdp_bar(df, year)
            elif yc.lower() == "pie":
                draw_pie_chart.yearly_gdp_pie(df, year)
            elif yc.lower() == "line":
                if cfg.get("country"):
                    plot_country_timeseries(
                        df,
                        cfg["country"],
                        show=show,
                        out_path=(
                            os.path.join(save_dir, f"country_line_{cfg['country']}_{year}.png")
                            if save_dir
                            else None
                        ),
                    )
                    yc = None
                elif cfg.get("region"):
                    plot_region_time_series(
                        df,
                        cfg["region"],
                        show=show,
                        out_path=(
                            os.path.join(save_dir, f"region_line_{cfg['region']}_{year}.png")
                            if save_dir
                            else None
                        ),
                    )
                    yc = None
                else:
                    print("Line chart requires country or region")
                    yc = None
            else:
                print(f"Unknown year_chart type: {yc}")
                yc = None

            if yc:
                if save_dir:
                    out = os.path.join(save_dir, f"year_{yc}_{year}.png")
                    plt.savefig(out, bbox_inches="tight")
                    saved_files.append(out)

                if show:
                    plt.show()
                else:
                    plt.close()

        except Exception as e:
            print(f"Could not draw year chart: {e}")

    if save_dir:
        print(f"Saved chart files: {saved_files}")

    return stats


# -----------------------------
# Entrypoint
# -----------------------------

def main():
    cfg = load_config("config.json")
    if not cfg:
        print("Cannot load config.json — aborting")
        sys.exit(1)

    save_dir = cfg.get("output_dir")

    try:
        run_from_config(cfg, show=True, save_dir=save_dir)
    except Exception as exc:
        print(f"Error running dashboard: {exc}")
        print(
            "If you're running headless, set 'output_dir' in config.json "
            "to save charts instead of showing them."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()