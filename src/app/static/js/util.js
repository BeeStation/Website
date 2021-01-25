function updateStats() {
	$.getJSON("/api/stats", function(servers) {
		for (var server_id in servers) {
			var stats = servers[server_id];
			$("#stat-duration-"+server_id).html((new Date).clearTime().addSeconds(stats["round_duration"]).toString('H:mm:ss'));
			$("#stat-players-"+server_id).html(stats["players"]);
			$("#stat-admins-"+server_id).html(stats["admins"]);
			$("#stat-mode-"+server_id).html(stats["mode"]);
			$("#stat-round-"+server_id).html(stats["round_id"]);
			$("#stat-map-"+server_id).html(stats["map_name"]);
		}
	});
}

window.odometerOptions = {
  auto: true,
  selector: '.odometer',
  format: '(,ddd)',
  duration: 2000,
  theme: 'default',
  animation: 'count',
};
