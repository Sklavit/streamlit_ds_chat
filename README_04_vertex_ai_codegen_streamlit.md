

For testing manager, the following questions are used:

<q>How many unique fruits are there in the dataset?</q>
<q>How many fruits likes each person?</q>
<q>Make a chart which shows, how many fruits likes each person?</q>
<q>How many different kinds of fruit each person likes?</q>

### Options from VertexAI itself
<q>What is the average number of fruits liked? </q>
<q>Who likes the most number of fruits? </q>
<q>Show the distribution of fruits liked by people. </q>

## Example output to the last question:

### Attention! The response includes \```python phrase in the beginning!

```python
import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show

def run(data):
    """
    This function analyzes the provided data and returns a descriptive summary.

    Args:
        data (dict): A dictionary containing the data to be analyzed.
        It should have the same keys as <locals> and corresponding values.

    Returns:
        dict: A dictionary containing the results of the analysis.
        'results' key contains the descriptive summary of the dataset.
        'chart' key contains the plot of the distribution of fruit likes per person.
    """

    df = data['df_table']  # Access the DataFrame from the data dictionary

    # Group by person and count likes
    person_likes = df.groupby('person')['likes'].sum()

    # Create a Bokeh figure
    p = figure(title="Distribution of Fruit Likes per Person",
               x_axis_label="Person", y_axis_label="Number of Likes")

    # Add a bar chart to the figure
    p.vbar(x=person_likes.index, top=person_likes.values, width=0.5)

    # Show the chart
    show(p)

    # Return the results and chart
    return {
        'results': None,  # No specific results in this case
        'chart': {
            'chart_type': 'vbar',
            'kwargs': {
                'x': person_likes.index,
                'top': person_likes.values,
                'width': 0.5,
                'title': "Distribution of Fruit Likes per Person",
                'x_axis_label': "Person",
                'y_axis_label': "Number of Likes"
            }
        }
    }
```
