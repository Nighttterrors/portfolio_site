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

window.onload = function() {

    const params = new URLSearchParams(window.location.search);

    if (params.get("login") === "1") {
        showLoginModal();
    } else if (params.get("signup")==="1"){
        showSignupModal();

    }
}