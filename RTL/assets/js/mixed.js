// Line & Column Chart //
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
const mixed1ChartOptions = {
  series: [
    {
      name: "بلاگ وبسایت",
      type: "column",
      data: [440, 505, 414, 671, 227, 413, 201, 352, 752, 320, 257, 160],
    },
    {
      name: "شبکه اجتماعی",
      type: "line",
      data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "line",
  },
  colors: ["#0F626A", "#626263"],
  stroke: {
    width: [0, 4],
  },
  dataLabels: {
    enabled: true,
    enabledOnSeries: [1],
  },

  labels: [
    "01 فروردین",
    "02 فروردین",
    "03 فروردین",
    "04 فروردین",
    "05 فروردین",
    "06 فروردین",
    "07 فروردین",
    "08 فروردین",
    "09 فروردین",
    "10 فروردین",
    "11 فروردین",
    "12 فروردین",
  ],
  yaxis: [
    {
      labels: {
        style: {
          fontSize: "14px",
          fontWeight: 500,
          fontFamily: "Vazirmatn FD,Rubik, serif",
        },
      },
    },
    {
      opposite: true,
    },
  ],
  xaxis: {
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

const mixed1Chart = new ApexCharts(
  document.querySelector("#mixed1"),
  mixed1ChartOptions
);
mixed1Chart.render();

// ----- multiple y-axis chart ---- //
const mixed2ChartOptions = {
  series: [
    {
      name: "درآمد",
      type: "column",
      data: [1.4, 2, 2.5, 1.5, 2.5, 2.8, 3.8, 4.6],
    },
    {
      name: "جریان نقدینگی",
      type: "column",
      data: [1.1, 3, 3.1, 4, 4.1, 4.9, 6.5, 8.5],
    },
    {
      name: "سود",
      type: "line",
      data: [20, 29, 37, 36, 44, 45, 50, 58],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "line",
    stacked: false,
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: [1, 1, 4],
  },
  title: {
    text: "",
    align: "left",
    offsetX: 110,
    fontFamily: "Vazirmatn FD,Rubik, serif",
  },
  xaxis: {
    categories: [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016],
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },

  colors: ["#0F626A", "#E14E5A", "#4196FA"],
  yaxis: [
    {
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: "#AECC34",
      },
      labels: {
        style: {
          colors: "#008FFB",
          fontSize: "14px",
          fontWeight: 500,
          fontFamily: "Vazirmatn FD,Rubik, serif",
        },
      },
      title: {
        text: "",
        style: {
          color: "#008FFB",
        },
      },
      tooltip: {
        enabled: true,
      },
    },
    {
      seriesName: "درآمد",
      opposite: true,
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: "#00E396",
      },
      labels: {
        style: {
          colors: "#00E396",
        },
      },
      title: {
        text: "",
        style: {
          color: "#00E396",
        },
      },
    },
    {
      seriesName: "سود",
      opposite: true,
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: "#FEB019",
      },
      labels: {
        style: {
          colors: "#FEB019",
        },
      },
      title: {
        text: "",
        style: {
          color: "#FEB019",
        },
      },
    },
  ],
  tooltip: {
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    fixed: {
      enabled: true,
      position: "topLeft", // topRight, topLeft, bottomRight, bottomLeft
      offsetY: 30,
      offsetX: 60,
    },
  },
  legend: {
    horizontalAlign: "left",
    offsetX: 40,
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
  },
};

const mixed2Chart = new ApexCharts(
  document.querySelector("#mixed2"),
  mixed2ChartOptions
);
mixed2Chart.render();

// Line & Area Chart //
const mixed3ChartOptions = {
  series: [
    {
      name: "تیم آ",
      type: "area",
      data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33],
    },
    {
      name: "تیم ب",
      type: "line",
      data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "line",
  },
  stroke: {
    curve: "smooth",
  },
  fill: {
    type: "solid",
    opacity: [0.35, 1],
  },

  colors: ["#0AB964", "#0F626A"],
  labels: [
    "خرد 01",
    "خرد 02",
    "خرد 03",
    "خرد 04",
    "خرد 05",
    "خرد 06",
    "خرد 07",
    "خرد 08",
    "خرد 09 ",
    "خرد 10",
    "خرد 11",
  ],
  markers: {
    size: 0,
  },

  xaxis: {
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: [
    {
      title: {
        text: "",
      },
      labels: {
        style: {
          fontSize: "14px",
          fontWeight: 500,
          fontFamily: "Vazirmatn FD,Rubik, serif",
        },
      },
    },
    {
      opposite: true,
      title: {
        text: "",
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y.toFixed(0) + " امتیاز";
        }
        return y;
      },
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
  },
};

const mixed3Chart = new ApexCharts(
  document.querySelector("#mixed3"),
  mixed3ChartOptions
);
mixed3Chart.render();

// Line, Column & Area Chart //

const mixed4ChartOptions = {
  series: [
    {
      name: "تیم آ",
      type: "column",
      data: [23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30],
    },
    {
      name: "تیم ب",
      type: "area",
      data: [44, 55, 41, 67, 22, 43, 21, 41, 56, 27, 43],
    },
    {
      name: "تیم ث",
      type: "line",
      data: [30, 25, 36, 30, 45, 35, 64, 52, 59, 36, 39],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "line",
    stacked: false,
  },
  stroke: {
    width: [0, 2, 5],
    curve: "smooth",
  },
  plotOptions: {
    bar: {
      columnWidth: "50%",
    },
  },

  fill: {
    opacity: [0.85, 0.25, 1],
    gradient: {
      inverseColors: false,
      shade: "light",
      type: "vertical",
      opacityFrom: 0.85,
      opacityTo: 0.55,
      stops: [0, 100, 100, 100],
    },
  },
  labels: [
    "01/01/1404",
    "02/01/1404",
    "03/01/1404",
    "04/01/1404",
    "05/01/1404",
    "06/01/1404",
    "07/01/1404",
    "08/01/1404",
    "09/01/1404",
    "10/01/1404",
    "11/01/1404",
  ],
  markers: {
    size: 0,
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

  colors: [
    getLocalStorageItem("color-primary", "#0F626A"),
    getLocalStorageItem("color-secondary", "#626262"),
    "#0AB964",
  ],
  yaxis: {
    title: {
      text: "",
    },
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
    min: 0,
  },
  tooltip: {
    shared: true,
    intersect: false,
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y.toFixed(0) + " امتیاز";
        }
        return y;
      },
    },
  },
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
  },
};

const mixed4Chart = new ApexCharts(
  document.querySelector("#mixed4"),
  mixed4ChartOptions
);
mixed4Chart.render();
