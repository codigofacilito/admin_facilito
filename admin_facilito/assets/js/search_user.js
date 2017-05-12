$(document).ready(function(){

  $("#search-user-form").submit(function(e){
    e.preventDefault();

    $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data : $(this).serialize(),

      success: function(json){ //json es la respuesta del servidor
        var html = "";
        var link = window.location.pathname + "add/"

        for(let elem of json){
          var href = link + elem.username + "/"
          html+= '<li>' + elem.username + '<a href="'+ href +'">agregar</a> </li>'
        }

        $('#ajax-result ul').empty();
        $('#ajax-result ul').append(html);

      }

    })

  });

})