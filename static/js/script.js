/**
 * Function to enable datepicker
 */

$(document).ready(function(){
    date = $('.datepicker').datepicker({
        format: 'dd mmmm yyyy',
        autoClose: true,
    });
  });

/**
 * Function to enable dropdown select box
 */

    $(document).ready(function(){
    $('select').formSelect();
  });
