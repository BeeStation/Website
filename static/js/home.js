function updateHomeStats() {
	$.getJSON("/api/stats/totals", function(json) {
			$("#stat-total-players").html(json["total_players"]);
			$("#stat-total-connections").html(json["total_connections"]);
			$("#stat-total-rounds").html(json["total_rounds"]);
	});
}


function updateBudgetInfo() {
	$.getJSON("/api/budget", function(json) {
			$(".progress-raised").html("$"+json["income"]+" / $"+json["goal"]);
			$(".progress-bar").css("width", json["percent"]+"%")
	});
}

window.onload = function WindowLoad(event) {
	updateBudgetInfo()
	updateHomeStats()
	window.setInterval(updateHomeStats, 10000)
  }