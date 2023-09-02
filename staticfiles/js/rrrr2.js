$("#numero").change(function(){
   
    var numeroCnib= $(this).val();
    $.ajax({
        type: "POST",
        url: "{% url 'add-donneur' collects.pk %}",
        data: {
            'numero_cnib': numeroCnib
        },
        success: function(data) {
            $("#nom").html(data);
        }
    });
});