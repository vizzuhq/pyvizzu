---
csv_url: ../../../assets/data/chart_types_eu.csv
---

# Area Chart with (-) Nums

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
                "x": "Year",
                "y": "Value 5 (+/-)",
                "label": "Value 5 (+/-)",
            },
            "title": "Area Chart with (-) Nums",
            "geometry": "area",
        }
    )
)
```

<script src="./area_negative_1dis_1con.js"></script>