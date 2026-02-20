// **------Bubble_chart 1**
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

function generateData(baseval, count, yrange) {
  let i = 0;
  const series = [];
  while (i < count) {
    const y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
    const z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;

    series.push([baseval, y, z]);
    baseval += 86400000;
    i++;
  }
  return series;
}

const bubble1ChartOption = {
  series: [
    {
      name: "حباب 1",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "حباب 2",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "حباب 3",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "حباب 4",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "bubble",
  },
  dataLabels: {
    enabled: false,
  },
  fill: {
    opacity: 0.8,
  },
  title: {
    text: "",
  },
  xaxis: {
    tickAmount: 12,
    type: "datetime",
    labels: {
      style: {
        colors: [],
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
    "#E14E5A",
  ],
  yaxis: {
    max: 70,
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
      const name = w.config.series[seriesIndex].name;
      const data = w.config.series[seriesIndex].data[dataPointIndex];
      const labels = {
        size: "سایز",
      };
      return `
                    <div class="apexcharts-tooltip-box apexcharts-tooltip-custom">
                        <div><b>${name} : ${data[1]}</b></div>
                        <div class="tooltip-label">${labels.size}: <span class="value">${data[2]}</span></div>
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

const bubble1Chart = new ApexCharts(
  document.querySelector("#bubble1"),
  bubble1ChartOption
);
bubble1Chart.render();

// **------Bubble_chart 2**

const bubble2ChartOption = {
  series: [
    {
      name: "حباب سه بعدی 1",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "حباب سه بعدی 2",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "حباب سه بعدی 3",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "حباب سه بعدی 4",
      data: generateData(new Date("11 Feb 2017 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "bubble",
  },
  dataLabels: {
    enabled: false,
  },
  fill: {
    type: "gradient",
  },
  title: {
    text: "",
  },
  xaxis: {
    tickAmount: 12,
    type: "datetime",
    labels: {
      rotate: 0,
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },

  colors: ["#0F626A", "#626262", "#0AB964", "#E14E5A"],
  yaxis: {
    max: 70,
    labels: {
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  theme: {
    palette: "palette2",
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
      const name = w.config.series[seriesIndex].name;
      const data = w.config.series[seriesIndex].data[dataPointIndex];
      const labels = {
        size: "سایز",
      };
      return `
                    <div class="apexcharts-tooltip-box apexcharts-tooltip-custom">
                        <div><b>${name} : ${data[1]}</b></div>
                        <div class="tooltip-label">${labels.size}: <span class="value">${data[2]}</span></div>
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

const bubble2Chart = new ApexCharts(
  document.querySelector("#bubble2"),
  bubble2ChartOption
);
bubble2Chart.render();
