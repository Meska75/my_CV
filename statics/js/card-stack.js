(function () {
  const root = document.querySelector("[data-card-stack]");
  if (!root) return;

  const stage = root.querySelector(".card-stack__stage");
  const cards = Array.from(root.querySelectorAll(".card-stack__card"));
  const dots = Array.from(root.querySelectorAll(".card-stack__dot"));
  const openLink = root.querySelector(".card-stack__open");
  const pauseBtn = root.querySelector(".card-stack__pause");
  const live = root.querySelector("[data-card-stack-live]");
  const len = cards.length;
  if (!stage || !len) return;

  const loop = root.dataset.loop !== "false";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const intervalMs = Math.max(700, Number(root.dataset.interval) || 2800);
  const rtl = document.documentElement.getAttribute("dir") === "rtl";
  const dir = rtl ? -1 : 1;

  let active = 0;
  let paused = reduceMotion || root.dataset.auto !== "true";
  let hover = false;
  let focusInside = false;
  let timer = 0;
  let announced = false;
  let drag = null;
  let suppressClick = false;

  function wrapIndex(n, length) {
    if (length <= 0) return 0;
    return ((n % length) + length) % length;
  }

  function signedOffset(i, current, length, doLoop) {
    const raw = i - current;
    if (!doLoop || length <= 1) return raw;
    const alt = raw > 0 ? raw - length : raw + length;
    return Math.abs(alt) < Math.abs(raw) ? alt : raw;
  }

  function metrics() {
    const width = stage.clientWidth || 320;
    const narrow = width < 680;
    const cardWidth = Math.round(Math.min(460, Math.max(220, width * (narrow ? 0.72 : 0.5))));
    const cardHeight = Math.round(Math.max(narrow ? 220 : 250, cardWidth * (narrow ? 0.82 : 0.64)));
    const maxOffset = 1;
    const spreadDeg = narrow ? 10 : 16;
    const rad = (spreadDeg * Math.PI) / 180;
    const aabbHalf =
      (cardWidth * Math.abs(Math.cos(rad)) + cardHeight * Math.abs(Math.sin(rad))) / 2;
    const sideRoom = Math.max(24, width / 2 - aabbHalf - 10);
    const cardSpacing = Math.round(Math.max(28, Math.min(sideRoom, cardWidth * 0.28)));
    stage.style.height = cardHeight + (narrow ? 36 : 72) + "px";
    return { cardWidth, cardHeight, maxOffset, cardSpacing, stepDeg: spreadDeg };
  }

  function paint(extraX) {
    const m = metrics();
    cards.forEach(function (card, i) {
      const off = signedOffset(i, active, len, loop);
      const abs = Math.abs(off);
      const visible = abs <= m.maxOffset;
      const isActive = off === 0;
      card.classList.toggle("is-off", !visible);
      card.setAttribute("aria-hidden", visible ? "false" : "true");
      card.classList.toggle("is-active", isActive);
      card.style.width = m.cardWidth + "px";
      card.style.height = m.cardHeight + "px";
      card.style.marginLeft = -(m.cardWidth / 2) + "px";

      const x = off * m.cardSpacing * dir + (isActive ? extraX || 0 : 0);
      const y = abs * 10 + (isActive ? -22 : 0);
      const rotZ = off * m.stepDeg * dir;
      const rotX = isActive ? 0 : 12;
      const scale = isActive ? 1.03 : 0.94;
      card.style.zIndex = String(100 - abs);
      card.style.transform =
        "translate3d(" + x + "px, " + y + "px, 0) rotateX(" + rotX + "deg) rotateZ(" + rotZ + "deg) scale(" + scale + ")";

      const inner = card.querySelector(".card-stack__inner");
      if (inner) inner.style.transform = "translateZ(" + (-abs * 120) + "px)";
      const details = card.querySelector(".card-stack__details");
      if (details) {
        details.tabIndex = isActive ? 0 : -1;
        details.setAttribute("aria-hidden", isActive ? "false" : "true");
      }
    });

    dots.forEach(function (dot, i) {
      const on = i === active;
      dot.classList.toggle("is-on", on);
      if (on) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });

    const href = cards[active].dataset.href || "";
    if (openLink) {
      if (href) {
        openLink.href = href;
        openLink.hidden = false;
      } else {
        openLink.hidden = true;
      }
    }

    if (announced && live) live.textContent = cards[active].dataset.title || "";
  }

  function go(index) {
    active = wrapIndex(index, len);
    paint(0);
  }

  function prev() {
    if (!loop && active <= 0) return;
    go(active - 1);
  }

  function next() {
    if (!loop && active >= len - 1) return;
    go(active + 1);
  }

  function held() {
    return paused || hover || focusInside;
  }

  function arm() {
    window.clearInterval(timer);
    if (held() || reduceMotion) return;
    timer = window.setInterval(function () {
      if (loop || active < len - 1) next();
    }, intervalMs);
  }

  function setPaused(value) {
    paused = value;
    root.classList.toggle("is-paused", paused);
    if (!pauseBtn) return;
    pauseBtn.setAttribute("aria-pressed", paused ? "true" : "false");
    const label = paused ? pauseBtn.dataset.labelPlay : pauseBtn.dataset.labelPause;
    if (label) pauseBtn.setAttribute("aria-label", label);
    arm();
  }

  cards.forEach(function (card) {
    card.addEventListener("click", function (event) {
      if (suppressClick) {
        suppressClick = false;
        event.preventDefault();
        return;
      }
      if (event.target.closest("a")) return;
      const index = Number(card.dataset.index);
      if (index !== active) go(index);
    });
  });

  dots.forEach(function (dot) {
    dot.addEventListener("click", function () {
      go(Number(dot.dataset.index));
    });
  });

  stage.addEventListener("keydown", function (event) {
    const forward = rtl ? "ArrowLeft" : "ArrowRight";
    const back = rtl ? "ArrowRight" : "ArrowLeft";
    if (event.key === forward) {
      event.preventDefault();
      next();
    } else if (event.key === back) {
      event.preventDefault();
      prev();
    }
  });

  stage.addEventListener("pointerdown", function (event) {
    if (event.button !== undefined && event.button !== 0) return;
    const card = event.target.closest(".card-stack__card");
    if (!card || Number(card.dataset.index) !== active) return;
    if (event.target.closest("a")) return;
    drag = { id: event.pointerId, x: event.clientX, dx: 0, moved: false, card: card };
    card.classList.add("is-dragging");
    if (card.setPointerCapture) card.setPointerCapture(event.pointerId);
  });

  stage.addEventListener("pointermove", function (event) {
    if (!drag || event.pointerId !== drag.id) return;
    drag.dx = event.clientX - drag.x;
    if (Math.abs(drag.dx) > 8) drag.moved = true;
    paint(drag.dx);
  });

  function endDrag(event) {
    if (!drag || (event && event.pointerId !== drag.id)) return;
    const travel = drag.dx * dir;
    const moved = drag.moved;
    const card = drag.card;
    const width = card.getBoundingClientRect().width || 320;
    const threshold = Math.min(160, width * 0.22);
    drag = null;
    card.classList.remove("is-dragging");
    if (moved) suppressClick = true;
    if (reduceMotion) {
      paint(0);
      return;
    }
    if (travel > threshold) prev();
    else if (travel < -threshold) next();
    else paint(0);
  }

  stage.addEventListener("pointerup", endDrag);
  stage.addEventListener("pointercancel", endDrag);

  root.addEventListener("mouseenter", function () {
    hover = true;
    arm();
  });
  root.addEventListener("mouseleave", function () {
    hover = false;
    arm();
  });
  root.addEventListener("focusin", function () {
    focusInside = true;
    arm();
  });
  root.addEventListener("focusout", function (event) {
    if (!root.contains(event.relatedTarget)) {
      focusInside = false;
      arm();
    }
  });

  if (pauseBtn) {
    pauseBtn.addEventListener("click", function () {
      setPaused(!paused);
    });
  }

  document.addEventListener("visibilitychange", arm);
  window.addEventListener("resize", function () {
    paint(drag ? drag.dx : 0);
  });

  if (reduceMotion && pauseBtn) pauseBtn.hidden = true;
  setPaused(paused);
  paint(0);
  announced = true;
})();
