from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from backend.services import get_transactions, sold_items_sorted

class Plots(QWidget):
    """
    A QWidget that generates and displays plots for sales data.

    The Plots class provides a graphical representation of sales data,
    including total sales over time and the most and least sold items.
    It utilizes Matplotlib for plotting and offers functionality to
    refresh and display these plots.
    """
    def __init__(self, parent: QWidget=None):
        """
        Initializes the Plots widget.

        The constructor sets up the plot style, font sizes, and the figure 
        for displaying the plots. A canvas is created to render the figure, 
        and a vertical layout is used to arrange the canvas within the widget.
        
        Parameters
        ----------
        parent : QWidget, optional
            The parent widget for the POS tab. Defaults to None.        
        """
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
        """
        Generates and refreshes the sales data plots.

        Clears the current figure and arranges the plots using a grid layout.
        Displays the total sales over time and the most and least sold items
        as horizontal bar charts. The canvas is updated to reflect changes.
        """
        # Clear the figure
        self.figure.clear()
        
        # Create a GridSpec layout to arrange subplots
        gs = self.figure.add_gridspec(2, 2, height_ratios=[2, 1])

        # Total Sales Plot
        self.total_sales_plot(self.figure.add_subplot(gs[0, :]))

        # Get the most sold items
        data = sold_items_sorted()
        most_sold_items = data[-self.limit:]

        # Most sold items
        self.most_sold_items_plot(self.figure.add_subplot(gs[1, 0]), most_sold_items)

        # Less sold items
        less_sold_items = data[:self.limit]
        self.least_sold_items_plot(self.figure.add_subplot(gs[1, 1]), less_sold_items)

        # Add padding between first and second row
        self.figure.subplots_adjust(hspace=0.8)
        # Refresh canvas
        self.canvas.draw()

    def total_sales_plot(self, ax):
        """
        Plots total sales over time.

        The method retrieves the sales data and plots it on a line chart 
        with markers. It sets appropriate labels, titles, and formats the 
        x-axis to show dates, with a locator set to tick every 15 days.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axes object where the plot will be drawn.
        """
        dates, total_sales = get_transactions()
        
        # Plot data with a line and markers
        ax.plot(dates, total_sales, linestyle='--', marker='o', color='g', markersize=5, linewidth=1, label='Total Sales')

        # Add title
        ax.set_title('Total Sales Over Time', fontsize=self.title_fontsize)

        # Improve date formatting on the x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        # Fix date locator to tick every 15 days
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))

        # Rotate date labels for better readability
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment('right')
        
        # Set the font size of the tick labels
        ax.tick_params(axis='both', which='major', labelsize=self.ticks_fontsize)
    
    def most_sold_items_plot(self, ax, data: list[tuple]):      
        """
        Plots the most sold items as a horizontal bar chart.

        The method takes sales data, extracts the top-selling items, 
        and displays them in a bar chart. It also configures the plot 
        for visual appeal.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes
            The Matplotlib axes object where the plot will be drawn.
        data : list of tuples
            A list of tuples containing item names and quantities sold.
        """
        items = [item[0] for item in data]
        quantity = [item[1] for item in data]

        # Create a bar chart
        bars = ax.barh(items, quantity, color='lightblue')

        # Add labels and title
        ax.set_title('Most Sold Items', fontsize=self.title_fontsize)

        self.configure_plot(ax, bars, items)

    def least_sold_items_plot(self, ax, data: list[tuple]):
        """
        Plots the least sold items as a horizontal bar chart.

        This method is similar to `most_sold_items_plot`, but it inverts
        the x-axis to emphasize the lower quantities and displays the 
        least sold items.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes
            The Matplotlib axes object where the plot will be drawn.
        data : list of tuples
            A list of tuples containing item names and quantities sold.
        """        
        items = [item[0] for item in data]
        quantity = [item[1] for item in data]

        # Create a bar chart
        bars = ax.barh(items, quantity, color='lightcoral')

        # Add labels and title
        ax.invert_xaxis()
        ax.yaxis.tick_right()
        ax.set_title('Less Sold Items', fontsize=self.title_fontsize)

        self.configure_plot(ax, bars, items)

    def configure_plot(self, ax, bars: list, items: list[str]):
        """
        Configures the plot by adjusting tick labels and placing item names inside the bars.

        The method customizes the appearance of the bar chart, including font sizes and 
        positioning of labels within the bars for better readability.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axes object where the plot is drawn.
        bars : list of matplotlib.patches.Rectangle
            The bars of the chart.
        items : list of str
            The item names corresponding to each bar.
        """
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
    """
    A QWidget that represents the analytics tab of the POSApp.

    The AnalyticsTab class contains the plots for sales data and allows 
    refreshing of the plots through the `redraw` method.
    """
    def __init__(self, parent: QMainWindow = None):
        """
        Initializes the AnalyticsTab widget.

        The constructor sets up the Plots widget and arranges it using a 
        vertical layout. The Plots widget is embedded within this tab.
        
        Parameters
        ----------
        parent : QMainWindow, optional
            The parent widget for the Analytics tab. Defaults to None.
        """
        super().__init__(parent)

        # Create the Matplotlib widget
        self.plot_widget = Plots(self)

        # Create a layout and add the Matplotlib widget
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.plot_widget)

        # Set the v_layout for this tab
        self.setLayout(v_layout)

    def redraw(self):
        """
        Redraws the plots by calling the generate_plots method.

        This method refreshes the sales data plots to display the most 
        recent data.
        """
        # Call the generate_plots method to refresh the plots
        self.plot_widget.generate_plots()
