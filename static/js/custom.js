// Custom JavaScript for enhancing navigation functionality

document.addEventListener('DOMContentLoaded', function() {
  // Function to handle smooth scrolling to target sections
  function smoothScrollToTarget(targetId) {
    const targetElement = document.getElementById(targetId);
    
    if (targetElement) {
      // Get the header height
      const header = document.querySelector('header');
      const headerHeight = header.offsetHeight;
      
      // Calculate the target position with extra padding
      const extraPadding = 20;
      const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight - extraPadding;
      
      // Smooth scroll to the target
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
      
      // Add a class to highlight the target section briefly
      targetElement.classList.add('target-highlight');
      setTimeout(function() {
        targetElement.classList.remove('target-highlight');
      }, 2000);
    }
  }
  
  // Process all links that point to hash targets
  function setupHashLinks() {
    // Get all links that point to hash targets on the same page
    const hashLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');
    
    hashLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
        // Prevent default anchor behavior
        e.preventDefault();
        
        // Get the target ID from the href
        const targetId = this.getAttribute('href').substring(1);
        
        // Smooth scroll to the target
        smoothScrollToTarget(targetId);
      });
    });
  }
  
  // Handle initial hash in URL
  function handleInitialHash() {
    if (window.location.hash) {
      // Remove the # character
      const targetId = window.location.hash.substring(1);
      
      // Wait a moment for the page to fully load
      setTimeout(function() {
        smoothScrollToTarget(targetId);
      }, 500);
    }
  }
  
  // Auto-close mobile TOC menu when a link is clicked
  const pageTOC = document.getElementById('pageTOC');
  if (pageTOC) {
    const tocLinks = pageTOC.querySelectorAll('a');
    
    tocLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
        // Prevent default anchor behavior
        e.preventDefault();
        
        // Get the target ID from the href
        const targetId = this.getAttribute('href').substring(1);
        
        // Close the TOC menu
        const bsCollapse = new bootstrap.Collapse(pageTOC);
        bsCollapse.hide();
        
        // Wait for the collapse animation to finish before scrolling
        setTimeout(function() {
          smoothScrollToTarget(targetId);
        }, 350);
      });
    });
  }
  
  // Also handle the other mobile menus (materials and units)
  const mobileMenus = ['materialsSidebar', 'unitsSidebar'];
  
  mobileMenus.forEach(function(menuId) {
    const menu = document.getElementById(menuId);
    if (menu) {
      const menuLinks = menu.querySelectorAll('a');
      
      menuLinks.forEach(function(link) {
        link.addEventListener('click', function() {
          // Close the menu when a link is clicked
          const bsCollapse = new bootstrap.Collapse(menu);
          bsCollapse.hide();
        });
      });
    }
  });
  
  // Setup all hash links and handle initial hash
  setupHashLinks();
  handleInitialHash();
  
  // Add scroll event listener to ensure header stays visible
  let lastScrollTop = 0;
  const header = document.querySelector('header');
  
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Make sure header is always visible
    if (scrollTop > lastScrollTop) {
      // Scrolling down
      header.style.transform = 'translateY(0)';
    } else {
      // Scrolling up
      header.style.transform = 'translateY(0)';
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  }, { passive: true });
});

/* 2. Mobile: Collapse TOC dropdown when clicking outside */
document.addEventListener('DOMContentLoaded', function () {
    const tocDropdownButton = document.querySelector('.td-page-meta--js .td-page-meta--toc button[data-bs-toggle="collapse"]'); // Adjust selector if needed
    const tocDropdownContent = document.querySelector('.td-page-meta--js .td-page-meta--toc .collapse'); // Adjust selector if needed
    const mainContentArea = document.querySelector('.td-content'); // Adjust selector for your main content area

    if (tocDropdownButton && tocDropdownContent && mainContentArea) {
        document.addEventListener('click', function (event) {
            // Check if the dropdown is currently shown (Bootstrap uses 'show' class)
            const isTocOpen = tocDropdownContent.classList.contains('show');
            // Check if the click was outside the TOC button AND outside the TOC content area
            const isClickInsideTocButton = tocDropdownButton.contains(event.target);
            const isClickInsideTocContent = tocDropdownContent.contains(event.target);

            if (isTocOpen && !isClickInsideTocButton && !isClickInsideTocContent) {
                // If open and click is outside, trigger a click on the button to close it
                // Using Bootstrap's API is safer if available, but clicking the button often works
                tocDropdownButton.click();
                // Or, if using Bootstrap 5 JS API directly (requires Bootstrap object):
                // const collapseInstance = bootstrap.Collapse.getInstance(tocDropdownContent);
                // if (collapseInstance) {
                //    collapseInstance.hide();
                // }
            }
        });
    } else {
        console.warn('Mobile TOC collapse script: Could not find necessary elements.');
        console.warn('Button selector used:', '.td-page-meta--js .td-page-meta--toc button[data-bs-toggle="collapse"]');
        console.warn('Content selector used:', '.td-page-meta--js .td-page-meta--toc .collapse');
    }
});
