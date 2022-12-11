import pandas as pd
import plotnine as gg

flights = pd.read_csv('flights_data.csv')  
airports = pd.read_csv('airport_data.csv')  
plot_data = flights.join(airports, lsuffix='Airport Code', rsuffix='Code')

plot = (
    gg.ggplot(plot_data, gg.aes(x = 'Date', y='Total', fill='Country')) + 
      gg.geom_area()
  )
plot.draw()


labs(x = "",
           y = "Average number of flights per day", 
           title = "") +
      scale_fill_manual("", 
                        values = c("Belgium" = "#8175aa", 
                                   "France" = "#6fb899", 
                                   "Ireland" = "#31a1b3", 
                                   "Luxembourg" = "#ccb22b", 
                                   "Netherlands" = "#a39fc9", 
                                   "United Kingdom" = "#94d0c0"), 
                        labels = function(x) str_wrap(x, width = 7)) +
      guides(fill = guide_legend(nrow = 1)) +
      theme_minimal() +
      theme(legend.position = "bottom", 
            legend.title = element_blank(), 
            plot.margin = unit(c(0.5, 0.5, 0.5, 0.5), unit = "cm"), 
            panel.grid.major.x = element_blank(),
            panel.grid.minor.x = element_blank())
