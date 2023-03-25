let valueForMoneyStars = document.querySelectorAll('.my-star.star-value-for-money');
valueForMoneyStars.forEach(function(star) {
    star.addEventListener('click', function() {
    let rating = parseInt(this.getAttribute("data-star"));
    let inputField = document.querySelector('#id_value_for_money');
    inputField.value = rating;
    for(let i=1; i<=5; i++) {
      let starClass = document.querySelectorAll('.my-star.star-value-for-money.star-'+i)[0].classList;
      if (i <= rating) {
        if (!starClass.contains('is-active')) {
          starClass.add('is-active');
        }
      } else {
        if (starClass.contains('is-active')) {
          starClass.remove('is-active');
        }
      }
    }
  });
});


let teaching_quality_stars = document.querySelectorAll('.my-star.star-teaching-quality');
teaching_quality_stars.forEach(function(star) {
  star.addEventListener('click', function() {
    let rating = parseInt(this.getAttribute("data-star"));
    let inputField = document.querySelector('#id_teaching_quality');
    inputField.value = rating;
    for(let i=1; i<=5; i++) {
      let starClass = document.querySelectorAll('.my-star.star-teaching-quality.star-'+i)[0].classList;
      if (i <= rating) {
        if (!starClass.contains('is-active')) {
          starClass.add('is-active');
        }
      } else {
        if (starClass.contains('is-active')) {
          starClass.remove('is-active');
        }
      }
    }
  });
});

let course_contentStars = document.querySelectorAll('.my-star.star-course-content');
course_contentStars.forEach(function(star) {
  star.addEventListener('click', function() {
    let rating = parseInt(this.getAttribute("data-star"));
    let inputField = document.querySelector('#id_course_content');
    inputField.value = rating;
    for(let i=1; i<=5; i++) {
      let starClass = document.querySelectorAll('.my-star.star-course-content.star-'+i)[0].classList;
      if (i <= rating) {
        if (!starClass.contains('is-active')) {
          starClass.add('is-active');
        }
      } else {
        if (starClass.contains('is-active')) {
          starClass.remove('is-active');
        }
      }
    }
  });
});

let job_prospects_stars = document.querySelectorAll('.my-star.star-job-prospects');
job_prospects_stars.forEach(function(star) {
  star.addEventListener('click', function() {
    let rating = parseInt(this.getAttribute("data-star"));
    let inputField = document.querySelector('#id_job_prospects');
    inputField.value = rating;
    for(let i=1; i<=5; i++) {
      let starClass = document.querySelectorAll('.my-star.star-job-prospects.star-'+i)[0].classList;
      if (i <= rating) {
        if (!starClass.contains('is-active')) {
          starClass.add('is-active');
        }
      } else {
        if (starClass.contains('is-active')) {
          starClass.remove('is-active');
        }
      }
    }
  });
});

