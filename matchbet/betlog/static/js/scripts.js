is_loading = false;

// wait until document has completely loaded
$(document).ready(function(){

    // on scrolling to bottom show load bar
    $(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() == $(document).height() && !is_loading) {
            is_loading = true;
            alert('at bottom');
           $('#table-load-icon').show();
        }
    });

    // if message is not empty then alert user
    if(msg) {
        alert(msg);
    }

    // loop confirmation elements
    $('[data-toggle=confirmation]').confirmation({
        rootSelector: '[data-toggle=confirmation]',
        // other options
    });


    // loop each selector element
    $('.class-selector').each(function(i, obj){

        $( obj ).selectize({
            /* width: "100%" */
        });

    });

    // loop each date picker element
    $('.class-date-picker').each(function(i, obj) {

        console.log('Set date picker ' + i);

        // get date from element - creating date picker clears the value
        objectValue = obj.value;

        $( obj ).bootstrapMaterialDatePicker({
            format:'DD/MM/YY', // format is '28/01/94'
            time: false,
        })

        // assign stored value
        obj.value = objectValue;
    });

    // loop each time picker element
    $('.class-time-picker').each(function(i, obj) {

        console.log('Set time picker ' + i);

        // get element value- creating picker clears the value
        objectValue = obj.value;

        $( obj ).bootstrapMaterialDatePicker({
            format: 'HH:mm',
            date: false,
        })

        // assign stored value
        obj.value = objectValue;

    });

    // on click of row link element
    $('.row-link').click(function(){
        // go to link contained in element
        window.location.href = $(this).attr('updatelink');
    });

});