// Daily Health Review - High-Converting Conversion Weapons Engine
// Powers: Dynamic Date, Scarcity Stock Counter, Sticky Mobile CTA Bar, and Exit-Intent Recovery Modal

document.addEventListener('DOMContentLoaded', () => {
  // 1. DYNAMIC CURRENT DATE INJECTOR (American Format: "November 4, 2026")
  const dateOptions = { month: 'long', day: 'numeric', year: 'numeric' };
  const formattedDate = new Intl.DateTimeFormat('en-US', dateOptions).format(new Date());

  document.querySelectorAll('.dynamic-current-date').forEach(el => {
    el.textContent = formattedDate;
  });

  // 2. REAL-TIME SCARCITY STOCK COUNTER
  const stockEls = document.querySelectorAll('.dynamic-stock-count');
  if (stockEls.length > 0) {
    let currentStock = parseInt(sessionStorage.getItem('dhr_live_stock') || '19', 10);
    stockEls.forEach(el => el.textContent = currentStock);

    // Subtle natural reduction after 18 seconds (simulating real purchases)
    setTimeout(() => {
      if (currentStock > 14) {
        currentStock -= 2;
        sessionStorage.setItem('dhr_live_stock', currentStock.toString());
        stockEls.forEach(el => {
          el.textContent = currentStock;
          el.classList.add('text-red-600', 'scale-110');
          setTimeout(() => el.classList.remove('scale-110'), 600);
        });
      }
    }, 18000);
  }

  // 3. STICKY MOBILE CTA BAR (Shows after 350px scroll, hidden on desktop)
  const stickyCta = document.getElementById('sticky-mobile-cta');
  const closeStickyBtn = document.getElementById('close-sticky-cta');

  if (stickyCta) {
    let stickyClosed = false;

    window.addEventListener('scroll', () => {
      if (!stickyClosed) {
        if (window.scrollY > 350) {
          stickyCta.classList.remove('translate-y-full');
          stickyCta.classList.add('translate-y-0');
        } else {
          stickyCta.classList.add('translate-y-full');
          stickyCta.classList.remove('translate-y-0');
        }
      }
    }, { passive: true });

    if (closeStickyBtn) {
      closeStickyBtn.addEventListener('click', (e) => {
        e.preventDefault();
        stickyClosed = true;
        stickyCta.classList.add('translate-y-full');
      });
    }
  }

  // 4. EXIT-INTENT RECOVERY MODAL
  const exitModal = document.getElementById('exit-intent-modal');
  const closeExitModalBtns = document.querySelectorAll('.close-exit-modal');

  if (exitModal) {
    const showExitModal = () => {
      if (!sessionStorage.getItem('dhr_modal_shown')) {
        sessionStorage.setItem('dhr_modal_shown', 'true');
        exitModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }
    };

    const hideExitModal = () => {
      exitModal.classList.add('hidden');
      document.body.style.overflow = '';
    };

    // Desktop: Trigger on mouse leaving viewport at top
    document.addEventListener('mouseleave', (e) => {
      if (e.clientY <= 12) {
        showExitModal();
      }
    });

    // Mobile: Trigger if user scrolls deep (> 75%) and idles for 10s
    let deepScrollTriggered = false;
    window.addEventListener('scroll', () => {
      const scrollPercent = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
      if (scrollPercent > 0.75 && !deepScrollTriggered) {
        deepScrollTriggered = true;
        setTimeout(() => {
          showExitModal();
        }, 12000);
      }
    }, { passive: true });

    closeExitModalBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        hideExitModal();
      });
    });

    exitModal.addEventListener('click', (e) => {
      if (e.target === exitModal) {
        hideExitModal();
      }
    });
  }
});
