/* ==========================================================================
   Trio Self Drive — Dashboard JavaScript
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* Sidebar toggle for mobile */
  var sidebarToggleBtn = document.querySelector('.sidebar-toggle-btn');
  var sidebar = document.querySelector('.dashboard-sidebar');
  var overlay = document.querySelector('.sidebar-overlay');

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('show');
    if (overlay) overlay.classList.remove('show');
  }

  if (sidebarToggleBtn && sidebar) {
    sidebarToggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('show');
      if (overlay) overlay.classList.toggle('show');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }

  /* Auto-dismiss alerts */
  var alerts = document.querySelectorAll('.alert-auto-dismiss');
  alerts.forEach(function (alertEl) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 5000);
  });

  /* Image preview for car add/edit form */
  var imageInput = document.getElementById('id_image');
  var imagePreview = document.getElementById('image-preview');
  if (imageInput && imagePreview) {
    imageInput.addEventListener('change', function () {
      var file = imageInput.files[0];
      if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
          imagePreview.src = e.target.result;
          imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  /* Confirm dialogs for destructive actions */
  var confirmButtons = document.querySelectorAll('[data-confirm]');
  confirmButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var message = btn.getAttribute('data-confirm') || 'Are you sure?';
      if (!window.confirm(message)) {
        e.preventDefault();
      }
    });
  });

  /* Auto-submit filter dropdowns in dashboard tables */
  var autoSubmitSelects = document.querySelectorAll('.auto-submit-select');
  autoSubmitSelects.forEach(function (el) {
    el.addEventListener('change', function () {
      el.closest('form').submit();
    });
  });

});
