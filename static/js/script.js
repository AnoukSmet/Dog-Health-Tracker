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



// var current_page = 1;
// var records_per_page = 5;
// var ind_logs = []

// var logs = document.querySelectorAll('.logs');
// for (var i = 0; i < logs.length; i++) {
//         ind_logs.push(logs[i].innerText)
//     }

// var test_logs = ind_logs[0]
// splitStr = test_logs.split(/\s+/)
// var date = splitStr.slice(0,3)
// var activity = splitStr.slice(5,6)
// console.log(logDay[0].innerText)

//      // Can be obtained from another source, such as your objJson variable

// function prevPage()
// {
//     if (current_page > 1) {
//         current_page--;
//         changePage(current_page);
//     }
// }

// function nextPage()
// {
//     if (current_page < numPages()) {
//         current_page++;
//         changePage(current_page);
//     }
// }
    
// function changePage(page)
// {
//     var btn_next = document.getElementById("btn_next");
//     var btn_prev = document.getElementById("btn_prev");
//     var listing_table = document.getElementById("listingTable");
//     // var page_span = document.getElementById("page");
 
//     // Validate page
//     if (page < 1) page = 1;
//     if (page > numPages()) page = numPages();

//     listing_table.innerHTML = "";

//     for (var i = (page-1) * records_per_page; i < (page * records_per_page); i++) {
//         listing_table.innerHTML += 
//         `<div class="container">
//             <div class="row log">
//                 ${ind_logs[i]}
//             </div>
//         </div>`
//         }

//     "<a href = {{logs}}>Click Here</a>";
//     // page_span.innerHTML = page;

//     if (page == 1) {
//         btn_prev.style.visibility = "hidden";
//     } else {
//         btn_prev.style.visibility = "visible";
//     }

//     if (page == numPages()) {
//         btn_next.style.visibility = "hidden";
//     } else {
//         btn_next.style.visibility = "visible";
//     }
// }

// function numPages()
// {
//     return Math.ceil(logs.length / records_per_page);
// }

// window.onload = function() {
//     changePage(1);
// };