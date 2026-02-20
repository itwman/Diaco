// basic chart //
Apex.chart = {
  locales: [
    {
      name: "fa",
      options: {
        months: [
          "فروردین",
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

const areaChartOptions = {
  series: [
    {
      name: "رومیزی",
      data: [10, 51, 35, 51, 59, 62, 79, 91, 148],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "area",
    zoom: {
      enabled: false,
    },
  },
  colors: ["rgba(var(--primary),1)"],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
  },
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      colorStops: [
        {
          offset: 0,
          color: "rgba(var(--primary),1)",
          opacity: 1,
        },
        {
          offset: 50,
          color: "rgba(var(--primary),1)",
          opacity: 1,
        },
        {
          offset: 100,
          color: "rgba(var(--primary),.1)",
          opacity: 0.1,
        },
      ],
    },
  },
  xaxis: {
    categories: ["فرو", "ارد", "خرد", "تیر", "مرد", "شهر", "مهر", "آبا", "آذر"],
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
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
};

const areaChart = new ApexCharts(
  document.querySelector("#area-basic-chart"),
  areaChartOptions
);
areaChart.render();

// spline chart //
const spLineChartOptions = {
  series: [
    {
      name: "سری 1",
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: "سری 2",
      data: [11, 32, 45, 32, 34, 52, 41],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "area",
  },
  colors: ["#eaea4f", "#147534"], // Different colors for each series
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 1,
      opacityTo: 0,
      stops: [0, 100], // Stops for the gradient
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
  },
  xaxis: {
    type: "datetime",
    categories: [
      "1404-09-19T00:00:00.000Z",
      "1404-09-19T01:30:00.000Z",
      "1404-09-19T02:30:00.000Z",
      "1404-09-19T03:30:00.000Z",
      "1404-09-19T04:30:00.000Z",
      "1404-09-19T05:30:00.000Z",
      "1404-09-19T06:30:00.000Z",
    ],
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
  tooltip: {
    x: {
      format: "yy/MM/dd HH:mm",
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
};

const spLineChart = new ApexCharts(
  document.querySelector("#Spline-chart"),
  spLineChartOptions
);
spLineChart.render();

// timeseries chart //
const timeSeriesOptions = {
  series: [
    {
      name: "محصول 1",
      data: [
        [new Date("01/01/1404").getTime(), 4500000],
        [new Date("01/03/1404").getTime(), 4800000],
        [new Date("01/07/1404").getTime(), 4700000],
        [new Date("01/11/1404").getTime(), 4600000],
        [new Date("01/15/1404").getTime(), 4500000],
      ],
    },
    {
      name: "محصول 2",
      data: [
        [new Date("01/02/1404").getTime(), 3500000],
        [new Date("01/06/1404").getTime(), 3600000],
        [new Date("01/10/1404").getTime(), 3400000],
        [new Date("01/14/1404").getTime(), 3500000],
        [new Date("01/18/1404").getTime(), 3700000],
      ],
    },
    {
      name: "محصول 3",
      data: [
        [new Date("01/03/1404").getTime(), 2500000],
        [new Date("01/05/1404").getTime(), 2700000],
        [new Date("01/09/1404").getTime(), 2600000],
        [new Date("01/13/1404").getTime(), 2800000],
        [new Date("01/17/1404").getTime(), 3000000],
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "area",
    stacked: false,
    height: 350,
    zoom: {
      enabled: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  markers: {
    size: 0,
  },
  colors: ["#0AB964", "#E14E5A", "#F9C123"],
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.45,
      opacityTo: 0.05,
      stops: [20, 100, 100, 100],
    },
  },
  yaxis: {
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
      offsetX: 0,
      formatter: function (val) {
        return (val / 1000000).toFixed(2); // Format as millions
      },
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  xaxis: {
    type: "datetime",
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },

  tooltip: {
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
  legend: {
    position: "top",
    horizontalAlign: "right",
    offsetX: -10,
  },
};

const timeSeriesChart = new ApexCharts(
  document.querySelector("#timeseries-chart"),
  timeSeriesOptions
);
timeSeriesChart.render();

// null area chart //

const nullChartOptions = {
  series: [
    {
      name: "شبکه",
      data: [
        {
          x: "Dec 23 2017",
          y: null,
        },
        {
          x: "Dec 24 2017",
          y: 44,
        },
        {
          x: "Dec 25 2017",
          y: 31,
        },
        {
          x: "Dec 26 2017",
          y: 38,
        },
        {
          x: "Dec 27 2017",
          y: null,
        },
        {
          x: "Dec 28 2017",
          y: 32,
        },
        {
          x: "Dec 29 2017",
          y: 55,
        },
        {
          x: "Dec 30 2017",
          y: 51,
        },
        {
          x: "Dec 31 2017",
          y: 67,
        },
        {
          x: "Jan 01 2018",
          y: 22,
        },
        {
          x: "Jan 02 2018",
          y: 34,
        },
        {
          x: "Jan 03 2018",
          y: null,
        },
        {
          x: "Jan 04 2018",
          y: null,
        },
        {
          x: "Jan 05 2018",
          y: 11,
        },
        {
          x: "Jan 06 2018",
          y: 4,
        },
        {
          x: "Jan 07 2018",
          y: 15,
        },
        {
          x: "Jan 08 2018",
          y: null,
        },
        {
          x: "Jan 09 2018",
          y: 9,
        },
        {
          x: "Jan 10 2018",
          y: 34,
        },
        {
          x: "Jan 11 2018",
          y: null,
        },
        {
          x: "Jan 12 2018",
          y: null,
        },
        {
          x: "Jan 13 2018",
          y: 13,
        },
        {
          x: "Jan 14 2018",
          y: null,
        },
      ],
    },
  ],
  chart: {
    type: "area",
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    animations: {
      enabled: false,
    },
    zoom: {
      enabled: false,
    },
  },

  colors: ["rgba(var(--secondary))"],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "straight",
  },
  fill: {
    opacity: 0.8,
    type: "pattern",
    pattern: {
      style: ["verticalLines", "horizontalLines"],
      width: 5,
      height: 6,
    },
  },
  markers: {
    size: 5,
    hover: {
      size: 9,
    },
  },
  tooltip: {
    x: {
      show: false,
    },
    style: {
      fontFamily: "Vazirmatn FD,Rubik, serif",
      fontSize: "16px",
    },
  },
  theme: {
    palette: "palette1",
  },
  xaxis: {
    type: "datetime",
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: {
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
};

const nullChart = new ApexCharts(
  document.querySelector("#null-chart"),
  nullChartOptions
);
nullChart.render();
