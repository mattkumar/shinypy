from shiny import *
from shiny.types import FileInfo
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


app_ui = app_ui = ui.page_fluid(
    # CSS
    ui.tags.style(
        """
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        
        body {font-family: 'Press Start 2P', cursive;
              background-image: url('https://www.androidguys.com/wp-content/uploads/2016/04/8bit_wallpaper7.jpg');
        }
        """
    ),
    ui.tags.link(href = "https://unpkg.com/nes.css@2.3.0/css/nes.min.css", rel="stylesheet"),
    
    # App Title
    ui.h2({"style": "text-align: center;"}, "Shiny Meets Python: An Experiment"),
    ui.tags.br(),
    
    # Single Row
    ui.row(
        # Column 1 - inputs
        ui.column(
            3,
            ui.div(
                {"class": "nes-balloon from-left nes-pointer"},
                """
                Upload a CSV to use for linear regression. You can also use sample data.
                """,
                ui.tags.br(), ui.tags.br(),ui.tags.br(),
                    ui.input_file("file1", "Choose File", accept=[".csv"], multiple=False),
                    ui.tags.br(),  
                    ui.input_action_button("use_sample","Use Sample"),
                    ui.tags.br(), ui.tags.br(),  
                    ui.output_ui("controls"),
                
            ),
            ui.tags.i({"class": "nes-mario"}),
        ),
        # Column 2 - output
        ui.column(
             9,
             ui.div(
                ui.tags.br(),
                ui.output_plot("p"),
             ), 
           ),
        ),
)

def server(input, output, session):
    @reactive.Calc
    def data():
        if input.use_sample():
            infile = Path(__file__).parent / "adsl.csv"
            df = pd.read_csv(infile)
            return df
        f: list[FileInfo] = input.file1()
        with open(f[0]["datapath"], 'rb') as z:
            df = pd.read_csv(z)
        return df
    
    @output
    @render.ui
    def controls():
      req(input.use_sample() or input.file1())
      return ui.TagList(
          ui.input_select("x", "Explanatory:", data().select_dtypes(include=np.number).columns.tolist()),
          ui.input_select("y", "Response:", data().select_dtypes(include=np.number).columns.tolist()),
          ui.input_select("trt", "Treatment:", list(data()))
      )

    @output
    @render.plot
    def p():
      req(input.use_sample() or input.file1())
      sns.set(rc={'axes.facecolor':'#79C9FA', 'figure.facecolor':'#79C9FA'})
      g = sns.lmplot(data=data(),
                     x=input.x(),
                     y=input.y(),
                     hue=input.trt(),
                     palette = sns.color_palette("bright"))
      return sns.move_legend(g, "lower center", bbox_to_anchor=(.5, 1), ncol=3, title=None, frameon=False,)
       

app = App(app_ui, server)
