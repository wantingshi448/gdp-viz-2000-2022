import pandas as pd
import matplotlib.pyplot as plt
from typing import Iterable, Optional

def plot_countries(
    df_tidy: pd.DataFrame,
    countries: Optional[Iterable[str]] = None,
    title: str = "GDP (constant 2015 US$)",
    save_path: Optional[str] = None,
    show: bool = False,
    unit: str = "raw",  # "raw" | "billion" | "trillion"
    logy: bool = False,
    normalize_base_year: Optional[int] = None,  # e.g., 2000 -> index to 100
) -> None:
    """
    Plot GDP lines from tidy df(country, year, value).
    - unit: scale y values for readability
    - logy: use log scale on y-axis
    - normalize_base_year: divide each country's series by its value at that year and *100
    """
    data = df_tidy if countries is None else df_tidy[df_tidy["country"].isin(countries)].copy()

    # 单位换算
    scale = 1.0
    y_label = "GDP (constant 2015 US$)"
    if unit == "billion":
        scale = 1e-9
        y_label = "GDP (billion, 2015 US$)"
    elif unit == "trillion":
        scale = 1e-12
        y_label = "GDP (trillion, 2015 US$)"

    # 归一化（相对指数）
    if normalize_base_year is not None:
        normed = []
        for c in sorted(data["country"].unique()):
            sub = data[data["country"] == c].sort_values("year").copy()
            base = sub.loc[sub["year"] == normalize_base_year, "value"]
            if not base.empty and base.iloc[0] > 0:
                sub["value"] = sub["value"] / base.iloc[0] * 100.0
                normed.append(sub)
        if normed:
            data = pd.concat(normed, ignore_index=True)
            y_label = f"GDP index (base={normalize_base_year} = 100)"

    fig, ax = plt.subplots()
    for c in sorted(data["country"].unique()):
        sub = data[data["country"] == c].sort_values("year")
        ax.plot(sub["year"], sub["value"] * scale, label=c)

    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel(y_label)
    if logy:
        ax.set_yscale("log")
    ax.legend()
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
