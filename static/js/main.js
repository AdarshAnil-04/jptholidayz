/* ==========================================================================
   JPT HOLIDAYS — Client-side Interactivity & Layout Scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
  // Mobile Navigation Menu Toggle
  const mobileToggle = document.querySelector('.mobile-nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', function() {
      navMenu.classList.toggle('show');
    });
  }

  // Auto-dismiss Alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(function() {
        alert.remove();
      }, 500);
    }, 6000);
  });

  // Dynamic Accordion for Itinerary Days
  const accordionHeaders = document.querySelectorAll('.itinerary-accordion-header');
  accordionHeaders.forEach(function(header) {
    header.addEventListener('click', function() {
      const content = this.nextElementSibling;
      const icon = this.querySelector('.accordion-icon');
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
        if (icon) icon.textContent = '+';
      } else {
        content.style.maxHeight = content.scrollHeight + "px";
        if (icon) icon.textContent = '−';
      }
    });
  });
});
