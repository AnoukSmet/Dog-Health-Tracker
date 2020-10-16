/**
 * Function to enable datepicker
 */
    
 $(document).ready(function(){
    var date = new Date();
    var today = date.getFullYear();
    var min = today - 30;
     $('.datepicker').datepicker({
        format: 'yyyy mmmm dd',
        autoClose: true,
        yearRange: [min, today],
        minDate: new Date('1990,0,13'),
        maxDate: new Date(),
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
  document.getElementById('dog-profile-selection').submit(); 
} 

/**
 * Function to trigger the dropdown to log out
 */

$('.dropdown-trigger').dropdown({
   coverTrigger: false,
});

/**
 * Function to go back to dashboard 
 * when cancel button add dog is clicked
 */
function goBack() {
  window.history.back();
}
