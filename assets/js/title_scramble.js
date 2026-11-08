// Port of the departuremono.com title scramble animation.
// Independent loops for first name / space / last name; each cycle swaps
// a few chars for look-alike glyphs, with a 10% chance of a rapid 4-frame flash.
(function () {
  "use strict";

  // Uppercase-only substitutions (the title is rendered uppercase).
  var GLYPHS = {
    A: "Λ4∀",
    B: "8",
    D: "ĐÐ",
    E: "3Ξ€",
    I: "1!|",
    M: "ɱΜ",
    R: "₹2",
  };

  // Idle window between cycles: base + up to range (ms).
  var IDLE_BASE = 2500;
  var IDLE_RANGE = 5000;

  function randInt(n) {
    return Math.floor(Math.random() * n);
  }
  function sample(arr) {
    return arr[randInt(arr.length)];
  }
  function permutation(n) {
    var a = new Array(n);
    for (var i = 0; i < n; i++) a[i] = i;
    for (var j = n - 1; j > 0; j--) {
      var k = randInt(j + 1);
      var t = a[j];
      a[j] = a[k];
      a[k] = t;
    }
    return a;
  }
  function natural(n) {
    return randInt(n);
  }

  function scramble(word, counts) {
    var n = sample(counts);
    if (n === 0) return word;
    var out = word.split("");
    var idxs = word.length === 1 ? [0] : permutation(word.length);
    for (var i = 0; i < n; i++) {
      var ch = word.charAt(idxs[i]);
      var pool = GLYPHS[ch];
      if (pool) out[idxs[i]] = pool.charAt(randInt(pool.length));
    }
    return out.join("");
  }

  function startLoop(el, counts, flashCounts) {
    var word = el.getAttribute("data-dm-word");
    if (word == null) return;
    var setText = function (t) {
      el.textContent = t;
    };
    setText(word);

    (function loop() {
      var idle = natural(IDLE_RANGE) + IDLE_BASE;
      if (flashCounts && Math.random() < 0.1) {
        setTimeout(function () {
          setText(scramble(word, flashCounts));
        }, idle);
        setTimeout(function () {
          setText(word);
        }, idle + 70);
        setTimeout(function () {
          setText(scramble(word, flashCounts));
        }, idle + 140);
        setTimeout(function () {
          setText(word);
        }, idle + 210);
        setTimeout(loop, idle + 280);
      } else {
        setTimeout(function () {
          setText(scramble(word, counts));
        }, idle);
        setTimeout(function () {
          setText(word);
        }, idle + 80);
        setTimeout(loop, idle + 160);
      }
    })();
  }

  function init() {
    var firsts = document.querySelectorAll(".dm-scramble-first");
    var lasts = document.querySelectorAll(".dm-scramble-last");
    // first/last: lengths ~4-5, so scramble 0-3 chars; flash swaps more.
    for (var i = 0; i < firsts.length; i++) {
      startLoop(firsts[i], [0, 0, 0, 1, 1, 2, 2, 2, 3], [2, 3, 4, 4, 5, 5]);
    }
    for (var k = 0; k < lasts.length; k++) {
      startLoop(lasts[k], [0, 0, 0, 1, 1, 2, 2], [1, 1, 2, 2, 3, 3]);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
