window.addEventListener("load", function () {
	window.library_page = new Vue ({
		el: "#content",

		data: {
			page: 1,

			books: [],
			loaded_page: null,
			pages: null,

			loaded: false // Have we loaded books at least once so far?
		},

		mounted: function() {
			this.parse_url();
			this.update_url();
			this.load_books();
		},

		methods: {
			load_books() {
				this.loaded = false;

				$.getJSON(`${window.api_base_url}/library?page=${this.page}`, function(data) {
					this.books = data.data;
					this.pages = data.pages;
					this.loaded_page = data.page;

					this.loaded = true;
				}.bind(this))
			},

			parse_url() {
				var url = new URL(window.location.href);
				this.page = parseInt(url.searchParams.get("page")) || 1;
			},

			update_url() {
				var url = new URL(window.location.href);
				url.searchParams.set("page", this.page);
				window.history.replaceState(null, null, url);
			},

			change_page(amount) {
				if(!this.loaded){return;}

				this.page += amount;
				this.page = Math.min(Math.max(this.page, 1), this.pages);
				this.update_url();
				this.load_books();
			},

			open_book(book_id) {
				window.location = `/library/${book_id}`
			}
		}
	})
})
