/* 포스터 상세페이지 이미지 슬라이더 — 메인 포스터 + 상세컷을 스와이프/클릭으로 넘겨봄(인스타그램 게시물 방식).
   상세컷(2번째 슬라이드부터)은 CSS에서 4:5로 고정 크롭.
   1번째 슬라이드(메인 포스터)만 다른 상세페이지처럼 원본 비율 그대로 보여주기 위해,
   메인 이미지가 보일 때만 viewport의 aspect-ratio를 원본 비율로 바꿔치기한다.
   [data-slider]가 없는 일반 상세페이지(이미지 1장)에서는 아무 동작도 하지 않는다. */
(function () {
  function setup(slider) {
    var viewport = slider.querySelector('.poster-slider-viewport');
    var track = slider.querySelector('[data-slider-track]');
    if (!track) return;
    var slides = Array.prototype.slice.call(track.children);
    var dotsWrap = slider.querySelector('[data-slider-dots]');
    var dots = dotsWrap ? Array.prototype.slice.call(dotsWrap.children) : [];
    var prevBtn = slider.querySelector('[data-slider-prev]');
    var nextBtn = slider.querySelector('[data-slider-next]');
    var total = slides.length;
    if (total <= 1) return;

    function currentIndex() {
      var w = track.clientWidth || 1;
      return Math.round(track.scrollLeft / w);
    }

    function goTo(index) {
      index = Math.max(0, Math.min(total - 1, index));
      track.scrollTo({ left: index * track.clientWidth, behavior: 'smooth' });
    }

    function mainMediaSize(media) {
      // <img>는 naturalWidth/Height, <video>는 videoWidth/Height로 원본 크기를 읽는다.
      if (media.tagName === 'VIDEO') return [media.videoWidth, media.videoHeight];
      return [media.naturalWidth, media.naturalHeight];
    }

    function applyMainRatio() {
      var mainMedia = slides[0].querySelector('img, video');
      if (!viewport || !mainMedia) return;
      var size = mainMediaSize(mainMedia);
      if (!size[0]) return;
      viewport.style.aspectRatio = size[0] + ' / ' + size[1];
    }

    function syncRatio(index) {
      if (!viewport) return;
      if (index !== 0) {
        viewport.style.aspectRatio = ''; // CSS 기본값(4/5)으로 복귀
        return;
      }
      var mainMedia = slides[0].querySelector('img, video');
      if (!mainMedia) return; // onerror로 placeholder-box가 됐으면 기본 4/5 유지
      if (mainMediaSize(mainMedia)[0]) {
        applyMainRatio();
      } else if (mainMedia.tagName === 'VIDEO') {
        mainMedia.addEventListener('loadedmetadata', applyMainRatio, { once: true });
      } else if (!mainMedia.complete) {
        mainMedia.addEventListener('load', applyMainRatio, { once: true });
      }
    }

    function updateUI() {
      var i = currentIndex();
      dots.forEach(function (d, di) { d.classList.toggle('is-active', di === i); });
      if (prevBtn) prevBtn.disabled = i <= 0;
      if (nextBtn) nextBtn.disabled = i >= total - 1;
      syncRatio(i);
    }

    dots.forEach(function (d, i) {
      d.addEventListener('click', function () { goTo(i); });
    });
    if (prevBtn) prevBtn.addEventListener('click', function () { goTo(currentIndex() - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { goTo(currentIndex() + 1); });

    var raf = null;
    track.addEventListener('scroll', function () {
      if (raf) return;
      raf = requestAnimationFrame(function () { updateUI(); raf = null; });
    });
    window.addEventListener('resize', function () { goTo(currentIndex()); updateUI(); });

    updateUI();
  }

  function init() {
    document.querySelectorAll('[data-slider]').forEach(setup);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
