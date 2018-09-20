$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				key : $('#message-form1-k').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#successAlert').hide();
				$('#errorAlert').text(data.error).show();
			}
			else {
				$('#successAlert').text(data.success).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});