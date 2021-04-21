// Рабочий варант - заменяет текст внутри кнопки и количество лайков

console.log('Hello!')


$(document).ready(function(){

    $('.cv_list').on('click', '#bookmark', function(e){
        e.preventDefault()
        console.log('works!')
        
        let current = $(this)
        const id = current.data('id')
        console.log(id)

        const button = $(`.like-btn${id}`)
        console.log(button)

        const cls = button.attr('class')
        console.log(cls)

        // const url = $(this).attr('action')
        // console.log(url)
        
        



        $.ajax({
            type: 'POST',
            url: "/employer/cv/bookmark/" + id ,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'pk': id,
            },

            success: function(response) {
                console.log('success', response)
                let res = response['res'];
                console.log(res)
                if(res === 'false') {
                    $(`.like-btn${id}`).toggleClass('btn-danger btn-outline-danger')

                } else {
                    $(`.like-btn${id}`).toggleClass('btn-outline-danger btn-danger')

                }

            },

            error: function(response) {
                console.log('error', response)
            }
        })
        
        
        
    });

});

