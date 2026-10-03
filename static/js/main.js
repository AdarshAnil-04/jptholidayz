/* ==========================================================================
   JPT HOLIDAYS — Client-side Interactivity, Animations & Dynamic Controls
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
  
  // 1. Navbar Sticky & Scroll Elevation
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }, { passive: true });
  }

  // 2. Mobile Navigation Menu Toggle
  const mobileToggle = document.querySelector('.mobile-nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', function() {
      const isExpanded = navMenu.classList.toggle('show');
      mobileToggle.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target) && navMenu.classList.contains('show')) {
        navMenu.classList.remove('show');
        mobileToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 3. Scroll Reveal Observer
  const revealElements = document.querySelectorAll('[data-reveal]');
  if (revealElements.length > 0) {
    if ('IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      });

      revealElements.forEach(el => revealObserver.observe(el));
    } else {
      // Fallback for older browsers
      revealElements.forEach(el => el.classList.add('revealed'));
    }
  }

  // 4. Itinerary Accordion Expand/Collapse
  const itineraryHeaders = document.querySelectorAll('.itinerary-header');
  itineraryHeaders.forEach(header => {
    header.addEventListener('click', function() {
      const card = this.closest('.itinerary-card');
      const body = card.querySelector('.itinerary-body');
      const toggleIcon = this.querySelector('.accordion-toggle-icon');
      
      if (body) {
        const isOpen = body.style.display !== 'none';
        body.style.display = isOpen ? 'none' : 'block';
        if (toggleIcon) {
          toggleIcon.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
        }
      }
    });
  });

  // 5. Lightbox Modal Support for Gallery Images
  const galleryItems = document.querySelectorAll('[data-lightbox-src]');
  const modalOverlay = document.querySelector('.modal-overlay');
  
  if (galleryItems.length > 0 && modalOverlay) {
    const modalImage = modalOverlay.querySelector('.modal-img');
    const modalCaption = modalOverlay.querySelector('.modal-caption');
    const modalClose = modalOverlay.querySelector('.modal-close');

    galleryItems.forEach(item => {
      item.addEventListener('click', function() {
        const src = this.getAttribute('data-lightbox-src');
        const caption = this.getAttribute('data-caption') || '';
        
        if (modalImage) modalImage.src = src;
        if (modalCaption) modalCaption.textContent = caption;
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    const closeModal = () => {
      modalOverlay.classList.remove('active');
      document.body.style.overflow = '';
    };

    if (modalClose) modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', function(e) {
      if (e.target === modalOverlay) closeModal();
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
        closeModal();
      }
    });
  }

  // 6. Auto-dismiss Notification Flash Messages
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      setTimeout(function() {
        alert.remove();
      }, 500);
    }, 6000);
  });

  // 7. Form Submission Loading States
  const forms = document.querySelectorAll('form[data-loading-state]');
  forms.forEach(form => {
    form.addEventListener('submit', function() {
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <svg class="icon icon-sm spin" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" opacity="0.25"/>
            <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          Processing...
        `;
      }
    });
  });

});

