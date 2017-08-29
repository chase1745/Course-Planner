$(document).ready(function() {
    newTimepicker();

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
    //    Adding schedule   //
    //////////////////////////
    var maxschedule = 8;
    $('body').on('click', '.btn-add-sec', function(e) {
        e.preventDefault();
        var num_schedule = parseInt($(this).prevAll(".course-info").find(".num-schedule").val());
        num_schedule++;
        if (num_schedule <= maxschedule) {
            $("#sec-template").clone().insertBefore($(this)).removeAttr('id').show();
            $(this).prevAll(".course-info").find(".num-schedule").val(num_schedule);
        } else {
            $(this).next(".max-reached").remove();
            $(this).after("<p class='max-reached'>Maximum of 8 schedule per course.</p>");
        }
        newTimepicker();
    });

    //////////////////////////
    //   Removing schedule  //
    //////////////////////////
    $('body').on('click', '.btn-delete-sec', function(e) {
        e.preventDefault();
        var num_schedule = parseInt($(this).parent().siblings(".course-info").find(".num-schedule").val());
        num_schedule--;
        $(this).parent().siblings(".course-info").find(".num-schedule").val(num_schedule);
        $(this).parents('.sec-info').remove();
    });

    //////////////////////////
    //    Adding Courses    //
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
            $(".input-wrapper:last label.course-count").html("Class "+numCourses+":");
            $(".input-wrapper:last input[type=hidden]").attr('id', numCourses);
            $(".input-wrapper:last").show();
        } else {
            $(this).next(".max-reached").remove();
            $(this).after("<p class='max-reached'>Maximum of 8 courses.</p>");
        }
        newTimepicker();
    });

    //////////////////////////
    //   Removing Courses   //
    //////////////////////////
    $('body').on('click', '.btn-delete-course', function(e) {
        e.preventDefault();
        $(this).parents('.input-wrapper').remove();
        numCourses--;
    });

    //////////////////////////
    //         OUTPUT       //
    //////////////////////////
    var tabs = $('.tab');
    var schedule = $('.schedule');
    // Make first schedule selected
    tabs.eq(0).addClass('selected');
    schedule.eq(0).css('display', 'table');

    tabs.click(function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
        var index = $(this).index();
        schedule.each( function() { $(this).css('display', 'none'); });
        schedule.eq(index).css('display', 'table');
    });
});

//////////////////////////
//   Timepicker funcs.  //
//////////////////////////
function newTimepicker() {
    var timeStart = $(".start-time");
    var timeFinish = $(".finish-time");

    timeStart.each(function () {
        $(this).timepicker({
            'minTime': '7:00am',
            'maxTime': '10:00pm',
            'timeFormat': 'g:ia',
            'step': 15
        });
    });
    timeFinish.each(function () {
        $(this).timepicker({
            'minTime': '8:00am',
            'maxTime': '11:00pm',
            'timeFormat': 'g:ia',
            'step': 15
        });
    });
    $(".input-wrapper").on('change', ".start-time", function () {
        $(".finish-time").timepicker('option', 'minTime', $(this).val());
    });
}
