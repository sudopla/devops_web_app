$(document).ready(function() {

    //Event for menu
    $('.nav-link').click(function(){

        //Remove/add class active for menu links
        $('.nav-link').removeClass('active');
        $(this).addClass('active');

        //Load page
        link = $(this).attr('data-link');
        $('#page_content').load(link, function(){});

    });

    //Github form submit event
    $(document).on('click', '#gitformsubmit', function(){
        //Create Github repository with Django Project
        project_name = $("#inputFirstName").val();
        project_description = $("#inputDescription").val();
        //Get CSRF token
        csrf_token = $("#gitrepo").find('input[name=csrfmiddlewaretoken]').val();
        //alert(csrf_token);
         $.post( "django_repo/new",
            { repo_name: project_name, repo_description: project_description, csrfmiddlewaretoken: csrf_token },
            function( data ) {
              if (data.result == 'ok'){
                $('#modalGithub p').html('The repository has been created successfully. <br> URL - ' + data.repo_url);
                $('#myModalGihub').modal('show');
                //Clear form values
                $("#inputFirstName").val('');
                $("#inputDescription").val('');
              } else {
                $('#modalGithub p').html(data.message);
                $('#myModalGihub').modal('show');
              }
            },
            "json");

         //Create DataDog event
         $.post( "datadog/new_event",
            { repo_name: project_name, csrfmiddlewaretoken: csrf_token },
            "json");
    });


    //DataDog form submit event
    $(document).on('click', '#datadogformsubmit', function(){
        //Create Github repository with Django Project
        test_name_i = $("#inputFirstName").val();
        test_description_i = $("#inputTestDescription").val();
        location_i = $("#inputLocation").val();
        frequency_i = $("#inputFrequency").val();
        url_i = $("#inputURL").val();
        method_i = $("#inputMethod").val();
        //Get CSRF token
        csrf_token = $("#datadog").find('input[name=csrfmiddlewaretoken]').val();
        $.post( "datadog/new_test",
            { test_name: test_name_i, test_description: test_description_i,
              location: location_i, frequency: frequency_i,
              url: url_i, method: method_i, csrfmiddlewaretoken: csrf_token },
            function( data ) {
              if (data.result == 'ok'){
                $('#myModalDataDogSuccess').modal('show');
                //Clear from values
                $("#inputFirstName").val('');
                $("#inputTestDescription").val('');
                $("#inputURL").val('');
              } else {
                $('#modalDataDogError p').html(data.error);
                $('#myModalDataDogError').modal('show');
              }

            },
            "json");

    });

    //Event for DataDog errro Modal
    $(document).on('click', '.start-over', function(){
        $('#myModalDataDogError').modal('hide');
        //Clear from values
        $("#inputFirstName").val('');
        $("#inputTestDescription").val('');
        $("#inputURL").val('');
    });


});