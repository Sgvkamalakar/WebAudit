
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("goToTopBtn").style.display = "block";
    } else {
        document.getElementById("goToTopBtn").style.display = "none";
    }
}

function toggleSection(sectionId) {
    var section = document.getElementById(sectionId);
    var expander = document.querySelector(`button[data-section="${sectionId}"]`);
    if (section.style.display === "none") {
        section.style.display = "block";
        expander.classList.add("active");
    } else {
        section.style.display = "none";
        expander.classList.remove("inactive");
    }
}

function openImage(imgUrl) {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");
    modal.style.display = "block";
    modalImg.src = imgUrl;
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

