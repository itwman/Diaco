// treemap_chart 1
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

const treemap1Options = {
  series: [
    {
      data: [
        {
          x: "مشهد",
          y: 218,
        },
        {
          x: "تهران",
          y: 149,
        },
        {
          x: "شیراز",
          y: 184,
        },
        {
          x: "اصفهان",
          y: 55,
        },
        {
          x: "آبادان",
          y: 84,
        },
        {
          x: "کرج",
          y: 31,
        },
        {
          x: "قزوین",
          y: 70,
        },
        {
          x: "رشت",
          y: 30,
        },
        {
          x: "ساری",
          y: 44,
        },
        {
          x: "زابل",
          y: 68,
        },
        {
          x: "زاهدان",
          y: 28,
        },
        {
          x: "کرمانشاه",
          y: 19,
        },
        {
          x: "کرمان",
          y: 29,
        },
      ],
    },
  ],
  legend: {
    show: false,
  },
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "treemap",
  },

  colors: [getLocalStorageItem("color-primary", "#0F626A")],
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

const treemap1Chart = new ApexCharts(
  document.querySelector("#treemap1"),
  treemap1Options
);
treemap1Chart.render();

// treemap_chart 2

const treemap2Options = {
  series: [
    {
      name: "رومیزی",
      data: [
        {
          x: "آ ب ث",
          y: 10,
        },
        {
          x: "د ذ ر",
          y: 60,
        },
        {
          x: "پ ه ع",
          y: 41,
        },
      ],
    },
    {
      name: "موبایل",
      data: [
        {
          x: "ش ط ب",
          y: 10,
        },
        {
          x: "ف ق ب",
          y: 20,
        },
        {
          x: "ح خ ه",
          y: 51,
        },
        {
          x: "م ن ت",
          y: 30,
        },
        {
          x: "ا ل ب",
          y: 20,
        },
        {
          x: "ی س ش",
          y: 30,
        },
      ],
    },
  ],
  legend: {
    show: false,
  },
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "treemap",
  },

  colors: [getLocalStorageItem("color-secondary", "#626262"), "#0AB964"],

  title: {
    text: "",
    align: "center",
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

const treemap2Chart = new ApexCharts(
  document.querySelector("#treemap2"),
  treemap2Options
);
treemap2Chart.render();

// treemap_chart 3

const treemap3Options = {
  series: [
    {
      data: [
        {
          x: "مشهد",
          y: 218,
        },
        {
          x: "تهران",
          y: 149,
        },
        {
          x: "شیراز",
          y: 184,
        },
        {
          x: "اصفهان",
          y: 55,
        },
        {
          x: "آبادان",
          y: 84,
        },
        {
          x: "کرج",
          y: 31,
        },
        {
          x: "قزوین",
          y: 70,
        },
        {
          x: "رشت",
          y: 30,
        },
        {
          x: "ساری",
          y: 44,
        },
        {
          x: "زابل",
          y: 68,
        },
        {
          x: "زاهدان",
          y: 28,
        },
        {
          x: "کرمانشاه",
          y: 19,
        },
        {
          x: "کرمان",
          y: 29,
        },
      ],
    },
  ],
  legend: {
    show: false,
  },
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "treemap",
  },
  title: {
    text: "",
    align: "center",
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
  plotOptions: {
    treemap: {
      distributed: true,
      enableShades: false,
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

const treemap3Chart = new ApexCharts(
  document.querySelector("#treemap3"),
  treemap3Options
);
treemap3Chart.render();

// treemap_chart 4

const treemap4Options = {
  series: [
    {
      data: [
        {
          x: "اینترنت",
          y: 1.2,
        },
        {
          x: "ه ع",
          y: 0.4,
        },
        {
          x: "غ ف ق",
          y: -1.4,
        },
        {
          x: "ث ص ض",
          y: 2.7,
        },
        {
          x: "پ چ جT",
          y: -0.3,
        },
        {
          x: "ف ق ",
          y: 5.1,
        },
        {
          x: "ی ب",
          y: -2.3,
        },
        {
          x: "ل ا ت",
          y: 2.1,
        },
        {
          x: "ن م ",
          y: 0.3,
        },
        {
          x: "گ ک",
          y: 0.12,
        },
        {
          x: "و د ذ",
          y: -2.31,
        },
        {
          x: "ر ز ط",
          y: 3.98,
        },
        {
          x: "ظ ش ی",
          y: 1.67,
        },
      ],
    },
  ],
  legend: {
    show: false,
  },
  chart: {
    fontFamily: "Vazirmatn FD,Rubik, serif",
    height: 350,
    type: "treemap",
  },
  title: {
    text: "",
  },
  dataLabels: {
    enabled: true,
    style: {
      fontSize: "12px",
      fontFamily: "Vazirmatn FD,Rubik, serif",
    },
    formatter: function (text, op) {
      return [text, op.value];
    },
    offsetY: -4,
  },
  plotOptions: {
    treemap: {
      enableShades: true,
      shadeIntensity: 0.5,
      reverseNegativeShade: true,
      colorScale: {
        ranges: [
          {
            from: -6,
            to: 0,
            color: "#282632",
          },
          {
            from: 0.001,
            to: 6,
            color: getLocalStorageItem("color-primary", "#0F626A"),
          },
        ],
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

const treemap4Chart = new ApexCharts(
  document.querySelector("#treemap4"),
  treemap4Options
);
treemap4Chart.render();
