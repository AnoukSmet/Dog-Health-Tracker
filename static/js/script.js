
$(document).ready(function(){
    /**
    * Set the full month instead of number for the dashboard view 
    */
    var log_month = document.querySelectorAll('#log-month');
    for (let i = 0; i < log_month.length; i++) {
         if (log_month[i].innerText == 01) {
             log_month[i].innerText = "January";
         } else if ((log_month[i].innerText) == 02) {
             log_month[i].innerText = "February";
        } else if ((log_month[i].innerText) == 03) {
             log_month[i].innerText = "March";
        } else if ((log_month[i].innerText) == 04) {
             log_month[i].innerText = "April";
        } else if ((log_month[i].innerText) == 05) {
             log_month[i].innerText = "May";
        } else if ((log_month[i].innerText) == 06) {
             log_month[i].innerText = "June";
        } else if ((log_month[i].innerText) == 07) {
             log_month[i].innerText = "July";
        } else if ((log_month[i].innerText) == 08) {
             log_month[i].innerText = "August";
        } else if ((log_month[i].innerText) == 09) {
             log_month[i].innerText = "September";
        } else if ((log_month[i].innerText) == 10) {
             log_month[i].innerText = "October";
        } else if ((log_month[i].innerText) == 11) {
             log_month[i].innerText = "November";
        } else if ((log_month[i].innerText) == 12) {
             log_month[i].innerText = "December";
        }
    }

    /**
    * Enable datepicker
    */
    var date = new Date();
    var today = date.getFullYear();
    var min = today - 30;
     $('.datepicker').datepicker({
        format: 'yyyy mm dd',
        autoClose: true,
        yearRange: [min, today],
        minDate: new Date('1990,0,13'),
        maxDate: new Date(),
        disableEntry: true 
        
      });

   /**
    * Enable dropdown select box
    */
    $('select').formSelect();
    
    /**
     * Modal to open when user wants to delete dog profile
     */
    $('.modal').modal();
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
   * Function that takes the user back to the previous dashboard 
*/
function goBack() {
  window.history.back();
}

/**
* Prevents manual input 
 */
 $(".datepicker").keydown(function(e){
        e.preventDefault();
    });