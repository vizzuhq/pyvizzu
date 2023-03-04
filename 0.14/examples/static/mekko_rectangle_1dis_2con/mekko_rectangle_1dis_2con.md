---
csv_url: ../../../assets/data/chart_types_eu_data_4.csv
---

# Mekko Chart

<div id="example_01"></div>

??? info "Info - How to setup Chart"
    ```python
    import pandas as pd
    from ipyvizzu import Chart, Data, Config, Style

    data_frame = pd.read_csv(
        "https://ipyvizzu.vizzuhq.com/0.14/assets/data/chart_types_eu_data_4.csv",
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
                "x": ["Country", "Value 2 (+)"],
                "y": {
                    "set": ["Value 1 (+)"],
                    "range": {"max": "110%"},
                },
                "color": "Country",
                "label": ["Value 2 (+)", "Country"],
            },
            "title": "Mekko Chart",
        }
    )
)
```

<script src="./mekko_rectangle_1dis_2con.js"></script>