// Basic Typeahead
const stringMatcher = (strs) => {
  return function findMatches(word, wd) {
    const strmatches = [];
    const substrRegex = new RegExp(word, "i");
    strs.forEach((str) => {
      if (substrRegex.test(str)) {
        strmatches.push(str);
      }
    });
    wd(strmatches);
  };
};

const states = [
  "آذربایجان شرقی",
  "آذربایجان غربی",
  "اردبیل",
  "اصفهان",
  "البرز",
  "ایلام",
  "بوشهر",
  "تهران",
  "چهارمحال و بختیاری",
  "خراسان جنوبی",
  "خراسان رضوی",
  "خراسان شمالی",
  "خوزستان",
  "زنجان",
  "سمنان",
  "سیستان و بلوچستان",
  "فارس",
  "قزوین",
  "قم",
  "کردستان",
  "کرمان",
  "کهگیلویه و بویراحمد",
  "گلستان",
  "گیلان",
  "لرستان",
  "مازندران",
  "مرکزی",
  "هرمزگان",
  "همدان",
  "یزد",
];

$("#basictype .typeahead").typeahead(
  {
    hint: true,
    highlight: true,
    minLength: 1,
    rtl: true,
  },
  {
    name: "states",
    source: stringMatcher(states),
  }
);

// Bloodhoundtype Typeahead
const bloodhoundStates = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  local: states,
});

$("#bloodhoundtype .typeahead").typeahead(
  {
    hint: true,
    highlight: false,
    minLength: 1,
    rtl: true,
  },
  {
    name: "states",
    source: bloodhoundStates,
  }
);

// Prefetchtype Typeahead
const countries = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: "assets/vendor/typeahead/data/countries.json",
});

$("#prefetchtype .typeahead").typeahead(
  {
    hint: true,
    highlight: false,
    minLength: 1,
    rtl: true,
  },
  {
    name: "states",
    source: countries,
  }
);

// Remotetype Typeahead
const bestPictures = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace("value"),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: "assets/vendor/typeahead/data/post_1960.json",
});

$("#remotetype .typeahead").typeahead(null, {
  name: "best-pictures",
  display: "value",
  source: bestPictures,
});

// Custom Templates
$("#customtype-templates .typeahead").typeahead(null, {
  name: "best-pictures",
  display: "value",
  source: bestPictures,
  templates: {
    empty: [
      '<div class="empty-message">',
      '<i class="ti ti-mood-sad"></i> داده ای یافت نشد',
      "</div>",
    ].join("\n"),
  },
});

// multiple-datasets
const nbaTeams = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace("team"),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: "assets/vendor/typeahead/data/nba.json",
});

const nhlTeams = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace("team"),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: "assets/vendor/typeahead/data/nhl.json",
});

// multiple-datasets
$("#multiple-datasetstype .typeahead").typeahead(
  null,
  {
    name: "nba-teams",
    display: "team",
    source: nbaTeams,
    templates: {
      header: '<h5 class="league-name">تیم های NBA</h5>',
    },
  },
  {
    name: "nhl-teams",
    display: "team",
    source: nhlTeams,
    templates: {
      header: '<h5 class="league-name">تیم های NHL</h5>',
    },
  }
);

// scrollable-dropdown-menu
$("#scrollable-dropdown-menu .typeahead").typeahead(null, {
  name: "countries",
  limit: 10,
  source: countries,
});

// rtltype Typeahead
const arabicPhrases = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  local: states,
});

$("#rtltype .typeahead").typeahead(
  {
    hint: false,
  },
  {
    name: "arabic-phrases",
    source: arabicPhrases,
  }
);
