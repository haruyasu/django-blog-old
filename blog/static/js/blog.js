"use strict";

const mainNav = document.querySelector("#mainNav")

// windowの幅が992px以上の場合
if (window.innerWidth > 992) {
  let previousTop = 0;

  // スクロールイベント
  window.addEventListener('scroll', (e) => {
    // トップを取得
    let currentTop = document.documentElement.scrollTop || document.body.scrollTop;

    if (currentTop < previousTop) {
      // スクロールUP
      if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
        mainNav.classList.add("is-visible");
      } else {
        // スクロールTOP
        mainNav.classList.remove("is-visible", "is-fixed");
      }
    } else if (currentTop > previousTop) {
      // スクロールDOWN
      mainNav.classList.remove("is-visible");

      if (currentTop > mainNav.clientHeight && !mainNav.classList.contains('is-fixed')) {
        mainNav.classList.add("is-fixed");
      }
    }
    previousTop = currentTop;
  });
}
