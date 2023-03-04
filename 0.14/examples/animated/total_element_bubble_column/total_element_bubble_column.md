---
csv_url: ../../../assets/data/chart_types_eu.csv
---

# Stacked Bubble  to Column

<div id="example_01"></div>

??? info "Info - How to setup Chart"
    ```python
    import pandas as pd
    from ipyvizzu import Chart, Data, Config, Style

    data_frame = pd.read_csv(
        "https://ipyvizzu.vizzuhq.com/0.14/assets/data/chart_types_eu.csv",
        dtype={"Year": str, "Timeseries": str},
    )
    data = Data()
    data.add_data_frame(data_frame)

    chart = Chart()
    chart.animate(data)
    ```

```python
chart.animate(
    Config(
        {
            "channels": {
                "color": "Joy factors",
                "label": "Country_code",
                "size": ["Country_code", "Value 2 (+)"],
            },
            "title": "Stacked Bubble Chart",
            "geometry": "circle",
        }
    )
)

chart.animate(
    Config(
        {
            "channels": {
                "x": "Joy factors",
                "y": ["Country_code", "Value 2 (+)"],
                "label": None,
                "size": None,
            },
            "title": "Column Chart",
            "geometry": "rectangle",
            "orientation": "vertical",
        }
    )
)

chart.animate(
    Config({"channels": {"y": "Value 2 (+)", "label": "Value 2 (+)"}})
)
```

<script src="./total_element_bubble_column.js"></script>