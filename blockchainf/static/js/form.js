$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				aadhar:$('#name-header15-2').val(),
				name : $('#name-header15-3').val(),
				age : $('#Age-header15-3').val(),
				gender : $('#Gender-header15-3').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.success).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
