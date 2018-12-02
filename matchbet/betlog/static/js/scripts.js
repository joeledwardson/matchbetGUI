// false - html attribute to collect when target hidden, true - attribute to collect when shown
toggleMap = {false: "show_prompt", true: "hide_prompt"};

// get html attribute which denotes target to show/hide
function toggle_target( obj ) {
    return $("#" + $( obj ).attr("target_id"));
}

// is object showing
function is_visible( obj ) {
    return !($( obj ).css('display') == 'none' || $( obj ).css("visibility") == "hidden");
}

// set element of class "btn-toggler" value based on if target is shown/hidden
function set_toggler_button( obj, visible ) {
    // get prompt
    newValue = $( obj ).attr( toggleMap[visible] );
    // set value as prompt
    $( obj ).val( newValue );
}

// wait until document has completely loaded
$(document).ready(function(){

    // loop confirmation elements
    $('[data-toggle=confirmation]').confirmation({
        rootSelector: '[data-toggle=confirmation]',
        // other options
    });

//     loop button toggler class elements
//    $('.btn-toggler').each(function(i, obj) {
//        // set text value based on target visibility
//        set_toggler_button( obj, is_visible( toggle_target( obj )));
//    });

    // loop each selector element
    $('.class-selector').each(function(i, obj){

        $( obj ).selectize({
            /* width: "100%" */
        });

//        $( obj ).select2({
//            placeholder: "", // by default display nothing
//            allowClear: $( obj ).hasClass('class-selector-clearable'), // allow clearing selection if has clearable class denoter
//            width: '100%',
//        });
    });

//    $('.class-selector').on('select2:unselecting', function() {
//
//        // user has de-selected option - set custom data value
//        $(this).data('is_deselecting', true);
//
//    }).on('select2:opening', function(e) {
//
//        // dropdown is opening
//        if ($(this).data('is_deselecting')) {
//
//            // action is user de-selecting - reset val
//            $(this).data('is_deselecting', false);
//            // prevent dropdown opening!
//            e.preventDefault();
//        }
//    });


    // loop each date picker element
    $('.class-date-picker').each(function(i, obj) {

        console.log('Set date picker ' + i);

        // get date from element - creating date picker clears the value
        objectValue = obj.value;

//        $( obj ).datepicker({
//            showOn: "both", // pop up on click text box and icon
//            buttonImage: calenderGif, // this must be declared somewhere!
//            buttonImageOnly: true,
//            buttonText: "Select date"
//        }); // create datepicker widget with icon
//
//        $( obj ).datepicker( "option", "dateFormat", "yy-mm-dd" ); // set format


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

//        $( obj ).timepicker({
//            timeFormat: 'HH:mm',
//            interval: 30,
//            dynamic: false,
//            dropdown: true,
//            scrollbar: true
//        });

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

//    // on click of button toggler element
//    $(".btn-toggler").click(function(){
//
//        // get button target
//        objTarget = toggle_target(this);
//
//        // DEBUG - log
//        console.log(objTarget);
//
//        // set value to opposite of current target visibility
//        set_toggler_button( this, !is_visible( objTarget ));
//
//        // toggle target visibility
//        $( objTarget ).toggle();
//    });

});