// ---------basic tree start---- //
$("#theme_tree").jstree({
  core: {
    rtl: true,
    themes: {
      variant: "large",
      rtl: true,
    },
    data: [
      {
        text: "کای-ادمین",
        icon: "fa fa-folder text-warning",
        state: {
          selected: false,
        },
        type: "demo",
        children: [
          {
            text: "استس",
            icon: "fa fa-folder text-warning",
            state: {
              selected: true,
            },
            // "li_attr": {
            //     "class": "li-style"
            // },
            // "a_attr": {
            //     "class": "a-style"
            // }
            children: [
              {
                text: "سی اس اس",
                icon: "fa fa-folder text-warning",

                state: {
                  selected: true,
                },
              },
              {
                text: "فونت ها",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "آیکن ها",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "تصاویر",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "جی اس",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "اس سی اس اس",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "وندور",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
            ],
          },
          {
            text: "ماژول ها",
            icon: "fa fa-folder text-warning",
            state: {
              selected: true,
            },
          },
          {
            text: "قالب ها",
            icon: "fa fa-folder text-warning",
            state: {
              selected: true,
            },
            children: [
              {
                text: "ایندکس.html",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "اکوردیون.html",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "انیمیشن.html",
                icon: "fa fa-folder text-warning ",
                state: {
                  selected: true,
                },
              },
              {
                text: "تقویم.html",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
              {
                text: "کلیپبورد.html",
                icon: "fa fa-folder text-warning",
                state: {
                  selected: true,
                },
              },
            ],
          },
          {
            text: "گالپ",
            icon: "fa  fa-file text-light",
            state: {
              selected: true,
            },
          },
          {
            text: "پکیج.json",
            icon: "fa  fa-file text-light",
            state: {
              selected: true,
            },
          },
          {
            text: "پکیج.json",
            icon: "fa  fa-file text-light",
            state: {
              selected: true,
            },
          },
        ],
      }, // root node end, end of JSON
    ],
  },
});
// -----end basic tree-------- //

// -----tree with checkbox start------ //
$("#level_tree").jstree({
  core: {
    rtl: true,
    themes: {
      variant: "large",
      rtl: true,
    },
    data: [
      {
        text: "کای-ادمین",
        icon: "ti ti-category",
        state: {
          selected: false,
        },
        type: "demo",
        children: [
          {
            text: "داشبورد",
            icon: "ti ti-home-heart",
            state: {
              selected: true,
            },
            children: [
              {
                text: "فروشگاهی",
                icon: "ti ti-circle text-primary",

                state: {
                  selected: true,
                },
              },
              {
                text: "پروژه",
                icon: "fa ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "تحلیل",
                icon: "fa ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "آموزش",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
            ],
          },
          {
            text: "برنامه ها",
            icon: "ti ti-server-2 ",
            state: {
              selected: true,
            },
            children: [
              {
                text: "تقویم",
                icon: "ti ti-circle text-primary",

                state: {
                  selected: true,
                },
              },
              {
                text: "فاکتور",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "کان بان",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "پروفایل",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "تایم لاین",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "سوالات متداول",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
            ],
          },
          {
            text: "کیت های یو آی",
            icon: "ti ti-lock-open ",
            state: {
              selected: true,
            },
            children: [
              {
                text: "برگه تقلب",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "هشدار",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "نشان ها",
                icon: "ti ti-circle text-primary ",
                state: {
                  selected: true,
                },
              },
              {
                text: "دکمه ها",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
              {
                text: "کارت ها",
                icon: "ti ti-circle text-primary",
                state: {
                  selected: true,
                },
              },
            ],
          },
        ],
      }, // root node end, end of JSON
    ],
  },

  plugins: ["themes", "html_data", "checkbox", "sort", "ui"],
});
// -------tree with checkbox end------ //
