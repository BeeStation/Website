window.addEventListener("load", function () {
	window.stats_page = new Vue ({
		el: "#content",

		data: {
			servers: [],
			server_stats: {}
		},

		mounted: function() {
			$.getJSON(`${window.api_base_url}/servers`, function(data) {
				window.stats_page.servers = data;
			})

			load_server_stats_loop();
		}
	})

})

function load_server_stats_loop() {
	$.getJSON(`${window.api_base_url}/stats`, function(data) {
		window.stats_page.server_stats = data;
	})
	setTimeout(load_server_stats_loop, 5000)
}
