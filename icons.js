/* Shared weather icon set: used by the app and by legend.html, so the legend
   can never drift away from what the screen actually shows. */
var WH = (function () {
  "use strict";

  var CLOUD = '<g fill="#c9d4e2"><circle cx="25" cy="37" r="12"/>' +
    '<circle cx="43" cy="32" r="14"/>' +
    '<rect x="18" y="37" width="33" height="13" rx="6.5"/></g>';
  var SUN_SMALL = '<g stroke="#ffb020" stroke-width="4" stroke-linecap="round">' +
    '<path d="M24 9V4M24 39v5M9 22H4M39 22h5M34.6 11.4l3-3M13.4 32.6l-3 3' +
    'M34.6 32.6l3 3M13.4 11.4l-3-3"/></g>' +
    '<circle cx="24" cy="22" r="9" fill="#ffb020"/>';
  var DROPS = '<g stroke="#4aa3ff" stroke-width="4" stroke-linecap="round">' +
    '<path d="M22 52l-2 7M32 52l-2 7M42 52l-2 7"/></g>';
  var DRIZZLE = '<g stroke="#4aa3ff" stroke-width="3.5" stroke-linecap="round">' +
    '<path d="M26 52l-1 6M38 52l-1 6"/></g>';
  var FLAKES = '<g stroke="#b8d9ff" stroke-width="3" stroke-linecap="round">' +
    '<path d="M22 50v8M19 52l6 4M25 52l-6 4M42 50v8M39 52l6 4M45 52l-6 4"/></g>';
  var FOG = '<g fill="#c9d4e2"><circle cx="27" cy="30" r="11"/>' +
    '<circle cx="43" cy="26" r="12"/>' +
    '<rect x="20" y="30" width="30" height="11" rx="5.5"/></g>' +
    '<g stroke="#93a0b2" stroke-width="4" stroke-linecap="round">' +
    '<path d="M18 48h28M24 56h22"/></g>';
  var BOLT = '<polygon points="34,44 24,57 31,57 28,63 41,50 34,50" fill="#ffd24a"/>';
  /* Night has to look different at a glance: a moon, never a sun, otherwise
     the 23:00 icon reads like noon. */
  var MOON = '<circle cx="32" cy="30" r="16" fill="#dbe6f5"/>' +
    '<g fill="#b9c6d8"><circle cx="26" cy="24" r="3"/>' +
    '<circle cx="37" cy="35" r="4"/><circle cx="27" cy="37" r="2"/></g>' +
    '<g fill="#ffd24a"><path d="M51 12l1.6 3.4L56 17l-3.4 1.6L51 22l-1.6-3.4L46 17l3.4-1.6z"/>' +
    '<path d="M15 39l1.2 2.6 2.6 1.2-2.6 1.2L15 47l-1.2-2.6L11 43l2.6-1.2z"/></g>';
  var MOON_SMALL = '<circle cx="22" cy="20" r="10" fill="#dbe6f5"/>' +
    '<g fill="#b9c6d8"><circle cx="19" cy="17" r="2"/>' +
    '<circle cx="25" cy="23" r="2.4"/></g>';

  var ICONS = {
    sun: '<g stroke="#ffb020" stroke-width="5" stroke-linecap="round">' +
      '<path d="M32 14V6M32 50v8M14 32H6M50 32h8M45.5 18.5L50 14M18.5 45.5L14 50' +
      'M45.5 45.5L50 50M18.5 18.5L14 14"/></g>' +
      '<circle cx="32" cy="32" r="12" fill="#ffb020"/>',
    cloud: CLOUD,
    suncloud: SUN_SMALL + CLOUD,
    fog: FOG,
    drizzle: CLOUD + DRIZZLE,
    rain: CLOUD + DROPS,
    showers: SUN_SMALL + CLOUD + DROPS,
    snow: CLOUD + FLAKES,
    snowshowers: SUN_SMALL + CLOUD + FLAKES,
    thunder: CLOUD + BOLT,
    moon: MOON,
    mooncloud: MOON_SMALL + CLOUD,
    moonshowers: MOON_SMALL + CLOUD + DROPS,
    moonsnowshowers: MOON_SMALL + CLOUD + FLAKES
  };

  var NAMES = {
    sun: { hr: "Vedro", en: "Clear" },
    suncloud: { hr: "Prete\u017eno vedro / djelomi\u010dno obla\u010dno", en: "Mainly clear / partly cloudy" },
    cloud: { hr: "Obla\u010dno", en: "Overcast" },
    fog: { hr: "Magla", en: "Fog" },
    drizzle: { hr: "Rosulja", en: "Drizzle" },
    rain: { hr: "Ki\u0161a", en: "Rain" },
    showers: { hr: "Pljuskovi", en: "Showers" },
    snow: { hr: "Snijeg", en: "Snow" },
    snowshowers: { hr: "Snje\u017eni pljuskovi", en: "Snow showers" },
    thunder: { hr: "Grmljavina", en: "Thunderstorm" },
    moon: { hr: "Vedro (no\u0107)", en: "Clear (night)" },
    mooncloud: { hr: "Djelomi\u010dno obla\u010dno (no\u0107)", en: "Partly cloudy (night)" },
    moonshowers: { hr: "No\u0107ni pljuskovi", en: "Night showers" },
    moonsnowshowers: { hr: "No\u0107ni snje\u017eni pljuskovi", en: "Night snow showers" }
  };

  return {
    icons: ICONS,
    names: NAMES,
    order: ["sun", "suncloud", "cloud", "fog", "drizzle", "rain",
            "showers", "snow", "snowshowers", "thunder",
            "moon", "mooncloud", "moonshowers", "moonsnowshowers"],
    svg: function (name) {
      return '<svg class="ic" viewBox="0 0 64 64">' +
             (ICONS[name] || ICONS.cloud) + "</svg>";
    }
  };
}());
