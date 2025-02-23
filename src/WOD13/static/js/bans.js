window.addEventListener("load", function () {
	window.bans_page = new Vue ({
		el: "#content",

		data: {
			page: 1,
			query: "",

			bans: [],
			loaded_page: null,
			pages: null,

			loaded: false // Have we loaded bans at least once so far?
		},

		mounted: function() {
			this.parse_url();
			this.update_url();
			this.load_bans();
		},

		methods: {
			search_bans(query) {
				this.query = query;
				this.page = 1;
				this.update_url();
				this.load_bans();
			},

			load_bans() {
				this.loaded = false;

				$.getJSON(`${window.api_base_url}/bans?page=${this.page}&search_query=${this.query}`, function(data) {
					this.bans = data.data;
					this.pages = data.pages;
					this.loaded_page = data.page;

					this.loaded = true;
				}.bind(this))
			},

			parse_url() {
				var url = new URL(window.location.href);
				this.page = parseInt(url.searchParams.get("page")) || 1;
				this.query = url.searchParams.get("q") || "";
			},

			update_url() {
				var url = new URL(window.location.href);
				url.searchParams.set("page", this.page);
				url.searchParams.set("q", this.query);
				window.history.replaceState(null, null, url);
			},

			change_page(amount) {
				if(!this.loaded){return;}

				this.page += amount;
				this.page = Math.min(Math.max(this.page, 1), this.pages);
				this.update_url();
				this.load_bans();
			},

			render_dtstring(dtstring) {
				return Date.parse(dtstring).toISOString().split("T").join(" ").slice(0, -5);
			}
		}
	})
})
