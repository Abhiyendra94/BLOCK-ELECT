$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				candidate : $('input[name=candidate]:checked').val(),
				key : $('#message-form1-i').val()
			},
			type : 'POST',
			url : '/vote'
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
