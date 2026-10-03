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

  // 8. Scroll Progress Indicator Line
  const progressBar = document.querySelector('.scroll-progress-bar');
  if (progressBar) {
    window.addEventListener('scroll', function() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = Math.min(100, Math.max(0, scrolled)) + '%';
    }, { passive: true });
  }

  // 9. Hero Choreography Load Sequence
  const heroElement = document.querySelector('.hero');
  if (heroElement) {
    setTimeout(function() {
      heroElement.classList.add('hero-loaded');
    }, 100);
  }

  // 10. Desktop Cursor Atmosphere Glow Orb
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!isTouchDevice && !prefersReducedMotion) {
    const pointerOrb = document.createElement('div');
    pointerOrb.className = 'pointer-glow-orb';
    document.body.appendChild(pointerOrb);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let orbX = mouseX;
    let orbY = mouseY;

    window.addEventListener('mousemove', function(e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
    }, { passive: true });

    function animatePointerOrb() {
      orbX += (mouseX - orbX) * 0.12;
      orbY += (mouseY - orbY) * 0.12;
      pointerOrb.style.left = orbX + 'px';
      pointerOrb.style.top = orbY + 'px';
      requestAnimationFrame(animatePointerOrb);
    }
    animatePointerOrb();
  }

  // 11. Magnetic Button Physics
  const magneticButtons = document.querySelectorAll('.btn-magnetic');
  if (!isTouchDevice && !prefersReducedMotion) {
    magneticButtons.forEach(btn => {
      btn.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        this.style.transform = `translate(${x * 0.18}px, ${y * 0.18}px) scale(1.03)`;
      });

      btn.addEventListener('mouseleave', function() {
        this.style.transform = 'translate(0px, 0px) scale(1)';
      });
    });
  }

  // 12. Clip-Path Image Reveal Observer
  const clipRevealElements = document.querySelectorAll('[data-reveal-clip]');
  if (clipRevealElements.length > 0) {
    if ('IntersectionObserver' in window && !prefersReducedMotion) {
      const clipObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });

      clipRevealElements.forEach(el => clipObserver.observe(el));
    } else {
      clipRevealElements.forEach(el => el.classList.add('revealed'));
    }
  }

  // 13. Page Transition Sweep Overlay
  const transitionOverlay = document.querySelector('.page-transition-overlay');
  if (transitionOverlay && !prefersReducedMotion) {
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (href && !href.startsWith('#') && !href.startsWith('javascript') && !link.hasAttribute('target') && link.hostname === window.location.hostname) {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          transitionOverlay.classList.add('active');
          setTimeout(function() {
            window.location.href = href;
          }, 350);
        });
      }
    });
  }

});


