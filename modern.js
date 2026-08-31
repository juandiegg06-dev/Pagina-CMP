/* ==========================================================================
   Coomulpinort Interactive Script - modern.js
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function() {
  
  // 1. Mobile Menu Drawer Toggle Logic
  const mobileToggle = document.querySelector(".mobile-menu-toggle");
  const closeDrawer = document.querySelector(".drawer-close-btn");
  const navDrawer = document.querySelector(".mobile-nav-drawer");
  const navOverlay = document.querySelector(".drawer-overlay");

  if (mobileToggle && navDrawer && navOverlay) {
    function openMobileMenu() {
      navDrawer.classList.add("drawer-open");
      navOverlay.classList.add("overlay-visible");
      document.body.style.overflow = "hidden"; // Prevents background scroll
    }

    function closeMobileMenu() {
      navDrawer.classList.remove("drawer-open");
      navOverlay.classList.remove("overlay-visible");
      document.body.style.overflow = "";
    }

    mobileToggle.addEventListener("click", openMobileMenu);
    if (closeDrawer) closeDrawer.addEventListener("click", closeMobileMenu);
    navOverlay.addEventListener("click", closeMobileMenu);
  }

  // 2. Homepage Hero Banner Slider Logic
  const slides = document.querySelectorAll(".slide");
  const nextBtn = document.querySelector(".slider-btn-next");
  const prevBtn = document.querySelector(".slider-btn-prev");
  const dots = document.querySelectorAll(".slider-dot");
  let currentSlideIndex = 0;
  let slideInterval;

  if (slides.length > 0) {
    function showSlide(index) {
      slides.forEach(slide => slide.classList.remove("slide-active"));
      
      // Wrap around logic
      if (index >= slides.length) {
        currentSlideIndex = 0;
      } else if (index < 0) {
        currentSlideIndex = slides.length - 1;
      } else {
        currentSlideIndex = index;
      }
      
      slides[currentSlideIndex].classList.add("slide-active");
      dots.forEach(dot => dot.classList.remove("slider-dot-active"));
      if (dots[currentSlideIndex]) {
        dots[currentSlideIndex].classList.add("slider-dot-active");
      }
    }

    function nextSlide() {
      showSlide(currentSlideIndex + 1);
    }

    function prevSlide() {
      showSlide(currentSlideIndex - 1);
    }

    // Auto rotate slides
    function startSlideShow() {
      slideInterval = setInterval(nextSlide, 6000); // Change slide every 6 seconds
    }

    function stopSlideShow() {
      clearInterval(slideInterval);
    }

    // Controls click handlers
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        stopSlideShow();
        nextSlide();
        startSlideShow();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        stopSlideShow();
        prevSlide();
        startSlideShow();
      });
    }

    dots.forEach(dot => {
      dot.addEventListener("click", function() {
        stopSlideShow();
        showSlide(parseInt(this.getAttribute("data-index"), 10));
        startSlideShow();
      });
    });

    // Initialize Slider
    showSlide(0);
    startSlideShow();

    // Touch swipe support — slide to the next/previous image with a finger
    const sliderContainer = document.querySelector(".hero-slider-container");
    if (sliderContainer) {
      let touchStartX = 0;
      let touchEndX = 0;

      sliderContainer.addEventListener("touchstart", (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      sliderContainer.addEventListener("touchend", (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const delta = touchEndX - touchStartX;
        const SWIPE_THRESHOLD = 40;
        if (Math.abs(delta) > SWIPE_THRESHOLD) {
          stopSlideShow();
          if (delta < 0) {
            nextSlide();
          } else {
            prevSlide();
          }
          startSlideShow();
        }
      }, { passive: true });
    }
  }

  // 3. E.D.S. Interactive Municipio Filter Logic
  const tabButtons = document.querySelectorAll(".eds-tab-btn");
  const muniGroups = document.querySelectorAll(".zone-muni-group");
  const mobileSelect = document.getElementById("eds-mobile-select");

  if (tabButtons.length > 0 && muniGroups.length > 0) {
    function filterStations(muni) {
      muniGroups.forEach(group => {
        const groupMuni = group.getAttribute("data-muni");
        // "none" (nothing selected) hides every group. Otherwise show only the match ("all" shows everything).
        const shouldShow = muni !== "none" && (muni === "all" || groupMuni === muni);
        group.style.display = shouldShow ? "block" : "none";
      });
    }

    tabButtons.forEach(btn => {
      btn.addEventListener("click", function() {
        const alreadyActive = this.classList.contains("tab-active");
        tabButtons.forEach(b => b.classList.remove("tab-active"));

        if (alreadyActive) {
          // Deselect: show nothing, same as the initial state
          filterStations("none");
          if (mobileSelect) mobileSelect.value = "none";
        } else {
          this.classList.add("tab-active");
          const muniTarget = this.getAttribute("data-muni-target");
          filterStations(muniTarget);
          if (mobileSelect) mobileSelect.value = muniTarget;
        }
      });
    });

    if (mobileSelect) {
      mobileSelect.addEventListener("change", function() {
        const muniTarget = this.value;
        tabButtons.forEach(b => b.classList.remove("tab-active"));
        if (muniTarget !== "all" && muniTarget !== "none") {
          const matchingBtn = document.querySelector(`.eds-tab-btn[data-muni-target="${muniTarget}"]`);
          if (matchingBtn) matchingBtn.classList.add("tab-active");
        }
        filterStations(muniTarget);
      });
    }

    // Default on page load: nothing selected, nothing shown
    filterStations("none");

    // Expand/collapse individual municipio station lists on demand
    document.querySelectorAll(".zone-muni-toggle").forEach(toggleBtn => {
      toggleBtn.addEventListener("click", function() {
        const cardsWrap = this.closest(".zone-muni-group").querySelector(".zone-muni-cards");
        const isExpanded = cardsWrap.classList.toggle("expanded");
        this.textContent = isExpanded ? "Ocultar estaciones" : "Ver estaciones";
      });
    });
  }

  // 4. Smooth animations on elements when they hover
  const buttons = document.querySelectorAll(".btn");
  buttons.forEach(btn => {
    btn.addEventListener("mousedown", function() {
      this.style.transform = "scale(0.97)";
    });
    btn.addEventListener("mouseup", function() {
      this.style.transform = "";
    });
  });

  // 5. Mobile-only footer accordion — wraps each footer column's content
  // so it can collapse behind its heading on small screens. Harmless on
  // desktop since the collapse styling only applies inside the mobile
  // media query.
  document.querySelectorAll(".footer-column").forEach(col => {
    const heading = col.querySelector("h3");
    if (!heading) return;
    const wrapper = document.createElement("div");
    wrapper.className = "footer-column-content";
    // Move every sibling after the heading into the wrapper
    while (heading.nextSibling) {
      wrapper.appendChild(heading.nextSibling);
    }
    col.appendChild(wrapper);
    heading.addEventListener("click", function() {
      col.classList.toggle("footer-column-open");
    });
  });

  // 6. Top bar rotator: cycles between the contact info and the social
  // icons, one at a time. The current panel fades out COMPLETELY before
  // the next one starts fading in, so they never overlap.
  const topBarContent = document.querySelector(".top-bar-content");
  const topBarInfo = document.querySelector(".top-bar-info");
  const topBarSocials = document.querySelector(".top-bar-socials");

  if (topBarContent && topBarInfo && topBarSocials) {
    topBarContent.classList.add("tb-has-rotator");
    topBarInfo.classList.add("tb-visible");

    const topBarPanels = [topBarInfo, topBarSocials];
    let topBarIndex = 0;

    function rotateTopBar() {
      topBarPanels[topBarIndex].classList.remove("tb-visible");
      topBarIndex = (topBarIndex + 1) % topBarPanels.length;
      topBarPanels[topBarIndex].classList.add("tb-visible");
    }

    setInterval(rotateTopBar, 4000);
  }

});
