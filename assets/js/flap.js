/* 전광판(split-flap) 숫자 애니메이션 — .flap 요소를 찾아 data-target 값으로 철컥거리며 착지시킴 */
(function () {
  var CHARS = '0123456789';

  function runFlap(el, targetChar, steps) {
    function step(i) {
      var isLast = i >= steps;
      var char = isLast ? targetChar : CHARS[Math.floor(Math.random() * CHARS.length)];
      var duration = 90 + i * 18;

      el.animate(
        [
          { transform: 'perspective(300px) rotateX(0deg)' },
          { transform: 'perspective(300px) rotateX(-90deg)' },
          { transform: 'perspective(300px) rotateX(0deg)' }
        ],
        { duration: duration, easing: 'ease-in' }
      );
      setTimeout(function () { el.textContent = char; }, duration * 0.5);

      if (!isLast) {
        setTimeout(function () { step(i + 1); }, duration);
      }
    }
    step(1);
  }

  function initFlaps() {
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    document.querySelectorAll('.flap').forEach(function (wrap) {
      var target = wrap.getAttribute('data-target') || '';
      var digits = wrap.querySelectorAll('.flap-digit');

      digits.forEach(function (d, i) {
        var char = target[i] || '0';
        if (reduceMotion) {
          d.textContent = char;
        } else {
          runFlap(d, char, 6 + i * 3);
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFlaps);
  } else {
    initFlaps();
  }
})();
