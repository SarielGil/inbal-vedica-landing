(function () {
  "use strict";

  var PROD_HOSTS = {
    "vedica-ayurveda.co.il": true,
    "www.vedica-ayurveda.co.il": true
  };

  var hostname = window.location && window.location.hostname ? window.location.hostname : "";
  if (!PROD_HOSTS[hostname]) return;

  var fontsHref =
    "https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&family=Heebo:wght@500;700;800&display=swap";
  if (!document.querySelector('link[data-site-fonts="google"]')) {
    var fontsLink = document.createElement("link");
    fontsLink.rel = "stylesheet";
    fontsLink.href = fontsHref;
    fontsLink.setAttribute("data-site-fonts", "google");
    document.head.appendChild(fontsLink);
  }

  var dnt =
    navigator.doNotTrack === "1" ||
    window.doNotTrack === "1" ||
    navigator.msDoNotTrack === "1";
  var gpc = navigator.globalPrivacyControl === true;
  var ua = navigator.userAgent || "";
  var automated =
    navigator.webdriver === true ||
    /HeadlessChrome|Lighthouse|PageSpeed|GTmetrix|Pingdom|Chrome-Lighthouse/i.test(ua);

  if (dnt || gpc || automated) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag =
    window.gtag ||
    function () {
      window.dataLayer.push(arguments);
    };

  window.gtag("js", new Date());
  window.gtag("config", "G-MXKKRFNL56");

  if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
    var gaScript = document.createElement("script");
    gaScript.async = true;
    gaScript.src = "https://www.googletagmanager.com/gtag/js?id=G-MXKKRFNL56";
    document.head.appendChild(gaScript);
  }

  if (!document.querySelector('script[src*="googletagmanager.com/gtm.js"]')) {
    var gtmScript = document.createElement("script");
    gtmScript.async = true;
    gtmScript.src = "https://www.googletagmanager.com/gtm.js?id=GTM-WZKF36P7";
    document.head.appendChild(gtmScript);
  }
})();
