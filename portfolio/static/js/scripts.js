// Scrolling animation for skill bars
const skillBars = document.querySelectorAll('.skill-progress');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        bar.style.width = bar.dataset.width;
        observer.unobserve(bar); // animate only once
      }
    });
  }, {
    threshold: 0.05,
    rootMargin: "0px 0px -100px 0px" // triggers when 50% visible
  });

  skillBars.forEach(bar => observer.observe(bar));
