window.addEventListener("load", function () {
	window.book_page = new Vue ({
		el: "#content",

		data: {
			book: null
		},

		mounted: function() {
			this.load_book();
		},

		methods: {
			load_book() {
				$.getJSON(`${window.api_base_url}/library/${book_id}`, function(data) {
					this.book = data;
				}.bind(this))
			}
		}
	})
})
