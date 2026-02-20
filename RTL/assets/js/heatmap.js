//  **------heatma js**
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
function generateData(count, yRange) {
  let i = 0;
  let series = [];
  while (i < count) {
    let x = (i + 1).toString();
    let y =
      Math.floor(Math.random() * (yRange.max - yRange.min + 1)) + yRange.min;

    series.push({
      x: x,
      y: y,
    });
    i++;
  }
  return series;
}
const heatmap1ChartOptions = {
  series: [
    {
      name: "اندازه 1",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 2",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 3",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 4",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 5",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 6",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 7",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 8",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 9",
      data: generateData(18, {
        min: 0,
        max: 90,
      }),
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "heatmap",
  },
  dataLabels: {
    enabled: false,
  },
  colors: [
    getLocalStorageItem("color-primary", "#0F626A"),
    getLocalStorageItem("color-secondary", "#626262"),
    "#0AB964",
    "#E14E5A",
    "#F9C123",
    "#4196FA",
    "#C8B9D2",
    "#28232D",
  ],
  title: {
    text: "",
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
    x: {
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
};

const heatmap1Chart = new ApexCharts(
  document.querySelector("#heatma1"),
  heatmap1ChartOptions
);
heatmap1Chart.render();

// **------ chart 2**
const data = [
  {
    name: "اندازه 1",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 2",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 3",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 4",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 5",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 6",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 7",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 8",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 9",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 10",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 11",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 12",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 13",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 14",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: "اندازه 15",
    data: generateData(8, {
      min: 0,
      max: 90,
    }),
  },
];

data.reverse();

const colors = [
  getLocalStorageItem("color-primary", "#0F626A"),
  getLocalStorageItem("color-secondary", "#626262"),
  "#0AB964",
  "#E14E5A",
  "#F9C123",
  "#4196FA",
  "#C8B9D2",
  "#28232D",
];

colors.reverse();
const heatmap2ChartOptions = {
  series: data,
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 450,
    type: "heatmap",
  },
  dataLabels: {
    enabled: false,
  },
  colors: colors,
  xaxis: {
    type: "category",
    categories: [
      "10:00",
      "10:30",
      "11:00",
      "11:30",
      "12:00",
      "12:30",
      "01:00",
      "01:30",
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

  title: {
    text: "",
  },
  grid: {
    padding: {
      right: 20,
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

const heatmap2Chart = new ApexCharts(
  document.querySelector("#heatma2"),
  heatmap2ChartOptions
);
heatmap2Chart.render();

//  **------chart 3**
const heatmap3ChartOptions = {
  series: [
    {
      name: "فرو",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "ارد",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "خرد",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "تیر",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "مرد",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "شهر",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "مهر",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "آبا",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
    {
      name: "آذر",
      data: generateData(20, {
        min: -30,
        max: 55,
      }),
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "heatmap",
  },
  plotOptions: {
    heatmap: {
      shadeIntensity: 0.5,
      radius: 0,
      useFillColorAsStroke: true,
      colorScale: {
        ranges: [
          {
            from: -30,
            to: 5,
            name: "پایین",
            color: getLocalStorageItem("color-primary", "#0F626A"),
          },
          {
            from: 6,
            to: 20,
            name: "متوسط",
            color: getLocalStorageItem("color-secondary", "#626262"),
          },
          {
            from: 21,
            to: 45,
            name: "بالا",
            color: "#0AB964",
          },
          {
            from: 46,
            to: 55,
            name: "بیشترین",
            color: "#E14E5A",
          },
        ],
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 1,
  },
  title: {
    text: "",
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

const heatmap3Chart = new ApexCharts(
  document.querySelector("#heatma3"),
  heatmap3ChartOptions
);
heatmap3Chart.render();

//  **------chart 4**
const heatmap4ChartOptions = {
  series: [
    {
      name: "اندازه 1",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },

    {
      name: "اندازه 2",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },

    {
      name: "اندازه 3",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },

    {
      name: "اندازه 4",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },

    {
      name: "اندازه 5",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 6",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 7",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 8",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },
    {
      name: "اندازه 8",
      data: generateData(20, {
        min: 0,
        max: 90,
      }),
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "heatmap",
  },
  stroke: {
    width: 0,
  },
  plotOptions: {
    heatmap: {
      radius: 30,
      enableShades: false,
      colorScale: {
        ranges: [
          {
            from: 0,
            to: 50,
            color: "#F9C123",
          },
          {
            from: 51,
            to: 100,
            color: "#4196FA",
          },
        ],
      },
    },
  },
  dataLabels: {
    enabled: true,
    style: {
      colors: ["#fff"],
    },
  },
  xaxis: {
    type: "category",
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
      show: false,
    },
    style: {
      fontSize: "16px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
  },
};

const heatmap4Chart = new ApexCharts(
  document.querySelector("#heatma4"),
  heatmap4ChartOptions
);
heatmap4Chart.render();
