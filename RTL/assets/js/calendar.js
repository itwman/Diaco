// **------calendar js**

document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    noEventsContent: "رویدادی برای این تاریخ وجود ندارد!",
    direction: "rtl",
    locale: "fa",
    allDayText: "تمام روز",
    buttonText: {
      today: "امروز",
      month: "ماه",
      week: "هفته",
      day: "روز",
      list: "لیست",
    },
    navLinks: true,
    editable: true,
    dayMaxEvents: true,
    headerToolbar: {
      left: "prev,next,addEventButton",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
    },
    moreLinkContent: function (args) {
      return "+" + args.num + " مورد دیگر";
    },
    customButtons: {
      addEventButton: {
        text: "رویداد جدید...",
        click: function () {
          const dateStr = prompt("فرمت تاریخ به صورت YYYY-MM-DD وارد کنید");
          const date = new Date(dateStr + "T00:00:00");

          if (!isNaN(date.valueOf())) {
            calendar.addEvent({
              title: "رویداد پویا",
              start: date,
              allDay: true,
            });
            alert("بسیار خوب ، اکنون دیتابیس را بروزرسانی کنید...");
          } else {
            alert("تاریخ نامعتبر.");
          }
        },
      },
    },
    events: [
      {
        title: "تعطیلات",
        start: "2024-07-01",
        end: "2024-07-02",
        color: "#26C450",
        className: "event-success",
      },
      {
        title: "میتینگ",
        start: "2024-07-09",
        className: "event-primary",
      },
      {
        title: "میتینگ",
        start: "2024-07-15",
        className: "event-primary",
      },
      {
        title: "تور",
        start: "2024-07-18",
        end: "2024-07-21",
        className: "event-warning",
      },
      {
        title: "ناهار",
        start: "2024-07-30",
        end: "2024-07-31",
        color: "#F09E3C",
        className: "event-secondary",
      },
      {
        title: "میتینگ",
        start: "2024-07-12T10:30:00",
        end: "2024-07-12T12:30:00",
      },
      {
        title: "ناهار",
        start: "2024-07-12T12:00:00",
      },
      {
        title: "میتینگ",
        start: "2024-07-12T14:30:00",
      },
      {
        title: "استراحت",
        start: "2024-07-12T17:30:00",
      },
      {
        title: "شام",
        start: "2024-07-12T20:00:00",
      },
      {
        groupId: "availableForMeeting",
        start: "2024-07-11T10:00:00",
        end: "2024-07-11T16:00:00",
        display: "background",
      },
      {
        groupId: "availableForMeeting",
        start: "2024-07-13T10:00:00",
        end: "2024-07-13T16:00:00",
        display: "background",
      },
    ],
    eventClick: function () {
      $("#exampleModal").modal("show");
    },
    selectable: true,
    selectMirror: true,
    select: function (arg) {
      const title = prompt("عنوان رویداد:");
      if (title) {
        calendar.addEvent({
          title: title,
          start: arg.start,
          end: arg.end,
          allDay: arg.allDay,
        });
      }
      calendar.unselect();
    },

    droppable: true,
    drop: function (arg) {
      if (document.getElementById("drop-remove").checked) {
        arg.draggedEl.parentNode.removeChild(arg.draggedEl);
      }
    },
  });

  const containerEl = document.getElementById("events-list");
  new FullCalendar.Draggable(containerEl, {
    itemSelector: ".list-event",
    eventData: function (eventEl) {
      return {
        title: eventEl.innerText.trim(),
        start: new Date(),
        className: eventEl.getAttribute("data-class"),
      };
    },
  });

  calendar.render();
});

// **------slider js**

$(".slider").slick({
  dots: false,
  speed: 1000,
  slidesToShow: 3,
  centerMode: true,
  arrows: false,
  vertical: true,
  verticalSwiping: true,
  focusOnSelect: true,
  autoplay: true,
  autoplaySpeed: 1000,
});
