document.querySelector(".get-btn").addEventListener("click", function () {
  document.getElementById("target").scrollIntoView({ behavior: "smooth" });
});
const cards = document.querySelectorAll('.card');

window.addEventListener('scroll', () => {
  const triggerBottom = window.innerHeight * 0.8; // 80% of the viewport height

  cards.forEach((card, index) => {
      const cardTop = card.getBoundingClientRect().top;

      if (cardTop < triggerBottom) {
          // Add a delay based on the index of the card to create staggered effect
          setTimeout(() => {
              card.classList.add('visible');
          }, index * 150); // 200ms delay between each card
      }
  });
});

// Close the modal

const closeBtn = document.querySelector('.close-btn');
closeBtn.addEventListener('click', () => {
  const modal = document.querySelector('.modal');
  modal.classList.remove('show');
});

// Open the modal

const openBtn = document.querySelector('.open-btn');
openBtn.addEventListener('click', () => {
  const modal = document.querySelector('.modal');
  modal.classList.add('show');
});

// Form validation

const form = document.querySelector('form');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const nameInput = document.getElementById('name').value;
  const emailInput = document.getElementById('email').value;

  if (!nameInput ||!emailInput) {
      alert('Please fill in all fields.');
      return;
  }

  // Add your own validation logic here...

  alert(`Thank you, ${nameInput}! We'll be in touch with you at ${emailInput}.`);
});

// Toggle dark mode

const darkModeToggle = document.querySelector('.dark-mode-toggle');
darkModeToggle.addEventListener('change', (e) => {
  document.body.classList.toggle('dark-mode', e.target.checked);
});

