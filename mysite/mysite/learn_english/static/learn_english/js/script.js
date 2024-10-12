'use strict';

function flipCard(card) {
        card.classList.toggle('flipped');
    }

function toggleTranslation() {
    const englishText = document.getElementById('english-text');
    const ukrainianText = document.getElementById('ukrainian-text');
    const button = document.getElementById('translate-button');

    if (englishText.style.display === "none") {
        englishText.style.display = "block";
        ukrainianText.style.display = "none";
        button.innerHTML = "Translate text";
    } else {
        englishText.style.display = "none";
        ukrainianText.style.display = "block";
        button.innerHTML = "Show original";
    }
}