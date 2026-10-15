(function () {
  var cards = document.querySelectorAll(".services .info-card");
  if (!cards.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  cards.forEach(function (card) {
    card.addEventListener("mousemove", function (event) {
      var rect = card.getBoundingClientRect();
      var x = event.clientX - rect.left - rect.width / 2;
      var y = event.clientY - rect.top - rect.height / 2;
      var spot = ((event.clientX - rect.left) / rect.width) * 100;
      card.style.setProperty("--rotation", Math.atan2(y, x) + "rad");
      card.style.setProperty("--spot-x", Math.max(8, Math.min(92, spot)) + "%");
    });

    card.addEventListener("mouseleave", function () {
      card.style.setProperty("--rotation", "0deg");
      card.style.setProperty("--spot-x", "50%");
    });
  });
})();
