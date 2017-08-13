$(document).ready(function() {
    var timeStart = $(".start-time");
    var timeFinish = $(".finish-time");

    //////////////////////////
    //   Timepicker funcs.  //
    //////////////////////////
    timeStart.each( function(){
        $(this).timepicker({
            'minTime': '7:00am',
            'maxTime': '10:00pm',
            'timeFormat': 'g:ia',
            'step': 15,
        });
    });
    timeFinish.each( function(){
        $(this).timepicker({
            'minTime': '8:00am',
            'maxTime': '11:00pm',
            'timeFormat': 'g:ia',
            'step': 15
        });
    });
    $(".input-wrapper").on('change', ".start-time", function() {
        $(".finish-time").timepicker('option', 'minTime', $(this).val());
    });

    //////////////////////////
    //  Parsing checkboxes  //
    //////////////////////////
    $("form").submit(function () {
        var this_master = $(this);

        this_master.find('input[type="checkbox"]').each( function () {
            var checkbox_this = $(this);
            if( checkbox_this.is(":checked") == true ) {
                checkbox_this.attr('value','1');
            } else {
                checkbox_this.prop('checked',true);
                checkbox_this.attr('value','0');
            }
        });

        // remove templates as to not get their values in back-end
        $("#sec-template").remove();
        $("#course-template").remove();
    });    

    //////////////////////////
    //    Adding Sections   //
    //////////////////////////
    var maxSections = 8;
    $('body').on('click', '.btn-add-sec', function(e) {
        e.preventDefault();
        var num_sections = parseInt($(this).prevAll(".course-info").find(".num-sections").val());
        num_sections++;
        if (num_sections <= maxSections) {
            $("#sec-template").clone().insertBefore($(this)).removeAttr('id').show();
            $(this).prevAll(".course-info").find(".num-sections").val(num_sections);
        } else {
            $(this).next(".max-reached").remove();
            $(this).after("<p class='max-reached'>Maximum of 8 sections per course.</p>");
        }
    });
    
    //////////////////////////
    //    Adding Courses   //
    //////////////////////////
    var numCourses = 3;  // start out with 3
    var wrapper     = $('#course-template');
    var add_button  = $('.btn-add-course');
    var maxCourses = 8; // TODO: change

    $(add_button).click(function(e) {
        e.preventDefault();
        if (numCourses < maxCourses) {
            numCourses++;
            $("#course-template").clone().removeAttr('id').insertAfter('.input-wrapper:last');
            $(".input-wrapper:last label.course-count").html("Class "+numCourses);
            $(".input-wrapper:last input[type=hidden]").attr('id', numCourses);
            $(".input-wrapper:last").show();
        } else {
            $(this).next(".max-reached").remove();
            $(this).after("<p class='max-reached'>Maximum of 8 courses.</p>");
        }
    });
});
