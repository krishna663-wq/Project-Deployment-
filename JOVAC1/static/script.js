document.addEventListener('DOMContentLoaded', function () {
    const learnMoreLinks = document.querySelectorAll('.learn-more');

    learnMoreLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
