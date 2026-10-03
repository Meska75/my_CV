(function () {
  const root = document.querySelector("[data-pixel-hero]");
  const wrap = document.querySelector("[data-pixel-canvas]");
  if (!root || !wrap) return;

  const canvas = document.createElement("canvas");
  wrap.appendChild(canvas);

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const gap = 6;
  const cream = "rgba(244, 239, 230, 0.55)";
  let accent = "#cdaa80";
  const pixels = [];
  let frame = 0;
  let last = 0;

  function colorAt(index) {
    return index % 5 === 0 ? accent : cream;
  }

  function makePixel(ctx, x, y, delay) {
    const speed = (0.08 + Math.random() * 0.32) * (reduced ? 0 : 0.03);
    const pixel = {
      x: x,
      y: y,
      size: 0,
      max: 0.5 + Math.random() * 1.5,
      step: 0.12 + Math.random() * 0.16,
      min: 0.5,
      delay: delay,
      counter: 0,
      counterStep: 1.8 + Math.random() * 1.4 + (canvas.width + canvas.height) * 0.008,
      reverse: false,
      shimmer: false,
      idle: false,
      draw: function () {
        const offset = 1 - pixel.size * 0.5;
        ctx.fillStyle = colorAt((x / gap + y / gap) | 0);
        ctx.fillRect(pixel.x + offset, pixel.y + offset, pixel.size, pixel.size);
      },
      appear: function () {
        pixel.idle = false;
        if (pixel.counter <= pixel.delay) {
          pixel.counter += pixel.counterStep;
          return;
        }
        if (pixel.size >= pixel.max) pixel.shimmer = true;
        if (pixel.shimmer) {
          if (pixel.size >= pixel.max) pixel.reverse = true;
          else if (pixel.size <= pixel.min) pixel.reverse = false;
          pixel.size += pixel.reverse ? -speed : speed;
        } else {
          pixel.size += pixel.step;
        }
        pixel.draw();
      }
    };
    return pixel;
  }

  function init() {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    accent = getComputedStyle(document.documentElement).getPropertyValue("--accent-color").trim() || "#cdaa80";
    const rect = wrap.getBoundingClientRect();
    const width = Math.floor(rect.width);
    const height = Math.floor(rect.height);
    canvas.width = width;
    canvas.height = height;
    pixels.length = 0;
    for (let x = 0; x < width; x += gap) {
      for (let y = 0; y < height; y += gap) {
        const dx = x - width / 2;
        const dy = y - height / 2;
        const delay = reduced ? 0 : Math.sqrt(dx * dx + dy * dy) * 0.65;
        const pixel = makePixel(ctx, x, y, delay);
        if (reduced) {
          pixel.size = pixel.max;
          pixel.shimmer = false;
        }
        pixels.push(pixel);
      }
    }
  }

  function loop(now) {
    frame = requestAnimationFrame(loop);
    if (now - last < 1000 / 60) return;
    last = now;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < pixels.length; i += 1) pixels[i].appear();
  }

  init();
  if (reduced) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < pixels.length; i += 1) pixels[i].draw();
  } else {
    frame = requestAnimationFrame(loop);
  }

  const observer = new ResizeObserver(function () {
    cancelAnimationFrame(frame);
    init();
    if (!reduced) frame = requestAnimationFrame(loop);
  });
  observer.observe(wrap);

  let ticking = false;
  function syncSidebar() {
    ticking = false;
    const passed = root.getBoundingClientRect().bottom < window.innerHeight * 0.35;
    document.body.classList.toggle("intro-active", !passed);
  }
  window.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(syncSidebar);
  }, { passive: true });
  window.addEventListener("resize", syncSidebar);
  syncSidebar();
})();
