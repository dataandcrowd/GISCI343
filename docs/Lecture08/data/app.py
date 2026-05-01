from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
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
        ui.input_radio_buttons(
            "species", "Species",
            choices=["Adelie", "Gentoo", "Chinstrap"],
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

    @reactive.calc
    def filtered():
        df = penguins_geo[penguins_geo["species"] == input.species()]
        return df[df["island"].isin(input.islands())]

    @render_widget
    def map():
        sel = filtered().dropna(subset=["latitude"])
        colour = species_colours[input.species()]

        m = Map(
            center=(-64.8, -64.5),
            zoom=9,
            basemap=basemaps.Esri.WorldImagery,
        )
        for _, row in sel.iterrows():
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
        return m

    @render.text
    def summary():
        sel = filtered()
        n = len(sel.dropna(subset=["bill_length_mm"]))
        avg_mass = sel["body_mass_g"].mean()
        islands = ", ".join(sorted(sel["island"].unique()))
        return (
            f"{input.species()}: {n} penguins on {islands}, "
            f"avg body mass {avg_mass:,.0f} g"
        )

    @render.plot
    def hist():
        import matplotlib.pyplot as plt

        sel = filtered()
        colour = species_colours[input.species()]
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.hist(
            sel["bill_length_mm"].dropna(),
            bins=15,
            color=colour,
            edgecolor="white",
        )
        ax.set_xlabel("Bill length (mm)")
        ax.set_ylabel("Count")
        ax.set_title(f"{input.species()} bill lengths")
        return fig

# --- App ---
app = App(app_ui, server)
