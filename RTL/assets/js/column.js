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

const basicColumOptions = {
  series: [
    {
      name: "بهره وری",
      data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
    },
    {
      name: "درآمد",
      data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
    },
    {
      name: "موجودی جاری",
      data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "bar",
    height: 350,
  },
  colors: ["#0F626A", "#0AB964", "#E14E5A"],
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "55%",
      endingShape: "rounded",
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 2,
    colors: ["transparent"],
  },
  xaxis: {
    categories: ["فرو", "ارد", "خرد", "تیر", "مرد", "شهر", "مهر", "آبا", "آذر"],
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
  fill: {
    opacity: 1,
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
  },
  tooltip: {
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    y: {
      formatter: function (val) {
        return val + " هزار";
      },
    },
  },
};

const basicColumChart = new ApexCharts(
  document.querySelector("#basic-colum"),
  basicColumOptions
);
basicColumChart.render();

// dumbell chart //

const dumbbellChartOptions = {
  series: [
    {
      data: [
        {
          x: "1398",
          y: [2800, 4500],
        },
        {
          x: "1399",
          y: [3200, 4100],
        },
        {
          x: "1400",
          y: [2950, 7800],
        },
        {
          x: "1401",
          y: [3000, 4600],
        },
        {
          x: "1402",
          y: [3500, 4100],
        },
        {
          x: "1403",
          y: [4500, 6500],
        },
        {
          x: "1404",
          y: [4100, 5600],
        },
      ],
    },
  ],
  chart: {
    height: 350,
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "rangeBar",
    zoom: {
      enabled: false,
    },
  },
  plotOptions: {
    bar: {
      isDumbbell: true,
      columnWidth: 25,
      dumbbellColors: [["#000000", "#000000"]],
    },
  },
  legend: {
    show: true,
    showForSingleSeries: true,
    position: "top",
    horizontalAlign: "right",
    customLegendItems: ["محصول آ", "محصول ب"],
  },
  colors: ["#F9C123", "#E14E5A"],
  fill: {
    type: "gradient",
    gradient: {
      type: "vertical",
      gradientToColors: ["#E14E5A"],
      inverseColors: true,
      stops: [0, 100],
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: false,
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
    tickPlacement: "on",
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
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
};

const dumbbellChart = new ApexCharts(
  document.querySelector("#Dumbbell-chart"),
  dumbbellChartOptions
);
dumbbellChart.render();

// column chart //
const columnChartOptions = {
  series: [
    {
      name: "سرویس ها",
      data: [44, 55, 41, 67, 22, 43, 21, 33, 45, 31, 87, 65, 35],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "bar",
  },
  plotOptions: {
    bar: {
      borderRadius: 10,
      columnWidth: "50%",
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 0,
  },
  xaxis: {
    labels: {
      rotate: -45,
      rotateAlways: true,
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
    categories: [
      "سیب",
      "پرتقال",
      "توت فرنگی",
      "آناناس",
      "منگو",
      "موز",
      "بلک بری",
      "گلابی",
      "هندوانه",
      "آلبالو",
      "انار",
      "گیلاس",
      "گوجه فرنگی",
    ],
    tickPlacement: "on",
  },
  colors: ["#4196FA"],
  fill: {
    type: "gradient",
    gradient: {
      shade: "light",
      type: "horizontal",
      shadeIntensity: 0.25,
      gradientToColors: undefined,
      inverseColors: true,
      opacityFrom: 0.85,
      opacityTo: 0.85,
      stops: [50, 0, 100],
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
    row: {
      colors: ["#fff", "#f2f2f2"],
    },
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

const columnChart = new ApexCharts(
  document.querySelector("#Column-chart"),
  columnChartOptions
);
columnChart.render();

// column with marker chart //
const markersChartOptions = {
  series: [
    {
      name: "واقعی",
      data: [
        {
          x: "2011",
          y: 1292,
          goals: [
            {
              name: "مورد انتظار",
              value: 1400,
              strokeHeight: 5,
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2012",
          y: 4432,
          goals: [
            {
              name: "مورد انتظار",
              value: 5400,
              strokeHeight: 5,
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2013",
          y: 5423,
          goals: [
            {
              name: "مورد انتظار",
              value: 5200,
              strokeHeight: 5,
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2014",
          y: 6653,
          goals: [
            {
              name: "مورد انتظار",
              value: 6500,
              strokeHeight: 5,
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2015",
          y: 8133,
          goals: [
            {
              name: "مورد انتظار",
              value: 6600,
              strokeHeight: 13,
              strokeWidth: 0,
              strokeLineCap: "round",
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2016",
          y: 7132,
          goals: [
            {
              name: "مورد انتظار",
              value: 7500,
              strokeHeight: 5,
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2017",
          y: 7332,
          goals: [
            {
              name: "مورد انتظار",
              value: 8700,
              strokeHeight: 5,
              strokeColor: "#F9C123",
            },
          ],
        },
        {
          x: "2018",
          y: 6553,
          goals: [
            {
              name: "مورد انتظار",
              value: 7300,
              strokeHeight: 2,
              strokeDashArray: 2,
              strokeColor: "#F9C123",
            },
          ],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "bar",
  },

  plotOptions: {
    bar: {
      columnWidth: "60%",
    },
  },
  colors: ["#eaea4f"],
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: true,
    showForSingleSeries: true,
    customLegendItems: ["واقعی", "مورد انتظار"],
    markers: {
      fillColors: ["#F9C123", "#F9C123"],
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

const markersChart = new ApexCharts(
  document.querySelector("#markers-chart"),
  markersChartOptions
);
markersChart.render();
