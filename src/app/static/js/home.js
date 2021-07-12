window.addEventListener("load", function () {
	window.home_page = new Vue ({
		el: "#content",

		data: {
			server_totals: {},
			budget: {}
		},

		mounted: function() {
			$.getJSON(`${window.api_base_url}/budget`, function(data) {
				window.home_page.budget = data;
			})

			load_server_totals_loop();
		}
	})

})

function load_server_totals_loop() {
	$.getJSON(`${window.api_base_url}/stats/totals`, function(data) {
		window.home_page.server_totals = data;
	})
	setTimeout(load_server_totals_loop, 10000)
}