function showLoginModal() {
  document
    .getElementById("loginModal")
    .classList.add("active");
}

function hideLoginModal() {
  document
    .getElementById("loginModal")
    .classList.remove("active");
}

function showSignupModal() {
  document
    .getElementById("signupModal")
    .classList.add("active");
}

function hideSignupModal() {
  document
    .getElementById("signupModal")
    .classList.remove("active");
}


function toggleMobileMenu() {

  document
    .getElementById("mobileMenu")
    .classList.toggle("mobile-active");

  document
    .querySelector(".mobile-menu-btn")
    .classList.toggle("active");
}


window.onload = function() {

    const params = new URLSearchParams(window.location.search);

    if (params.get("login") === "1") {
        showLoginModal();
    } else if (params.get("signup")==="1"){
        showSignupModal();

    }
}


function toggleReplies(postId) {

    const container =
        document.getElementById(
            `replies-${postId}`
        );

    container.classList.toggle(
        "active"
    );
}

document.querySelectorAll(".review-card").forEach((card) => {
  const review = card.querySelector(".review-content");
  const button = card.querySelector(".review-toggle");

  const hasOverflow = review.scrollHeight > review.clientHeight;
    button.hidden = !hasOverflow;

    if (!hasOverflow) {
        return;
    }

  if (!review || !button || review.scrollHeight <= review.clientHeight) {
    return;
  }

  button.hidden = false;
  button.addEventListener("click", () => {
    const expanded = review.classList.toggle("is-expanded");
    button.setAttribute("aria-expanded", String(expanded));
    button.textContent = expanded ? "Read less" : "Read more";
  });
});