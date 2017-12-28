// https://vuejs.org/v2/examples/grid-component.html

var songs_template = `
	<div class="container-fluid ">
		<form class="container">
			<div class="form-group row">
				<div class="col-1">
					<label class="col-form-label font-weight-bold">Search</label>
				</div>
				<div class="col-10">
					<input name="query" class="form-control" v-model="searchQuery" />
				</div>
				<div class="col-1">
						<button class="btn btn-light" v-if="searchQuery" v-on:click="searchQuery=''"><i class="fa fa-times fa-fw"></i></button>
				</div>
			</div>
		</form>
		<table class="table">
			<thead>
				<tr class="row" >
					<th v-for="key in columns" :class="{ 'col-5':key=='TITLE' || key=='PATH', 'col-1':key=='LENGTH' }" >
						<button type="button" v-on:click="sortBy(key)" class="btn" :class="{ 'btn-secondary': sortKey == key,  'btn-link': sortKey != key}">
							{{ key }}
							<span class="fa fa-fw" :class="sortOrders[key] > 0 ? 'fa-sort-asc' : 'fa-sort-desc'"></span>
						</button>
					</th>
					<th class="col-1"><!-- Actions --></th>
				</tr>
			</thead>
			<tbody>
				<tr class="row" v-for="entry in filteredSongs">
					<td class="col-5">{{ entry["TITLE"] }}</td>
					<td class="col-1">{{ entry["LENGTH"] | duration }}</td>
					<td class="col-5 small">{{ entry["PATH"] }}</td>
					<td class="col-1">
						<button type="button" class="btn btn-link" v-on:click="playlist_add_song(entry['PATH'])"><i class="fa fa-list fa-fw"></i></button>
						<button type="button" class="btn btn-link" v-on:click="player_add_song(entry['PATH'])"><i class="fa fa-play-circle fa-fw"></i></button>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
`;


Vue.component('smh-playerstation-songs', {
  template: songs_template,
	data: function () {
		var sortOrders = {};
		var columns = ['TITLE','LENGTH', 'PATH']
		columns.forEach(function (key) {
			sortOrders[key] = 1
		})
		return {
			sortKey: '',
			sortOrders: sortOrders,
			searchQuery: '',
			columns: columns
		}
	},
	props: ['songs'],

	computed: {
		filteredSongs: function () {
			var sortKey = this.sortKey
			var searchQuery = this.searchQuery && this.searchQuery.toLowerCase()
			var order = this.sortOrders[sortKey] || 1
			var songs = this.songs
			if (searchQuery) {
				songs = songs.filter(function (row) {
					return Object.keys(row).some(function (key) {
						return String(row[key]).toLowerCase().indexOf(searchQuery) > -1
					})
				})
			}
			if (sortKey) {
				songs = songs.slice().sort(function (a, b) {
					a = a[sortKey]
					b = b[sortKey]
					return (a === b ? 0 : a > b ? 1 : -1) * order
				})
			}
			return songs
		}
	},
	filters: {
		duration: function (seconds){
			function pad(num, size){ return ('00' + num).substr(-size); }
			seconds = Number(seconds)
			return Math.floor(seconds/3600) + ":" + pad(Math.floor((seconds%3600)/60),2) + ":" + pad(Math.floor(seconds%60),2)
		}
	},
	methods: {
		sortBy: function (key) {
			this.sortKey = key
			this.sortOrders[key] = this.sortOrders[key] * -1
		},
		playlist_add_song: function(song_id){
			this.$emit('playlist_add_song', song_id);
		},
		player_add_song: function(song_id){
			this.$emit('player_add_songs', [song_id]);
		}
	}
});