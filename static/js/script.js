/**
 * Function to enable datepicker
 */

 $(document).ready(function(){
     $('.datepicker').datepicker({
          format: 'dd mmmm yyyy',
          autoClose: true,
      });
   })

/**
 * Function to enable dropdown select box
 */

    $(document).ready(function(){
    $('select').formSelect();
  });

  $(".dropdown-trigger").dropdown({
      coverTrigger: false,
  });

 $(document).ready(function(){
    $('.tabs').tabs();
  });