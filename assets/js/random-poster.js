/* 랜덤 환승 버튼 — #random-poster-btn 클릭 시 상세페이지 중 하나로 무작위 이동.
   index.html/gallery.html/info.html(루트)과 poster/*.html(하위 폴더) 양쪽에서 공용으로 쓰이므로
   현재 위치에 따라 링크 경로("poster/01.html" vs "01.html")를 자동으로 판단한다.
   버튼의 data-total 속성이 있으면 그 값을, 없으면 아래 기본값을 포스터 총 개수로 사용한다. */
(function () {
  var DEFAULT_TOTAL = 14; // data/posters.json 항목 수와 맞춰서 관리 (정적 페이지의 기본값)

  function init() {
    var btn = document.getElementById('random-poster-btn');
    if (!btn) return;

    var total = parseInt(btn.getAttribute('data-total'), 10) || DEFAULT_TOTAL;
    var inPosterDir = /\/poster\//.test(window.location.pathname);
    var currentMatch = window.location.pathname.match(/(\d{2})\.html$/);
    var currentId = inPosterDir && currentMatch ? currentMatch[1] : null;

    btn.addEventListener('click', function () {
      var id;
      do {
        id = String(Math.floor(Math.random() * total) + 1).padStart(2, '0');
      } while (total > 1 && id === currentId);

      window.location.href = (inPosterDir ? '' : 'poster/') + id + '.html';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
