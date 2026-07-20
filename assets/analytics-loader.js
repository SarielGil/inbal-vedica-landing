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

  function detectLlmReferrer(referrer) {
    if (!referrer) return null;

    try {
      var url = new URL(referrer);
      var host = url.hostname.replace(/^www\./, "").toLowerCase();
      var path = url.pathname.toLowerCase();
      var sourceByHost = {
        "chatgpt.com": "chatgpt",
        "chat.openai.com": "chatgpt",
        "perplexity.ai": "perplexity",
        "claude.ai": "claude",
        "gemini.google.com": "gemini",
        "bard.google.com": "gemini",
        "copilot.microsoft.com": "copilot",
        "poe.com": "poe",
        "you.com": "you",
        "phind.com": "phind",
        "chat.mistral.ai": "mistral",
        "lechat.mistral.ai": "mistral",
        "meta.ai": "meta_ai",
        "chat.deepseek.com": "deepseek",
        "grok.com": "grok"
      };

      if (sourceByHost[host]) {
        return {
          host: host,
          source: sourceByHost[host]
        };
      }

      if ((host === "bing.com" || host === "microsoft.com") && /\/(chat|copilot)/.test(path)) {
        return {
          host: host,
          source: "copilot"
        };
      }
    } catch (e) {
      return null;
    }

    return null;
  }

  var llmReferrer = detectLlmReferrer(document.referrer);
  if (llmReferrer) {
    window.gtag("event", "llm_referral_visit", {
      llm_source: llmReferrer.source,
      llm_referrer_host: llmReferrer.host,
      transport_type: "beacon"
    });
  }

  function cleanText(value) {
    return (value || "").replace(/\s+/g, " ").trim().slice(0, 120);
  }

  function getPath(url) {
    try {
      return new URL(url, window.location.href).pathname;
    } catch (e) {
      return "";
    }
  }

  function getCtaLocation(link) {
    var explicitLocation = link.getAttribute("data-cta-location");
    if (explicitLocation) return cleanText(explicitLocation);

    var section = link.closest("section, article, header, footer, nav");
    if (!section) return link.id || "unknown";
    if (section.id) return section.id;
    if (section.getAttribute("aria-label")) return cleanText(section.getAttribute("aria-label"));
    var heading = section.querySelector("h1, h2, h3");
    if (heading) return cleanText(heading.textContent);
    return cleanText(section.className) || link.id || "unknown";
  }

  function baseClickParams(link, eventType) {
    return {
      event_category: eventType === "lead" ? "lead" : "engagement",
      link_url: link.href,
      link_text: cleanText(link.textContent),
      link_id: link.id || "",
      cta_location: getCtaLocation(link),
      lead_page: window.location.pathname || "/",
      transport_type: "beacon"
    };
  }

  function trackLead(method, link) {
    var params = baseClickParams(link, "lead");
    params.lead_method = method;

    window.gtag("event", method + "_click", params);
    window.gtag("event", "generate_lead", params);
  }

  function trackEngagement(eventName, link, extraParams) {
    var params = baseClickParams(link, "engagement");
    Object.keys(extraParams || {}).forEach(function (key) {
      params[key] = extraParams[key];
    });
    window.gtag("event", eventName, params);
  }

  function trackSectionView(section) {
    var eventName = section.getAttribute("data-analytics-view-event");
    if (!eventName) return;

    window.gtag("event", eventName, {
      event_category: "engagement",
      cta_location: cleanText(section.getAttribute("data-cta-location") || section.id || "unknown"),
      transport_type: "beacon"
    });
  }

  var trackedSections = document.querySelectorAll("[data-analytics-view-event]");
  if (trackedSections.length) {
    if ("IntersectionObserver" in window) {
      var sectionObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting || entry.intersectionRatio < 0.25) return;
          trackSectionView(entry.target);
          sectionObserver.unobserve(entry.target);
        });
      }, {
        threshold: [0.25]
      });

      trackedSections.forEach(function (section) {
        sectionObserver.observe(section);
      });
    } else {
      trackedSections.forEach(trackSectionView);
    }
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a[href]");
    if (!link) return;

    var href = link.getAttribute("href") || "";
    var lowerHref = href.toLowerCase();
    var linkHost = "";
    try {
      linkHost = new URL(link.href).hostname.replace(/^www\./, "").toLowerCase();
    } catch (e) {
      linkHost = "";
    }

    var explicitEventName = link.getAttribute("data-analytics-event");
    if (explicitEventName) {
      trackEngagement(cleanText(explicitEventName), link);
    }

    if (lowerHref.indexOf("wa.me/") !== -1 || lowerHref.indexOf("whatsapp") !== -1) {
      trackLead("whatsapp", link);
      return;
    }

    if (lowerHref.indexOf("tel:") === 0) {
      trackLead("phone", link);
      return;
    }

    if (lowerHref.indexOf("mailto:") === 0) {
      trackLead("email", link);
      return;
    }

    if (getPath(link.href) === "/contact.html") {
      trackEngagement("contact_click", link, {
        contact_target: "contact_page"
      });
      return;
    }

    if (linkHost === "infomed.co.il") {
      trackEngagement("review_click", link, {
        review_source: "infomed"
      });
      return;
    }

    if (
      linkHost === "google.com" ||
      linkHost === "maps.google.com" ||
      linkHost === "waze.com" ||
      linkHost === "ul.waze.com"
    ) {
      trackEngagement("map_click", link, {
        map_source: linkHost
      });
    }
  }, true);

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
