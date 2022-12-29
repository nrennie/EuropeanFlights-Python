from shiny import ui, render, App
import plotnine as gg
import pandas as pd
from mizani.breaks import date_breaks
from mizani.formatters import date_format

# read in data
flights = pd.read_csv('flights_data.csv')  

# Function for UI
def create_ui(data: pd.DataFrame):
  # create our ui object
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
        ui.column(10,
          ui.output_plot("barplot")
        ), 
        # controls
        ui.column(2, 
          ui.markdown(
            """
            ### **Controls**
            
            Use the selectors below to choose a set of countries to explore.
    
            """
          ),
          ui.input_checkbox_group(
              "country", "Country",
              choices=["Belgium", "France", "Ireland", "Luxembourg", "Netherlands", "United Kingdom"],
              selected=["Belgium", "France", "Ireland", "Luxembourg", "Netherlands", "United Kingdom"]
          )
        )
    )
  )
  return app_ui

ui_obj = create_ui(flights)

# Function to make the plot
def create_plot(data):
  plot = (
    gg.ggplot(data = data, mapping = gg.aes(x = 'Date', y='Total', fill='Country')) +
      gg.geom_col() +
      gg.theme_minimal() +
      gg.labs(x = "", y = "Total number of flights per week", title="Total number of flights per week") +
      gg.scale_x_datetime(breaks=date_breaks('1 years'), labels=date_format('%Y')) +
      gg.scale_fill_brewer(type="qual", palette = "Dark2") +
      gg.theme(panel_grid_major_x = gg.element_blank(),
               panel_grid_minor_x = gg.element_blank())
  )
  return plot.draw()

# Function for the server
def create_server(data):
  def f(input, output, session):
  
    @output(id = "barplot")
    @render.plot
    def plot():
      country = list(input.country())
      new_data = data[data['Country'].isin(country)]
      plot = create_plot(new_data)
      return plot
  return f

server = create_server(flights)

app = App(ui_obj, server)