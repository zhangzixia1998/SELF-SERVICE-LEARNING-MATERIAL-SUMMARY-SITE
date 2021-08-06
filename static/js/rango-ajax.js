$(document).ready(function(){
    $('.likes').click(function() {
        var pageIdVar;
        pageIdVar = $(this).attr('data-pageid');
        
        
        $.get('/rango/like_page/', {'page_id': pageIdVar},
        function(data) {
            $("#likes"+pageIdVar).html(data);
        })
    });
    $('.dislikes').click(function() {
        var pageIdVar;
        pageIdVar = $(this).attr('data-pageid');
        $.get('/rango/dislike_page/', {'page_id': pageIdVar},
        function(data) {
            $("#dislikes"+pageIdVar).html(data);
        })
    });
    

}
)

