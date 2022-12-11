from shiny import ui, render, App
import plotnine as gg
import pandas as pd

app_ui = ui.page_fluid(
  ui.panel_title("European Flights"),
  ui.markdown(
        """
        The number of flights arriving or leaving from European airports saw a dramatic decrease with the onset of the Covid-19 pandemic in March 2020. Amsterdam - Schipol remains the busiest airport, averaging 1,150 flights per day since January 2016.
        
        Data: [Eurocontrol](https://ansperformance.eu/data/)

        """
    ),
  ui.row(
    # bar chart output
    ui.column(5), 
    # area chart output
    ui.column(5), 
    # controls
    ui.column(2, 
      ui.markdown(
        """
        ### **Controls**
        
        Use the selectors below to choose a date range and set of countries to explore.

        """
      ),
      ui.input_date_range(
        "date", "Date",
        start = "2016-01-01",
        end = "2022-05-31",
        min = "2016-01-01",
        max = "2022-05-31"
      ),
      ui.input_checkbox_group(
          "country", "Country",
          choices=["Belgium", "France", "Ireland", "Luxembourg", "Netherlands", "United Kingdom"],
          selected=["Belgium", "France", "Ireland", "Luxembourg", "Netherlands", "United Kingdom"]
        )
    )
  )
)

def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is {input.n() * 2}"

# This is a shiny.App object. It must be named `app`.
app = App(app_ui, server)
