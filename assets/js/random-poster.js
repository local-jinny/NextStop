/* 랜덤 환승 버튼 — #random-poster-btn 클릭 시 12개 상세페이지 중 하나로 무작위 이동 */
(function () {
  var TOTAL_POSTERS = 12; // data/posters.json 항목 수와 맞춰서 관리

  function init() {
    var btn = document.getElementById('random-poster-btn');
    if (!btn) return;

    btn.addEventListener('click', function () {
      var n = Math.floor(Math.random() * TOTAL_POSTERS) + 1;
      var id = String(n).padStart(2, '0');
      window.location.href = 'poster/' + id + '.html';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
