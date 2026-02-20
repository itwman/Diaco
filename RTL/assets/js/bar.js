// basic bar chart //
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
const basicBarOptions = {
  series: [
    {
      name: "سری 1",
      data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "bar",
    height: 350,
  },
  colors: ["#2e5ce2"],
  plotOptions: {
    bar: {
      borderRadius: 4,
      borderRadiusApplication: "end",
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: false,
  },
  xaxis: {
    categories: [
      "کره جنوبی",
      "کانادا",
      "انگلیس",
      "سوئیس",
      "ایتالیا",
      "فرانسه",
      "ژاپن",
      "ایالات متحده",
      "چین",
      "آلمان",
    ],
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
  tooltip: {
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
  },
};

const basicBarChart = new ApexCharts(
  document.querySelector("#basic-bar"),
  basicBarOptions
);
basicBarChart.render();

// Patterned bar chart //

const patternedBarOptions = {
  series: [
    {
      name: "اسپرایت دریایی",
      data: [44, 55, 41, 37, 22, 43, 21],
    },
    {
      name: "گوساله",
      data: [53, 32, 33, 52, 13, 43, 32],
    },
    {
      name: "تصویر تانک",
      data: [12, 17, 11, 9, 15, 11, 20],
    },
    {
      name: "سطل",
      data: [9, 7, 5, 8, 6, 9, 4],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "bar",
    height: 350,
    stacked: true,
    dropShadow: {
      enabled: true,
      blur: 1,
      opacity: 0.25,
    },
  },
  colors: ["#0F626A", "#0AB964", "#E14E5A", "#F9C123"],
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: "60%",
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 2,
  },

  xaxis: {
    categories: [2008, 2009, 2010, 2011, 2012, 2013, 2014],
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },

  yaxis: {
    title: {
      text: undefined,
    },
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  fill: {
    type: "pattern",
    opacity: 1,
    pattern: {
      style: ["circles", "slantedLines", "verticalLines", "horizontalLines"], // string or array of strings
    },
  },
  states: {
    hover: {
      filter: "none",
    },
  },
  legend: {
    position: "right",
    offsetY: 40,
    fontFamily: "Vazirmatn FD,Rubik, serif",
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
  },
  tooltip: {
    shared: false,
    y: {
      formatter: function (val) {
        return val + "هزار";
      },
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

const patternedBarChart = new ApexCharts(
  document.querySelector("#Patterned-bar"),
  patternedBarOptions
);
patternedBarChart.render();

// stacked bar charts //
const stackedChartOptions = {
  series: [
    {
      name: "اسپرایت دریایی",
      data: [44, 55, 41, 37, 22, 43, 21],
    },
    {
      name: "گوساله",
      data: [53, 32, 33, 52, 13, 43, 32],
    },
    {
      name: "تصویر تانک",
      data: [12, 17, 11, 9, 15, 11, 20],
    },
    {
      name: "سطل",
      data: [9, 7, 5, 8, 6, 9, 4],
    },
    {
      name: "بچه",
      data: [25, 12, 19, 32, 25, 24, 10],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "bar",
    height: 350,
    stacked: true,
  },
  colors: ["#0F626A", "#626262", "#0AB964", "#E14E5A", "#F9C123"],
  plotOptions: {
    bar: {
      horizontal: true,
      dataLabels: {
        total: {
          enabled: true,
          offsetX: 0,
          style: {
            fontSize: "13px",
            fontWeight: 900,
            fontFamily: "Vazirmatn FD,Rubik, serif",
          },
        },
      },
    },
  },
  stroke: {
    width: 1,
    colors: ["#fff"],
    fontFamily: "Vazirmatn FD,Rubik, serif",
  },
  xaxis: {
    categories: [2008, 2009, 2010, 2011, 2012, 2013, 2014],
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: {
    title: {
      text: undefined,
    },
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
  legend: {
    position: "top",
    horizontalAlign: "left",
    offsetX: 40,
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
        return val + "هزار";
      },
    },
  },
};

const stackedChart = new ApexCharts(
  document.querySelector("#stacked-chart"),
  stackedChartOptions
);
stackedChart.render();

// Grouped Stacked Bars chart //
const groupedChartOptions = {
  series: [
    {
      name: "بودجه فصل 1",
      group: "budget",
      data: [44000, 55000, 41000, 67000, 22000],
    },
    {
      name: "واقعی فصل 1",
      group: "actual",
      data: [48000, 50000, 40000, 65000, 25000],
    },
    {
      name: "بودجه فصل 2",
      group: "budget",
      data: [13000, 36000, 20000, 8000, 13000],
    },
    {
      name: "واقعی فصل 2",
      group: "actual",
      data: [20000, 40000, 25000, 10000, 12000],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    type: "bar",
    height: 350,
    stacked: true,
  },
  colors: ["#E14E5A", "#4196FA"],
  stroke: {
    width: 1,
    colors: ["#fff"],
  },
  dataLabels: {
    formatter: (val) => {
      return val / 1000 + " هزار ";
    },
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
  },
  xaxis: {
    categories: [
      "تبلیغات آنلاین",
      "آموزش فروش",
      "تبلیغات کاغذی",
      "کاتالوگ",
      "میتینگ",
    ],
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

  legend: {
    position: "top",
    horizontalAlign: "left",
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

const groupedChart = new ApexCharts(
  document.querySelector("#Grouped-chart"),
  groupedChartOptions
);
groupedChart.render();
