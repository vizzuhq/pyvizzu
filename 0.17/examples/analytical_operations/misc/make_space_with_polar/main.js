
const dataLoaded = import("../../../../assets/data/chart_types_eu.js");
const mdChartLoaded = import("../../../../assets/javascripts/mdchart.js");
  
Promise.all([dataLoaded, mdChartLoaded]).then((results) => {
  const data_8 = results[0].data_8;
  const MdChart = results[1].default;
  const mdchart = new MdChart(data_8, "./vizzu.js", "example");

  mdchart.create([
    {
      anims: [
        (chart) =>
		chart.animate({
			data: data_8,
			config: {
				channels: {
					x: 'Value 2 (+)',
					y: 'Country',
					color: 'Country'
				}
			}
		}),(chart) =>
		chart.animate({
			config: {
				channels: {
					x: ['Value 2 (+)'],
					y: {
						set: 'Country',
						/* Setting the radius of
                    the empty circle in the centre. */
						range: {
							min: '-30%'
						}
					},
					size: null
				},

				coordSystem: 'polar'
			},
			style: {
				plot: {
					paddingLeft: '25em'
				}
			}
		})
      ]
    }
  ]);
});

