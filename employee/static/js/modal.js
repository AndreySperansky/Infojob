console.log("Hello from employee modals!")

$(function () {
        

          // Read and Delete bookmark buttons open modal with id="modal"
          // The formURL is retrieved from the data of the element
          $(".read-bookmark").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url")});
          });
          
          $(".response-cv").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url")});
          });
          
          $(".delete-bookmark").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
          });
          
          $(".delete-response").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
          });
          
          // Filter button
          $("#filter-book").each(function () {
              $(this).modalForm({formURL: $(this).data("form-url")});
          });

          // Hide message
          // $(".alert").fadeTo(2000, 500).slideUp(500, function () {
          //     $(".alert").slideUp(500);
          // });
      });