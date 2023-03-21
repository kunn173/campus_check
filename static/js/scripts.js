const starInputs = document.querySelectorAll('.star-rating input[type="radio"]');

const handleStarSelect = (input) => {
  const inputs = Array.from(starInputs);
  const index = inputs.indexOf(input);

  inputs.forEach((input, i) => {
    const star = input.nextElementSibling;
    if (i <= index) {
      star.style.color = "#f7d000"; // change color to yellow
    } else {
      star.style.color = "#0b0202"; // reset color to black
    }
  });
};

starInputs.forEach((input) => {
  input.addEventListener('mouseover', (event) => {
    handleStarSelect(event.target);
  });
  input.addEventListener('mouseout', () => {
    handleStarSelect(null);
  });
});

const form = document.querySelector('.rate-form');
const confirmBox = document.getElementById('confirm-box');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const formValues = Object.fromEntries(formData.entries());
  console.log(formValues);
  confirmBox.innerHTML = 'Review submitted!';
});