// The ONE place the checkout link lives. Paste the Gumroad product link between the quotes.
var BUY_URL = "";

(function () {
  var buttons = document.querySelectorAll("[data-buy]");
  for (var i = 0; i < buttons.length; i++) {
    var b = buttons[i];
    if (BUY_URL) {
      b.href = BUY_URL;
    } else {
      b.textContent = "Launching soon";
      b.classList.add("soon");
      b.removeAttribute("href");
    }
  }
})();
