// Basic Timeline Chart//
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

const timeline1Options = {
  series: [
    {
      data: [
        {
          x: "کد",
          y: [
            new Date("1399-03-02").getTime(),
            new Date("1399-03-04").getTime(),
          ],
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-04").getTime(),
            new Date("1399-03-08").getTime(),
          ],
        },
        {
          x: "اعتبارسنجی",
          y: [
            new Date("1399-03-08").getTime(),
            new Date("1399-03-12").getTime(),
          ],
        },
        {
          x: "پیاده سازی",
          y: [
            new Date("1399-03-12").getTime(),
            new Date("1399-03-18").getTime(),
          ],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "rangeBar",
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
  },
  xaxis: {
    type: "datetime",
    labels: {
      rotate: -30,
      rotateAlways: true,
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
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  colors: [getLocalStorageItem("color-primary", "#0F626A")],
  responsive: [
    {
      breakpoint: 768,
      options: {
        chart: {
          height: 280,
        },
      },
    },
  ],
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

const timeline1Chart = new ApexCharts(
  document.querySelector("#timeline1"),
  timeline1Options
);
timeline1Chart.render();

// Different color for each bar chart //

const timeline2ChartOptions = {
  series: [
    {
      data: [
        {
          x: "تحلیل",
          y: [
            new Date("1399-02-27").getTime(),
            new Date("1399-03-04").getTime(),
          ],
          fillColor: getLocalStorageItem("color-secondary", "#626262"),
        },
        {
          x: "طراحی",
          y: [
            new Date("1399-03-04").getTime(),
            new Date("1399-03-08").getTime(),
          ],
          fillColor: "#0AB964",
        },
        {
          x: "کدنویسی",
          y: [
            new Date("1399-03-07").getTime(),
            new Date("1399-03-10").getTime(),
          ],
          fillColor: "#E14E5A",
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-08").getTime(),
            new Date("1399-03-12").getTime(),
          ],
          fillColor: "#F9C123",
        },
        {
          x: "پیاده سازی",
          y: [
            new Date("1399-03-12").getTime(),
            new Date("1399-03-17").getTime(),
          ],
          fillColor: "#4196FA",
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "rangeBar",
  },
  plotOptions: {
    bar: {
      horizontal: true,
      distributed: true,
      dataLabels: {
        hideOverflowingLabels: false,
      },
    },
  },
  dataLabels: {
    enabled: true,
    formatter: function (val, opts) {
      let label = opts.w.globals.labels[opts.dataPointIndex];
      let a = moment(val[0]);
      let b = moment(val[1]);
      let diff = b.diff(a, "days");
      return label + ": " + diff + (diff > 1 ? " روز" : " روز");
    },
    style: {
      colors: ["#f3f4f5", "#fff"],
    },
  },
  xaxis: {
    type: "datetime",
    labels: {
      rotate: -30,
      rotateAlways: true,
      style: {
        colors: [],
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  yaxis: {
    show: false,
    labels: {
      style: {
        fontSize: "14px",
        fontWeight: 500,
        fontFamily: "Vazirmatn FD,Rubik, serif",
      },
    },
  },
  responsive: [
    {
      breakpoint: 768,
      options: {
        chart: {
          height: 280,
        },
        yaxis: {
          show: false,
        },
      },
    },
  ],
  grid: {
    show: true,
    borderColor: "rgba(var(--dark),.2)",
    strokeDashArray: 2,
    row: {
      opacity: 1,
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

const timeline2Chart = new ApexCharts(
  document.querySelector("#timeline2"),
  timeline2ChartOptions
);
timeline2Chart.render();

// Multi-series Timeline //

const timeline3ChartOptions = {
  series: [
    {
      name: "باب",
      data: [
        {
          x: "طراحی",
          y: [
            new Date("1399-03-05").getTime(),
            new Date("1399-03-08").getTime(),
          ],
        },
        {
          x: "کد",
          y: [
            new Date("1399-03-08").getTime(),
            new Date("1399-03-11").getTime(),
          ],
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-11").getTime(),
            new Date("1399-03-16").getTime(),
          ],
        },
      ],
    },
    {
      name: "جو",
      data: [
        {
          x: "طراحی",
          y: [
            new Date("1399-03-02").getTime(),
            new Date("1399-03-05").getTime(),
          ],
        },
        {
          x: "کد",
          y: [
            new Date("1399-03-06").getTime(),
            new Date("1399-03-09").getTime(),
          ],
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-10").getTime(),
            new Date("1399-03-19").getTime(),
          ],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "rangeBar",
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      let a = moment(val[0]);
      let b = moment(val[1]);
      let diff = b.diff(a, "days");
      return diff + (diff > 1 ? " روز" : " روز");
    },
  },
  fill: {
    type: "gradient",
    gradient: {
      shade: "light",
      type: "vertical",
      shadeIntensity: 0.25,
      gradientToColors: undefined,
      inverseColors: true,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [50, 0, 100, 100],
    },
  },

  colors: ["#282632", getLocalStorageItem("color-primary", "#0F626A")],
  xaxis: {
    type: "datetime",
    labels: {
      rotate: -30,
      rotateAlways: true,
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
  legend: {
    position: "top",
  },
  responsive: [
    {
      breakpoint: 768,
      options: {
        chart: {
          height: 280,
        },
        yaxis: {
          show: false,
        },
      },
    },
  ],

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

const timeline3Chart = new ApexCharts(
  document.querySelector("#timeline3"),
  timeline3ChartOptions
);
timeline3Chart.render();

// Advanced Timeline (Multiple range) //

const timeline4ChartOptions = {
  series: [
    {
      name: "باب",
      data: [
        {
          x: "طراحی",
          y: [
            new Date("1399-03-05").getTime(),
            new Date("1399-03-08").getTime(),
          ],
        },
        {
          x: "کد",
          y: [
            new Date("1399-03-02").getTime(),
            new Date("1399-03-05").getTime(),
          ],
        },
        {
          x: "کد",
          y: [
            new Date("1399-03-05").getTime(),
            new Date("1399-03-07").getTime(),
          ],
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-03").getTime(),
            new Date("1399-03-09").getTime(),
          ],
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-08").getTime(),
            new Date("1399-03-11").getTime(),
          ],
        },
        {
          x: "اعتبارسنجی",
          y: [
            new Date("1399-03-11").getTime(),
            new Date("1399-03-16").getTime(),
          ],
        },
        {
          x: "طراحی",
          y: [
            new Date("1399-03-01").getTime(),
            new Date("1399-03-03").getTime(),
          ],
        },
      ],
    },
    {
      name: "جو",
      data: [
        {
          x: "طراحی",
          y: [
            new Date("1399-03-02").getTime(),
            new Date("1399-03-05").getTime(),
          ],
        },
        {
          x: "تست",
          y: [
            new Date("1399-03-06").getTime(),
            new Date("1399-03-16").getTime(),
          ],
          goals: [
            {
              name: "Break",
              value: new Date("1399-03-10").getTime(),
              strokeColor: "#CD2F2A",
            },
          ],
        },
        {
          x: "کد",
          y: [
            new Date("1399-03-03").getTime(),
            new Date("1399-03-07").getTime(),
          ],
        },
        {
          x: "پیاده سازی",
          y: [
            new Date("1399-03-20").getTime(),
            new Date("1399-03-22").getTime(),
          ],
        },
        {
          x: "طراحی",
          y: [
            new Date("1399-03-10").getTime(),
            new Date("1399-03-16").getTime(),
          ],
        },
      ],
    },
    {
      name: "دنیل",
      data: [
        {
          x: "کد",
          y: [
            new Date("1399-03-10").getTime(),
            new Date("1399-03-17").getTime(),
          ],
        },
        {
          x: "اعتبارسنجی",
          y: [
            new Date("1399-03-05").getTime(),
            new Date("1399-03-09").getTime(),
          ],
          goals: [
            {
              name: "Break",
              value: new Date("1399-03-07").getTime(),
              strokeColor: "#CD2F2A",
            },
          ],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 450,
    type: "rangeBar",
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: "80%",
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
  xaxis: {
    type: "datetime",
    labels: {
      rotate: -30,
      rotateAlways: true,
      style: {
        colors: [],
        fontSize: "14px",
        fontFamily: "Vazirmatn FD,Rubik, serif",
        fontWeight: 500,
      },
    },
  },
  colors: ["#282632", getLocalStorageItem("color-primary", "#0F626A")],
  stroke: {
    width: 1,
  },
  fill: {
    type: "solid",
    opacity: 0.6,
  },
  legend: {
    position: "top",
    horizontalAlign: "left",
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

const timeline4Chart = new ApexCharts(
  document.querySelector("#timeline4"),
  timeline4ChartOptions
);
timeline4Chart.render();

// Timeline_range_chart 5
const timeline5ChartOptions = {
  series: [
    // George Washington
    {
      name: "جورج واشینگتن",
      data: [
        {
          x: "رئیس جمهور",
          y: [new Date(1389, 3, 30).getTime(), new Date(1399, 2, 4).getTime()],
        },
      ],
    },
    // John Adams
    {
      name: "جان آدامز",
      data: [
        {
          x: "رئیس جمهور",
          y: [new Date(1399, 2, 4).getTime(), new Date(1401, 2, 4).getTime()],
        },
        {
          x: "معاون وزیر",
          y: [new Date(1389, 3, 21).getTime(), new Date(1399, 2, 4).getTime()],
        },
      ],
    },
    // توماس جفرسون
    {
      name: "توماس جفرسون",
      data: [
        {
          x: "رئیس جمهور",
          y: [new Date(1401, 2, 4).getTime(), new Date(1403, 2, 4).getTime()],
        },
        {
          x: "معاون وزیر",
          y: [new Date(1399, 2, 4).getTime(), new Date(1401, 2, 4).getTime()],
        },
        {
          x: "وزیر کشور",
          y: [
            new Date(1380, 2, 22).getTime(),
            new Date(1383, 11, 31).getTime(),
          ],
        },
      ],
    },
    // Aaron Burr
    {
      name: "آرون بور",
      data: [
        {
          x: "معاون وزیر",
          y: [new Date(1401, 2, 4).getTime(), new Date(1405, 2, 4).getTime()],
        },
      ],
    },
    // George Clinton
    {
      name: "بیل کلینتون",
      data: [
        {
          x: "معاون وزیر",
          y: [new Date(1405, 2, 4).getTime(), new Date(1412, 3, 20).getTime()],
        },
      ],
    },
    // John Jay
    {
      name: "جان جی",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1389, 8, 25).getTime(), new Date(1380, 2, 22).getTime()],
        },
      ],
    },
    // Edmund Randolph
    {
      name: "ادموند راندولف",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1389, 0, 2).getTime(), new Date(1395, 7, 20).getTime()],
        },
      ],
    },
    // Timothy Pickering
    {
      name: "تیموتی پیکرینگ",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1395, 7, 20).getTime(), new Date(1400, 4, 12).getTime()],
        },
      ],
    },
    // Charles Lee
    {
      name: "چارلز لی",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1400, 4, 13).getTime(), new Date(1400, 5, 5).getTime()],
        },
      ],
    },
    // John Marshall
    {
      name: "جان مارشال",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1400, 5, 13).getTime(), new Date(1401, 2, 4).getTime()],
        },
      ],
    },
    // Levi Lincoln
    {
      name: "لوی لینکلن",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1401, 2, 5).getTime(), new Date(1401, 4, 1).getTime()],
        },
      ],
    },
    // James Madison
    {
      name: "جیمز مدیسون",
      data: [
        {
          x: "وزیر کشور",
          y: [new Date(1401, 4, 2).getTime(), new Date(1403, 2, 3).getTime()],
        },
      ],
    },
  ],
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "rangeBar",
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: "50%",
      rangeBarGroupRows: true,
    },
  },
  colors: [
    getLocalStorageItem("color-primary", "#106068"),
    getLocalStorageItem("color-secondary", "#606060"),
    "#0bb462",
    "#db4d58",
    "#f2bc23",
    "#535AE7",
    "#E5E3E0",
    "#48443D",
  ],
  fill: {
    type: "solid",
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
  xaxis: {
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

  legend: {
    position: "right",
  },
  responsive: [
    {
      breakpoint: 768,
      options: {
        chart: {
          height: 280,
        },
        yaxis: {
          show: false,
        },
        legend: {
          show: false,
        },
      },
    },
  ],
};

const timeline5Chart = new ApexCharts(
  document.querySelector("#timeline5"),
  timeline5ChartOptions
);
timeline5Chart.render();
