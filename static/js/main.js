/* ==========================================================================
   Trio Self Drive — Main JavaScript
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* Navbar shadow + shrink on scroll */
  var navbar = document.querySelector('.tsd-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 10) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  /* Auto-dismiss alert messages after 5 seconds */
  var alerts = document.querySelectorAll('.alert-auto-dismiss');
  alerts.forEach(function (alertEl) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 5000);
  });

  /* Simple fade-in-up animation on scroll using IntersectionObserver */
  var animatedEls = document.querySelectorAll('.animate-on-scroll');
  if (animatedEls.length && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-up');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    animatedEls.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* Bootstrap tooltip initialization */
  var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  /* Booking form: auto-set minimum return date based on pickup date */
  var pickupDateInput = document.getElementById('id_pickup_date');
  var returnDateInput = document.getElementById('id_return_date');
  if (pickupDateInput && returnDateInput) {
    var syncMinReturnDate = function () {
      if (pickupDateInput.value) {
        returnDateInput.min = pickupDateInput.value;
      }
    };
    syncMinReturnDate();
    pickupDateInput.addEventListener('change', syncMinReturnDate);
  }

  /* Car filter form: auto-submit on select change */
  var autoSubmitSelects = document.querySelectorAll('.auto-submit-select');
  autoSubmitSelects.forEach(function (el) {
    el.addEventListener('change', function () {
      el.closest('form').submit();
    });
  });

  /* Confirm dialogs for destructive actions without a dedicated confirm page */
  var confirmButtons = document.querySelectorAll('[data-confirm]');
  confirmButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var message = btn.getAttribute('data-confirm') || 'Are you sure?';
      if (!window.confirm(message)) {
        e.preventDefault();
      }
    });
  });

});
