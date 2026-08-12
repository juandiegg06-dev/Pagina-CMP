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

    // Initialize Slider
    showSlide(0);
    startSlideShow();
  }

  // 3. E.D.S. Interactive Zone Filter Logic
  const tabButtons = document.querySelectorAll(".eds-tab-btn");
  const stationCards = document.querySelectorAll(".station-card, .zone-muni-heading");

  if (tabButtons.length > 0 && stationCards.length > 0) {
    function filterStations(zone) {
      stationCards.forEach(card => {
        const cardZone = card.getAttribute("data-zone");
        const displayType = card.classList.contains("zone-muni-heading") ? "block" : "flex";
        if (zone === "all" || cardZone === zone) {
          card.style.display = displayType;
          // Quick entry animation
          card.style.opacity = "0";
          card.style.transform = "translateY(5px)";
          setTimeout(() => {
            card.style.transition = "all 0.3s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
          }, 50);
        } else {
          card.style.display = "none";
        }
      });
    }

    tabButtons.forEach(btn => {
      btn.addEventListener("click", function() {
        // Toggle active button style
        tabButtons.forEach(b => b.classList.remove("tab-active"));
        this.classList.add("tab-active");
        
        // Filter stations
        const zoneTarget = this.getAttribute("data-zone-target");
        filterStations(zoneTarget);
      });
    });

    // Default: Trigger display for the active tab on page load
    const activeTab = document.querySelector(".eds-tab-btn.tab-active");
    if (activeTab) {
      filterStations(activeTab.getAttribute("data-zone-target"));
    } else {
      filterStations("all");
    }
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

});
