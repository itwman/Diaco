//  **------ boxplot chart 1**
Apex.chart = {
  locales: [
    {
      name: "fa",
      options: {
        months: [
          "فرور دین",
          "اردیبهشت",
          "خرداد",
          "تیر",
          "مرداد",
          "شهریور",
          "مهر",
          "آبان",
          "آذر",
          "دی",
          "بهمن",
          "اسفند",
        ],
        shortMonths: [
          "فرو",
          "ارد",
          "خرد",
          "تیر",
          "مرد",
          "شهر",
          "مهر",
          "آبا",
          "آذر",
          "دی",
          "بهمـ",
          "اسفـ",
        ],
        days: [
          "یکشنبه",
          "دوشنبه",
          "سه شنبه",
          "چهارشنبه",
          "پنجشنبه",
          "جمعه",
          "شنبه",
        ],
        shortDays: ["ی", "د", "س", "چ", "پ", "ج", "ش"],
        toolbar: {
          exportToSVG: "دانلود SVG",
          exportToPNG: "دانلود PNG",
          exportToCSV: "دانلود CSV",
          menu: "منو",
          selection: "انتخاب",
          selectionZoom: "بزرگنمایی انتخابی",
          zoomIn: "بزرگنمایی",
          zoomOut: "کوچکنمایی",
          pan: "پیمایش",
          reset: "بازنشانی بزرگنمایی",
        },
      },
    },
  ],
  defaultLocale: "fa",
};
const boxplot1ChartOption = {
  series: [
    {
      type: "boxPlot",
      data: [
        {
          x: "فرور 1396",
          y: [54, 66, 69, 75, 88],
        },
        {
          x: "فرور 1397",
          y: [43, 65, 69, 76, 81],
        },
        {
          x: "فرور 1398",
          y: [31, 39, 45, 51, 59],
        },
        {
          x: "فرور 1399",
          y: [39, 46, 55, 65, 71],
        },
        {
          x: "فرور 1400",
          y: [29, 31, 35, 39, 44],
        },
        {
          x: "فرور 1401",
          y: [41, 49, 58, 61, 67],
        },
        {
          x: "فرور 1402",
          y: [54, 59, 66, 71, 88],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "boxPlot",
    height: 350,
  },
  title: {
    text: "",
    align: "left",
    fontFamily: "Vazirmatn FD,Rubik, serif",
  },

  plotOptions: {
    boxPlot: {
      colors: {
        upper: getLocalStorageItem("color-primary", "#0F626A"),
        lower: getLocalStorageItem("color-secondary", "#626262"),
      },
    },
  },
  xaxis: {
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
    xaxis: {
      lines: {
        show: false,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
  },
  tooltip: {
    custom: function ({ seriesIndex, dataPointIndex, w }) {
      const data = w.config.series[seriesIndex].data[dataPointIndex];
      const values = data.y;

      // Custom labels
      const labels = {
        minimum: "حداقل",
        q1: "فصل1",
        median: "میانه",
        q3: "فصل3",
        maximum: "حداکثر",
        maximum: "حداکثر",
      };

      // Create custom HTML for tooltip
      return `
                    <div class="apexcharts-tooltip-box apexcharts-tooltip-custom">
                        <div class="tooltip-label">${labels.maximum}: <span class="value">${values[4]}</span></div>
                        <div class="tooltip-label">${labels.q3}: <span class="value">${values[3]}</span></div>
                        <div class="tooltip-label">${labels.median}: <span class="value">${values[2]}</span></div>
                        <div class="tooltip-label">${labels.q1}: <span class="value">${values[1]}</span></div>
                        <div class="tooltip-label">${labels.minimum}: <span class="value">${values[0]}</span></div>
                    </div>
                    `;
    },
    x: {
      show: false,
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
};

const boxplot1Chart = new ApexCharts(
  document.querySelector("#boxplot1"),
  boxplot1ChartOption
);
boxplot1Chart.render();

//  **------boxplot chart 2**
const boxplot2ChartOption = {
  series: [
    {
      name: "box",
      type: "boxPlot",
      data: [
        {
          x: new Date("1397-01-01").getTime(),
          y: [54, 66, 69, 75, 88],
        },
        {
          x: new Date("1398-01-01").getTime(),
          y: [43, 65, 69, 76, 81],
        },
        {
          x: new Date("1399-01-01").getTime(),
          y: [31, 39, 45, 51, 59],
        },
        {
          x: new Date("1400-01-01").getTime(),
          y: [39, 46, 55, 65, 71],
        },
        {
          x: new Date("1401-01-01").getTime(),
          y: [29, 31, 35, 39, 44],
        },
      ],
    },
    {
      name: "داده های پرت",
      type: "scatter",
      data: [
        {
          x: new Date("1397-01-01").getTime(),
          y: 32,
        },
        {
          x: new Date("1398-01-01").getTime(),
          y: 25,
        },
        {
          x: new Date("1399-01-01").getTime(),
          y: 64,
        },
        {
          x: new Date("1400-01-01").getTime(),
          y: 27,
        },
        {
          x: new Date("1401-01-01").getTime(),
          y: 78,
        },
        {
          x: new Date("1402-01-01").getTime(),
          y: 15,
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "boxPlot",
    height: 350,
  },
  title: {
    text: "",
    align: "left",
    fontFamily: "Vazirmatn FD,Rubik, serif",
  },
  xaxis: {
    type: "datetime",
    tooltip: {
      formatter: function (val) {
        return new Date(val).getFullYear();
      },
    },
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  plotOptions: {
    boxPlot: {
      colors: {
        upper: "#0AB964",
        lower: "#E14E5A",
      },
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
    xaxis: {
      lines: {
        show: false,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
  },
  tooltip: {
    shared: false,
    intersect: true,
    custom: function ({ seriesIndex, dataPointIndex, w }) {
      const data = w.config.series[seriesIndex].data[dataPointIndex];

      let values = data.y;
      console.log(values);

      // Custom labels
      const labels = {
        minimum: "حداقل",
        q1: "فصل1",
        median: "میانه",
        q3: "فصل3",
        maximum: "حداکثر",
      };
      if (!Array.isArray(values)) {
        values = [
          "تعریف نشده",
          "تعریف نشده",
          "تعریف نشده",
          "تعریف نشده",
          "تعریف نشده",
        ];
      }

      // Create custom HTML for tooltip
      return `
                    <div class="apexcharts-tooltip-box apexcharts-tooltip-custom">
                        <div class="tooltip-label">${labels.maximum}: <span class="value">${values[4]}</span></div>
                        <div class="tooltip-label">${labels.q3}: <span class="value">${values[3]}</span></div>
                        <div class="tooltip-label">${labels.median}: <span class="value">${values[2]}</span></div>
                        <div class="tooltip-label">${labels.q1}: <span class="value">${values[1]}</span></div>
                        <div class="tooltip-label">${labels.minimum}: <span class="value">${values[0]}</span></div>
                    </div>
                    `;
    },
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
};

const boxplot2Chart = new ApexCharts(
  document.querySelector("#boxplot2"),
  boxplot2ChartOption
);
boxplot2Chart.render();

//  **------boxplot chart 3**
const boxplot3ChartOption = {
  series: [
    {
      data: [
        {
          x: "دسته بندی آ",
          y: [54, 66, 69, 75, 88],
        },
        {
          x: "دسته بندی ب",
          y: [43, 65, 69, 76, 81],
        },
        {
          x: "دسته بندی پ",
          y: [31, 39, 45, 51, 59],
        },
        {
          x: "دسته بندی ث",
          y: [39, 46, 55, 65, 71],
        },
        {
          x: "دسته بندی د",
          y: [29, 31, 35, 39, 44],
        },
        {
          x: "دسته بندی ر",
          y: [41, 49, 58, 61, 67],
        },
        {
          x: "دسته بندی ز",
          y: [54, 59, 66, 71, 88],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "boxPlot",
    height: 350,
  },
  title: {
    text: "",
    align: "left",
    fontFamily: "Vazirmatn FD,Rubik, serif",
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: "50%",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    boxPlot: {
      colors: {
        upper: "#F9C123",
        lower: "#4196FA",
      },
    },
  },
  xaxis: {
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
    xaxis: {
      lines: {
        show: false,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
  },
  tooltip: {
    custom: function ({ seriesIndex, dataPointIndex, w }) {
      const data = w.config.series[seriesIndex].data[dataPointIndex];
      const values = data.y;

      // Custom labels
      const labels = {
        minimum: "حداقل",
        q1: "فصل1",
        median: "میانه",
        q3: "فصل3",
        maximum: "حداکثر",
      };

      // Create custom HTML for tooltip
      return `
                    <div class="apexcharts-tooltip-box apexcharts-tooltip-custom">
                        <div class="tooltip-label">${labels.maximum}: <span class="value">${values[4]}</span></div>
                        <div class="tooltip-label">${labels.q3}: <span class="value">${values[3]}</span></div>
                        <div class="tooltip-label">${labels.median}: <span class="value">${values[2]}</span></div>
                        <div class="tooltip-label">${labels.q1}: <span class="value">${values[1]}</span></div>
                        <div class="tooltip-label">${labels.minimum}: <span class="value">${values[0]}</span></div>
                    </div>
                    `;
    },
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },

  stroke: {
    colors: ["#6c757d"],
  },
};

const boxplot3Chart = new ApexCharts(
  document.querySelector("#boxplot3"),
  boxplot3ChartOption
);
boxplot3Chart.render();
