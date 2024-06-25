import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
# dff = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]
dff = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
    ] 
# print(dff)



def draw_line_plot():
    # Draw line plot
    xpoints = dff.index
    ypoints = dff['value']

    fig, ax = plt.subplots(figsize=(10, 5))  # Create figure and axis

    ax.plot(xpoints, ypoints, color='r')  # Plot data on the axis
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')  # Save the figure before showing it
    # plt.show()  # Display the plot interactively

    return fig  # Return the figure object

# Call the function and save the returned figure
fig_line = draw_line_plot()

def draw_bar_plot():
    # Copy and prepare data
    df_bar = dff.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Create pivot table to aggregate average page views by month and year
    df_pivot = df_bar.pivot_table(values='value', index='year', columns='month', aggfunc='mean')

    # Define month order for sorting
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Sort columns (months) by defined order
    df_pivot = df_pivot.reindex(columns=month_order)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    df_pivot.plot(kind='bar', ax=ax, stacked=True)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily freeCodeCamp Forum Page Views\nby Month and Year')

    # Add legend with title
    ax.legend(title='Months', labels=month_order, loc='upper left')

    # Adjust layout and save figure
    plt.tight_layout()
    plt.savefig('bar_plot.png')
    plt.show()

    # Return the figure object for testing purposes (don't change this part)
    return fig

fig_bar = draw_bar_plot()

def draw_box_plot():
    # Prepare data for box plots
    df_box = dff.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Create figure with two subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    # Year-wise box plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], palette='Set3')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise box plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box,
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=axes[1], palette='Set3')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Adjust layout
    plt.tight_layout()

    # Save figure and show
    plt.savefig('box_plot.png')
    plt.show()

    return fig

fig_box = draw_box_plot()


