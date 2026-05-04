from shiny import App, ui, render, reactive
from shinywidgets import output_widget, register_widget
from ipyleaflet import Map, CircleMarker, basemaps
from ipywidgets import HTML
import pandas as pd

# --- Load data (runs once when the app starts) ---
penguins_geo = pd.read_csv("data/penguins_geo.csv")

species_colours = {
    "Adelie": "#ff6f00",
    "Gentoo": "#1565c0",
    "Chinstrap": "#2e7d32",
}

# --- UI ---
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox_group(
            "species", "Species",
            choices=["Adelie", "Gentoo", "Chinstrap"],
            selected=["Adelie", "Gentoo", "Chinstrap"],
        ),
        ui.input_checkbox_group(
            "islands", "Islands",
            choices=["Torgersen", "Biscoe", "Dream"],
            selected=["Torgersen", "Biscoe", "Dream"],
        ),
        width=280,
    ),
    ui.output_text("summary"),
    ui.layout_columns(
        ui.card(
            ui.card_header("Map"),
            output_widget("map"),
        ),
        ui.card(
            ui.card_header("Bill length distribution"),
            ui.output_plot("hist"),
        ),
        col_widths=[7, 5],
    ),
    title="Palmer Penguins Explorer",
)

# --- Server ---
def server(input, output, session):

    # Create the map ONCE and register it with the output.
    # We update layers in place using @reactive.effect instead of
    # recreating the whole map, because @render_widget does not
    # reliably re-render ipyleaflet maps when inputs toggle.
    m = Map(
        center=(-64.8, -64.5),
        zoom=9,
        basemap=basemaps.Esri.WorldImagery,
    )
    register_widget("map", m)

    @reactive.calc
    def filtered():
        df = penguins_geo[penguins_geo["species"].isin(input.species())]
        return df[df["island"].isin(input.islands())]

    @reactive.effect
    def _update_map():
        sel = filtered().dropna(subset=["latitude"])

        # Remove old markers (keep the basemap layer at index 0)
        m.layers = [m.layers[0]]

        for _, row in sel.iterrows():
            colour = species_colours[row["species"]]
            marker = CircleMarker(
                location=(row["latitude"], row["longitude"]),
                radius=4,
                color=colour,
                fill_color=colour,
                fill_opacity=0.7,
            )
            marker.popup = HTML(
                value=(
                    f"<b>{row['species']}</b><br>"
                    f"Island: {row['island']}<br>"
                    f"Bill: {row['bill_length_mm']} mm<br>"
                    f"Mass: {row['body_mass_g']} g"
                )
            )
            m.add(marker)

    @render.text
    def summary():
        sel = filtered()
        n = len(sel.dropna(subset=["bill_length_mm"]))
        avg_mass = sel["body_mass_g"].mean()
        species_list = ", ".join(sorted(sel["species"].unique()))
        islands = ", ".join(sorted(sel["island"].unique()))
        return (
            f"{species_list}: {n} penguins on {islands}, "
            f"avg body mass {avg_mass:,.0f} g"
        )

    @render.plot
    def hist():
        import matplotlib.pyplot as plt

        sel = filtered()
        selected_species = sorted(sel["species"].unique())

        fig, ax = plt.subplots(figsize=(7, 3))
        for sp in selected_species:
            sub = sel[sel["species"] == sp]
            ax.hist(
                sub["bill_length_mm"].dropna(),
                bins=15,
                color=species_colours[sp],
                edgecolor="white",
                alpha=0.7,
                label=sp,
            )
        ax.set_xlabel("Bill length (mm)")
        ax.set_ylabel("Count")
        ax.legend()
        return fig

# --- App ---
app = App(app_ui, server)
