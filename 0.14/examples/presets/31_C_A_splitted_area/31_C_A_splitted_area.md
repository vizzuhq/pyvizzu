---
csv_url: ../../../assets/data/chart_types_eu_data_6.csv
---

# Splitted Area Chart

<div id="example_01"></div>

??? info "Info - How to setup Chart"
    ```python
    import pandas as pd
    from ipyvizzu import Chart, Data, Config, Style

    data_frame = pd.read_csv(
        "https://ipyvizzu.vizzuhq.com/0.14/assets/data/chart_types_eu_data_6.csv",
        dtype={"Year": str, "Timeseries": str},
    )
    data = Data()
    data.add_data_frame(data_frame)

    chart = Chart()
    chart.animate(data)
    ```

```python
chart.animate(
    Config.splittedArea(
        {
            "x": "Year",
            "y": "Value 2 (+)",
            "splittedBy": "Country",
            "title": "Splitted Area Chart",
        }
    )
)
```

<script src="./31_C_A_splitted_area.js"></script>