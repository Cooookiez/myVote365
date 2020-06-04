console.log('hello from update callback')

function show_responses_from_post(response_raw){
    //clear previous callback(s)
    $('p.callback').each(function(){
        $(this).text('');
    });
    // write callback
    var response_json = JSON.parse(response_raw)
    var responses_count = Object.keys(response_json).length
    console.log(response_json)
    $('#'+place).attr('data-callback-type', type).text(msg)
    for( i = 0; i < responses_count; i++ ){
        var place = response_json[i].place;
        var type = response_json[i].type;
        var msg = response_json[i].msg;
        $('#'+place).attr({
            'data-callback-type': type,
            'data-show': 'True'
        }).text(msg)
        if( type == 'success' ){
            weit_and_hide_main_alert(place);
            if( place == 'callback-user-settings-password-submit' ){
                $('#user-settings-password-new-password-1').val('');
                $('#user-settings-password-new-password-2').val('');
            }
        }
    }
}

function weit_and_hide_main_alert(place){
    setTimeout(function(){
        $('#'+place).attr('data-show', 'False')
    }, 2000);
}