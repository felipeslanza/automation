$(document).ready(function () {
	$("#signup-button").click(function () {
		$("#signup-box").removeClass("hidden");
		$("#initial-box").addClass("hidden");
	});

	$("#login-button").click(function () {
		$("#login-box").removeClass("hidden");
		$("#initial-box").addClass("hidden");
	});

	$("#back-button").click(function () {
		$("#login-box").addClass("hidden");
		$("#signup-box").addClass("hidden");
		$("#initial-box").removeClass("hidden");
	});

	$("#signup-submit").click(function () {
		let form = $("#signup-box form")[0];
		let pwd1 = form.password.value;
		let pwd2 = form.password2.value;
		if (pwd1 != pwd2) {
			alert("Passwords must match!");
			return;
		}
		let formData = JSON.stringify({
			name: form.name.value,
			email: form.email.value,
			password: form.password.value,
			birthday: form.birthday.value,
		});

		$.ajax({
			type: "POST",
			url: "api/trainer",
			data: formData,
			dataType: "json",
			contentType: "application/json; charset=utf-8",
			error: function (e) {
				console.log("Failed to create new trainer")
				console.error(e);
			},
		}).done(function(res) {
			console.log("Success");

			let token = res["token"];
			localStorage.setItem("pokemon_api_token", token)

			$("#signup-box").addClass("hidden");
			$("#trainer-box").removeClass("hidden");
		});
	});

	$("#login-submit").click(function () {
		let form = $("#login-box form")[0];
		let formData = JSON.stringify({
			email: form.email.value,
			password: form.password.value,
		});

		$.ajax({
			type: "POST",
			url: "api/login",
			data: formData,
			dataType: "json",
			contentType: "application/json; charset=utf-8",
			error: function (e) {
				console.error(e);
			},
		});
	});
});
