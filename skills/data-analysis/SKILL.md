---
name: data-analysis
description: Analyze data using Python with pandas, numpy, and visualization libraries. Generate insights, charts, and statistical summaries.
---

# Data Analysis Skill

## Capabilities

- Load and parse data files (CSV, Excel, JSON, SQL databases)
- Data cleaning and preprocessing
- Statistical analysis and summary statistics
- Data visualization (matplotlib, seaborn, plotly)
- Exploratory data analysis (EDA)
- Correlation analysis
- Time series analysis
- Group-by and aggregation operations

## Tools Used

- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `matplotlib` - Basic plotting
- `seaborn` - Statistical visualization
- `plotly` - Interactive charts

## Usage

When the user asks to analyze data:

1. Load the data file
2. Explore structure (shape, columns, dtypes, head)
3. Check for missing values
4. Generate summary statistics
5. Create relevant visualizations
6. Provide insights and recommendations

## Example Commands

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data.csv')

# Basic exploration
print(df.shape)
print(df.columns)
print(df.describe())

# Visualization
df.plot(kind='hist')
plt.show()
```

## Notes

- Always check data types and missing values first
- Use appropriate visualizations for data types
- Provide actionable insights, not just numbers
