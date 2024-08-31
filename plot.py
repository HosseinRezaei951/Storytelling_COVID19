import matplotlib.pyplot as plt 
import matplotlib.ticker as tick
import numpy as np 


############################################################
## Plot Class
############################################################
class Plot(object):
    def __init__(self):
        self.title = None
        self.labels = []
        self.values = []
        self.index_values = []


    def load_data(self, title, labels, values, index_values):
        self.title = title
        self.labels = labels
        self.values = values
        self.index_values = index_values
        

    ############################################################
    ## drow_groupedBarChart
    ############################################################    
    def drow_groupedBarChart(self, barsWidth):
        labels = self.labels
        x = np.arange(len(labels))  # the label locations

        # Creating BarChart
        fig, ax = plt.subplots(1, 1, 
                        figsize =(10, 7)) 
         
        # # Add padding between axes and labels  
        ax.xaxis.set_tick_params(pad = 5)  
        ax.yaxis.set_tick_params(pad = 10)
        
        
        rects_list = []
        length = ((len(self.index_values)*barsWidth)/2) - (barsWidth/2) 
        for i in range(len(self.values)):
            rects = ax.bar((x - (barsWidth*i) + length), self.values[i], barsWidth, label=self.index_values[i])
            rects_list.append(rects)
        
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title(self.title)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        ax.grid(b = True, color ='grey',  
            linestyle ='-.', linewidth = 0.5,  
            alpha = 0.6) 

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        for rects in rects_list:
            autolabel(rects)

        fig.tight_layout()
        plt.show()