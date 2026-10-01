(function () {
  var nav = document.querySelector(".nav");
  var scroller = document.querySelector(".page");
  var toggle = document.querySelector("[data-nav-toggle]");
  var links = document.querySelector("[data-nav-links]");

  var sectionLinks = Array.prototype.slice.call(document.querySelectorAll(".nav-links a[href^='#']"));

  function markNav() {
    if (!scroller || !sectionLinks.length) return;
    var frame = scroller.getBoundingClientRect();
    var current = sectionLinks[0];
    sectionLinks.forEach(function (link) {
      var id = (link.getAttribute("href") || "").replace("#", "");
      var section = id ? document.getElementById(id) : null;
      if (!section) return;
      if (section.getBoundingClientRect().top - frame.top <= 140) current = link;
    });
    sectionLinks.forEach(function (link) {
      var on = link === current;
      link.classList.toggle("active", on);
      if (on) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  }

  function onScroll() {
    if (!nav || !scroller) return;
    nav.classList.toggle("is-scrolled", scroller.scrollTop > 8);
    markNav();
  }

  onScroll();
  if (scroller) scroller.addEventListener("scroll", onScroll, { passive: true });

  function setMenu(open) {
    if (!links || !toggle) return;
    links.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? toggle.dataset.closeLabel : toggle.dataset.openLabel);
  }

  var searchToggle = document.querySelector("[data-search-toggle]");
  var searchForm = document.querySelector("[data-search-form]");
  var searchInput = document.querySelector("[data-search-input]");

  function setSearch(open) {
    if (!searchToggle || !searchForm || !searchInput) return;
    searchForm.hidden = !open;
    searchToggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) searchInput.focus();
  }

  if (searchToggle && searchForm && searchInput) {
    searchToggle.addEventListener("click", function () {
      setSearch(searchForm.hidden);
    });
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var query = searchInput.value.trim().toLowerCase();
      if (!query || !scroller) return;
      var nodes = scroller.querySelectorAll("h1, h2, h3, a, p");
      for (var i = 0; i < nodes.length; i += 1) {
        var text = (nodes[i].textContent || "").trim().toLowerCase();
        if (text && text.indexOf(query) !== -1) {
          nodes[i].scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
          setSearch(false);
          break;
        }
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setSearch(false);
    });
  }

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      setMenu(!links.classList.contains("is-open"));
    });
    links.addEventListener("click", function (event) {
      if (event.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setMenu(false);
    });
  }

  var quotes = Array.prototype.slice.call(document.querySelectorAll("[data-quote]"));
  var indexNode = document.querySelector("[data-quote-index]");
  var quoteIndex = 0;

  function showQuote(next) {
    if (!quotes.length) return;
    quoteIndex = (next + quotes.length) % quotes.length;
    quotes.forEach(function (node, index) {
      node.hidden = index !== quoteIndex;
    });
    if (indexNode) {
      indexNode.textContent = String(quoteIndex + 1).padStart(2, "0");
    }
  }

  var prev = document.querySelector("[data-quote-prev]");
  var next = document.querySelector("[data-quote-next]");
  if (prev) prev.addEventListener("click", function () { showQuote(quoteIndex - 1); });
  if (next) next.addEventListener("click", function () { showQuote(quoteIndex + 1); });

  var lineCaret = document.querySelector("[data-hero-caret]");
  var role = document.querySelector("[data-hero-role]");
  var roleCaret = document.querySelector("[data-hero-role-caret]");
  var roleLive = document.querySelector("[data-hero-role-live]");
  var headlineParts = [
    { node: document.querySelector("[data-hero-a]"), text: "من " },
    { node: document.querySelector("[data-hero-b]"), text: "محمد اسکندرلو" },
    { node: document.querySelector("[data-hero-c]"), text: " هستم" }
  ];
  var roles = [
    "یک برنامه‌نویس بک‌اند",
    "یک توسعه‌دهنده Python و Django",
    "یک سازنده راهکارهای هوش مصنوعی",
    "یک طراح اتوماتیک ساز کسب و کارها",
    "یک توسعه دهنده بردهای الکترونیکی"
  ];
  var timers = [];
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function later(fn, ms) {
    var id = setTimeout(fn, reduced ? 0 : ms);
    timers.push(id);
    return id;
  }

  function typeInto(node, text, speed, done) {
    var i = 0;
    function step() {
      node.textContent = text.slice(0, i);
      if (i < text.length) {
        i += 1;
        later(step, speed);
      } else if (done) {
        done();
      }
    }
    step();
  }

  function erase(node, speed, done) {
    function step() {
      var current = node.textContent || "";
      if (!current) {
        if (done) done();
        return;
      }
      node.textContent = current.slice(0, -1);
      later(step, speed);
    }
    step();
  }

  function cycle(index) {
    var word = roles[index % roles.length];
    typeInto(role, word, 72, function () {
        if (roleLive) roleLive.textContent = word;
      later(function () {
        erase(role, 42, function () {
          later(function () { cycle(index + 1); }, 260);
        });
      }, 1500);
    });
  }

  if (reduced) {
    document.querySelectorAll(".stage-beam").forEach(function (svg) {
      if (svg.pauseAnimations) svg.pauseAnimations();
    });
  }

  var floaters = Array.prototype.slice.call(document.querySelectorAll(".floater"));
  var frameEl = document.querySelector(".stage-frame");
  if (floaters.length && frameEl && !reduced) {
    function seed(index, total) {
      var box = frameEl.getBoundingClientRect();
      var side = index % 4;
      var slot = Math.floor(index / 4);
      var lanes = Math.ceil(total / 4);
      var u = (slot + 0.45) / lanes;
      var speed = 0.07 + (index % 5) * 0.012;
      if (side === 0) return { x: box.left + u * box.width, y: 8, vx: speed, vy: 0.04 };
      if (side === 1) return { x: window.innerWidth - 60, y: box.top + u * box.height, vx: -0.03, vy: speed };
      if (side === 2) return { x: box.right - u * box.width, y: window.innerHeight - 60, vx: -speed, vy: -0.03 };
      return { x: 8, y: box.bottom - u * box.height, vx: 0.04, vy: -speed };
    }
    var bodies = floaters.map(function (el, index) {
      var depth = Number(el.getAttribute("data-depth")) || 1;
      var start = seed(index, floaters.length);
      return {
        el: el,
        x: start.x,
        y: start.y,
        vx: start.vx * (0.75 + depth * 0.2),
        vy: start.vy * (0.75 + depth * 0.2),
        angle: index * 20,
        spin: (index % 2 ? 0.012 : -0.01),
        mass: 0.75 + depth * 0.35
      };
    });
    var mouse = { x: -9999, y: -9999, px: -9999, py: -9999, vx: 0, vy: 0 };

    window.addEventListener("mousemove", function (event) {
      mouse.x = event.clientX;
      mouse.y = event.clientY;
    }, { passive: true });

    function soften(speed) {
      return speed * -0.28;
    }

    function bounce(body) {
      var w = body.el.offsetWidth || 52;
      var h = body.el.offsetHeight || 52;
      var box = frameEl.getBoundingClientRect();
      var left = 6;
      var top = 6;
      var right = window.innerWidth - 6;
      var bottom = window.innerHeight - 6;
      if (body.x < left) {
        body.x += (left - body.x) * 0.18;
        if (body.vx < 0) body.vx = soften(body.vx);
      }
      if (body.y < top) {
        body.y += (top - body.y) * 0.18;
        if (body.vy < 0) body.vy = soften(body.vy);
      }
      if (body.x + w > right) {
        body.x += (right - w - body.x) * 0.18;
        if (body.vx > 0) body.vx = soften(body.vx);
      }
      if (body.y + h > bottom) {
        body.y += (bottom - h - body.y) * 0.18;
        if (body.vy > 0) body.vy = soften(body.vy);
      }

      var cx = body.x + w / 2;
      var cy = body.y + h / 2;
      var innerLeft = box.left + 14;
      var innerTop = box.top + 14;
      var innerRight = box.right - 14;
      var innerBottom = box.bottom - 14;
      if (cx > innerLeft && cx < innerRight && cy > innerTop && cy < innerBottom) {
        var dl = cx - innerLeft;
        var dr = innerRight - cx;
        var dt = cy - innerTop;
        var db = innerBottom - cy;
        var nearest = Math.min(dl, dr, dt, db);
        if (nearest === dl) {
          body.x -= dl * 0.22;
          if (body.vx > 0) body.vx = soften(body.vx);
        } else if (nearest === dr) {
          body.x += dr * 0.22;
          if (body.vx < 0) body.vx = soften(body.vx);
        } else if (nearest === dt) {
          body.y -= dt * 0.22;
          if (body.vy > 0) body.vy = soften(body.vy);
        } else {
          body.y += db * 0.22;
          if (body.vy < 0) body.vy = soften(body.vy);
        }
      }
    }

    function drift() {
      if (mouse.px > -9000) {
        mouse.vx = mouse.x - mouse.px;
        mouse.vy = mouse.y - mouse.py;
      }
      mouse.px = mouse.x;
      mouse.py = mouse.y;
      var speed = Math.hypot(mouse.vx, mouse.vy);

      bodies.forEach(function (body) {
        var rect = body.el.getBoundingClientRect();
        var cx = rect.left + rect.width / 2;
        var cy = rect.top + rect.height / 2;
        var dx = cx - mouse.x;
        var dy = cy - mouse.y;
        var dist = Math.hypot(dx, dy) || 1;
        var reach = 72;
        if (dist < reach && speed > 1.4) {
          var nx = dx / dist;
          var ny = dy / dist;
          var hit = (1 - dist / reach) * Math.min(speed, 14) * 0.22;
          body.vx += (nx * hit) / body.mass;
          body.vy += (ny * hit) / body.mass;
          body.spin += ((-ny * mouse.vx) + (nx * mouse.vy)) * 0.012;
        }

        body.vx *= 0.992;
        body.vy *= 0.992;
        var pace = Math.hypot(body.vx, body.vy);
        if (pace < 0.08) {
          body.vx += body.vx >= 0 ? 0.004 : -0.004;
          body.vy += body.vy >= 0 ? 0.003 : -0.003;
        }
        if (pace > 0.62) {
          body.vx *= 0.62 / pace;
          body.vy *= 0.62 / pace;
        }
        body.spin *= 0.996;
        body.x += body.vx;
        body.y += body.vy;
        body.angle += body.spin;
        bounce(body);
        body.el.style.transform = "translate(" + body.x.toFixed(1) + "px," + body.y.toFixed(1) + "px) rotate(" + body.angle.toFixed(2) + "deg)";
      });
      requestAnimationFrame(drift);
    }
    requestAnimationFrame(drift);
  }

  function typeHeadline(done) {
    var index = 0;
    function next() {
      if (index >= headlineParts.length) {
        if (done) done();
        return;
      }
      var part = headlineParts[index];
      typeInto(part.node, part.text, 78, function () {
        index += 1;
        next();
      });
    }
    next();
  }

  if (headlineParts[0].node && role) {
    if (reduced) {
      headlineParts.forEach(function (part) { part.node.textContent = part.text; });
      if (lineCaret) lineCaret.hidden = true;
      var roleIndex = 0;
      function showRole() {
        role.textContent = roles[roleIndex];
        if (roleLive) roleLive.textContent = roles[roleIndex];
        roleIndex = (roleIndex + 1) % roles.length;
      }
      showRole();
      setInterval(showRole, 2500);
    } else {
      later(function () {
        typeHeadline(function () {
          later(function () {
            if (lineCaret) lineCaret.hidden = true;
            if (roleCaret) roleCaret.hidden = false;
            cycle(0);
          }, 420);
        });
      }, 280);
    }
  }
})();
