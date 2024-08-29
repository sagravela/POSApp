from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from backend.services import get_transactions, get_most_items

class Plots(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        plt.style.use('ggplot')
        self.axis_fontsize = 10
        self.title_fontsize = 10
        self.ticks_fontsize = 8

        # Number of items to display in barh
        self.limit = 5

        # Create a figure
        self.figure = Figure()
        
        # Create a canvas to render the figure
        self.canvas = FigureCanvas(self.figure)
        
        # Create the plot
        self.generate_plots()

        # Create a v_layout and add the canvas
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.canvas)
        self.setLayout(v_layout)

    def generate_plots(self):
        # Clear the figure
        self.figure.clear()
        
        # Create a GridSpec layout to arrange subplots
        gs = self.figure.add_gridspec(2, 2, height_ratios=[2, 1])

        # Total Sales Plot
        self.total_sales_plot(self.figure.add_subplot(gs[0, :]))

        # Get the most sold items
        data = get_most_items()
        most_sold_items = data[-self.limit:]

        # Most sold items
        self.most_sell_items_plot(self.figure.add_subplot(gs[1, 0]), most_sold_items)

        # Less sold items
        less_sold_items = data[:self.limit]
        self.less_sell_items_plot(self.figure.add_subplot(gs[1, 1]), less_sold_items)

        # Add padding between first and second row
        self.figure.subplots_adjust(hspace=0.8)
        # Refresh canvas
        self.canvas.draw()

    def total_sales_plot(self, ax):
        dates, total_sales = get_transactions()
        
        # Plot data with a line and markers
        ax.plot(dates, total_sales, linestyle='--', marker='o', color='g', markersize=5, linewidth=1, label='Total Sales')

        # Add labels and title
        ax.set_xlabel('Date', fontsize=self.axis_fontsize)
        ax.set_ylabel('Total Sales', fontsize=self.axis_fontsize)
        ax.set_title('Total Sales Over Time', fontsize=self.title_fontsize)

        # Improve date formatting on the x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Set date locator to tick every 15 days
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))

        # Rotate date labels for better readability
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment('right')
        
        # Set the font size of the tick labels
        ax.tick_params(axis='both', which='major', labelsize=self.ticks_fontsize)
    
    def most_sell_items_plot(self, ax, data):      
        items = [item[0] for item in data]
        quantity = [item[1] for item in data]

        # Create a bar chart
        bars = ax.barh(items, quantity, color='lightblue')

        # Add labels and title
        ax.set_xlabel('Total Quantity Sold', fontsize=self.axis_fontsize)
        ax.set_title('Most Sold Items', fontsize=self.title_fontsize)

        self.configure_plot(ax, bars, items)

    def less_sell_items_plot(self, ax, data):
        items = [item[0] for item in data]
        quantity = [item[1] for item in data]

        # Create a bar chart
        bars = ax.barh(items, quantity, color='lightcoral')

        # Add labels and title
        ax.invert_xaxis()
        ax.yaxis.tick_right()
        ax.set_xlabel('Total Quantity Sold', fontsize=self.axis_fontsize)
        ax.set_title('Less Sold Items', fontsize=self.title_fontsize)

        self.configure_plot(ax, bars, items)

    def configure_plot(self, ax, bars, items):
        # Set the font size of the tick labels
        ax.tick_params(axis='both', which='major', labelsize=self.ticks_fontsize)

        # Get the center position of the x-axis
        x_center = ax.get_xlim()[0] / 2

        # Place the y-tick labels inside the bars
        ax.yaxis.set_ticks([])  # Hide y-ticks
        for bar, label in zip(bars, items):
            width = bar.get_width()
            x_position = width / 2 if width > x_center // 4 else x_center  # Minimum x-position when width is 0
            ax.text(x_position, bar.get_y() + bar.get_height() / 2,
                    label, ha='center', va='center', fontsize=self.ticks_fontsize, color='black')


class AnalyticsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the Matplotlib widget
        self.plot_widget = Plots(self)

        # Create a layout and add the Matplotlib widget
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.plot_widget)

        # Set the v_layout for this tab
        self.setLayout(v_layout)
