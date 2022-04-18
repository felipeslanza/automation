$(document).ready(function () {
	// ++++++++++++++
	// Click handlers
	// ++++++++++++++
	$("#signup-button").click(function () {
		$("#signup-box").removeClass("hidden");
		$("#initial-box").addClass("hidden");
	});

	$("#login-button").click(function () {
		$("#login-box").removeClass("hidden");
		$("#initial-box").addClass("hidden");
	});

	$("#back-button").click(function () {
		load_initial_view();
	});

	$("#display-selection-button").click(function () {
		load_selection_view();
	});

	$("#pokemon-back-button").click(function () {
		$("#pokemon-box").addClass("hidden");
		load_trainer_view();
	});

	$("#logout-button").click(function () {
		localStorage.removeItem("pokemon_api_token");
		load_initial_view();
	});

	$("#signup-submit").click(function () {
		let form = $("#signup-box form")[0];
		let formData = {
			name: form.name.value,
			email: form.email.value,
			password: form.password.value,
			birthday: form.birthday.value,
		};

		if (
				formData.name &&
				formData.email &&
				formData.password &&
				formData.birthday
		) {
			formData = JSON.stringify(formData);
		} else {
			alert("All fields are required!");
			load_initial_view()
		}

		let pwd1 = form.password.value;
		let pwd2 = form.password2.value;
		if (pwd1 != pwd2) {
			alert("Passwords must match!");
			return;
		}

		$.ajax({
			type: "POST",
			url: "api/trainer",
			data: formData,
			dataType: "json",
			contentType: "application/json; charset=utf-8",
			error: function (e) {
				console.log("Failed to create new trainer");
				console.error(e);
				load_initial_view(); // Reset
			},
		}).done(function (res) {
			let token = res["token"];
			localStorage.setItem("pokemon_api_token", token);

			$("#signup-box").addClass("hidden");
			load_trainer_view();
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
				alert("Invalid credentials");
				load_initial_view();
			},
		}).done(function (res) {
			let token = res["token"];
			localStorage.setItem("pokemon_api_token", token);

			$("#login-box").addClass("hidden");
			load_trainer_view();
		});
	});

	$("#selection-submit").click(function () {
		let checked = $('input[name="radio-answer"]:checked');
		if (!checked.length) {
			alert("Must select one option to continue");
			return;
		}

		let token = localStorage.getItem("pokemon_api_token");
		let species_id = checked[0].id;
		let formData = JSON.stringify({ selected_species_id: species_id });

		$.ajax({
			type: "POST",
			url: "api/initials-pokemon/choose",
			headers: { Authorization: `Bearer ${token}` },
			data: formData,
			dataType: "json",
			contentType: "application/json; charset=utf-8",
			error: function (e) {
				console.error(e);
			},
		}).done(function (res) {
			$("#pokemon-box").addClass("hidden");
			load_trainer_view();
		});
	});

	// ++++++++++++++
	// View handlers
	// ++++++++++++++
	function load_initial_view() {
		$("#login-box").addClass("hidden");
		$("#signup-box").addClass("hidden");
		$("#trainer-box").addClass("hidden");
		$("#initial-box").removeClass("hidden");
	}

	function load_trainer_view() {
		$("#trainer-box").removeClass("hidden");
		let token = localStorage.getItem("pokemon_api_token");

		$.ajax({
			type: "GET",
			url: "api/trainer",
			contentType: "application/json; charset=utf-8",
			headers: { Authorization: `Bearer ${token}` },
			error: function (e) {
				console.error(e);
			},
		}).done(function (user) {
			$("#trainer-display").empty();
			$("#trainer-display").append([
				`<p><strong>Treinador: </strong>${user.name}</p>`,
				`<p><strong>Email: </strong>${user.email}</p>`,
				`<p><strong>Pokemon: </strong>${user.pokemon_name || "-"}</p>`,
			]);
			if (!!user.pokemon_id) $("#display-selection-button").addClass("hidden");
			else $("#display-selection-button").removeClass("hidden");
		});
	}

	function load_selection_view() {
		$("#trainer-box").addClass("hidden");
		$("#pokemon-box").removeClass("hidden");
		let token = localStorage.getItem("pokemon_api_token");

		$.ajax({
			type: "GET",
			url: "api/initials-pokemon",
			headers: { Authorization: `Bearer ${token}` },
			error: function (e) {
				console.error(e);
			},
		}).done(function (rotation_arr) {
			// NOTE: Order must match `server.config.POKEMON_ALLOWED_STARTING_TYPES`
			const types = ["Fire", "Grass", "Water"];

			$("#rotation-display").empty();
			for (let i = 0; i < types.length; i++) {
				let label = types[i];
				let [id, pokemon] = rotation_arr[i];

				$("#rotation-display").append([
					`<input id=${id} type="radio" name="radio-answer">`,
					`<label for=${id}><strong>${label}:</strong> ${pokemon}</label><br/>`,
				]);
			}
		});
	}
});
