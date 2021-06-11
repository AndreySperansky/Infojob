console.log("Hello from employee modals!")

$(function () {
        

          // Read and Delete bookmark buttons open modal with id="modal"
          // The formURL is retrieved from the data of the element
          $(".read-bookmark").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url")});
          });
          
          $(".response").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url")});
              console.log("Hello from response!")
          });
          
          $(".delete-bookmark").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
          });

          // Hide message
          // $(".alert").fadeTo(2000, 500).slideUp(500, function () {
          //     $(".alert").slideUp(500);
          // });
      });