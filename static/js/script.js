/**
 * Function to enable datepicker
 */

 function submitForm(){ 
  document.getElementById('dog-profile-selection').submit(); 
} 

    
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

$('.dropdown-trigger').dropdown({
   coverTrigger: false,
});

function goBack() {
  window.history.back();
}