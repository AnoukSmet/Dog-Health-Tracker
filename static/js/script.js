/**
 * Displays request format when incorrect input was given
 */

// const username = document.querySelector('#username');
// const password = document.querySelector('#password');

// username.oninvalid = function(event) {
//     event.target.setCustomValidity('Username should only have letters (either case) and numbers. No special characters');
// }

// password.oninvalid = function(event) {
//     event.target.setCustomValidity('Password should have six or more characters');
// }


/**
 * Function to enable datepicker
 */
    
 $(document).ready(function(){
    var date = new Date();
    var today = date.getFullYear();
    var min = today - 30;
     $('.datepicker').datepicker({
        format: 'yyyy mmmm dd',
        autoClose: false,
        yearRange: [min, today],
        minDate: new Date('1990,0,13'),
        maxDate: new Date(),
        defaultDate: date,
        setDefaultDate: true
      });
   })

/**
 * Function to enable dropdown select box
 */


$(document).ready(function(){
    $('select').formSelect();
});

/**
 * Function to submit selected profile without submit button 
 */
 function submitForm(){ 
  document.querySelector('#dog-profile-selection').submit(); 
} 

/**
 * Function to trigger the dropdown to log out
 */

$('.dropdown-trigger').dropdown({
   coverTrigger: false,
});

/**
 * Modal to open when user wants to delete dog profile
 */

 $(document).ready(function(){
    $('.modal').modal();
  });
