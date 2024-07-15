$(document).ready(function(){
    let inputCount = 1;

    $('#addInput').click(function() {
        $('#inputContainer').append('<input type="text" name="name' + inputCount + '" placeholder="Name">');
        inputCount++;
    });
});