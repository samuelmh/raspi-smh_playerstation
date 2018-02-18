// https://vuejs.org/v2/examples/grid-component.html

var songs_template = `
	<div class="container-fluid ">
		<form class="container">
			<div class="form-group row">
				<div class="col-1">
					<label class="col-form-label font-weight-bold">Search</label>
				</div>
				<div class="col-8 form-inline">
					<input name="query" class="col-11 form-control" v-model="searchQuery" />
					<button v-if="searchQuery" type="button" class="btn btn-light" v-on:click="searchQuery=''"><i class="fa fa-times fa-fw"></i></button>
				</div>

				<div class="col-3">
					<div v-if="searchQuery" >
						<button type="button" class="btn btn-light" v-on:click="encoder_add_songs(filteredSongs)"><i class="fa fa-hdd-o fa-fw"></i></button>
						<button type="button" class="btn btn-light" v-on:click="playlist_add_songs(filteredSongs)"><i class="fa fa-list fa-fw"></i></button>
						<button type="button" class="btn btn-light" v-on:click="player_add_songs(filteredSongs)"><i class="fa fa-play-circle fa-fw"></i></button>
					</div>
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
					<td class="col-1">{{ entry["LENGTH_HMS"] }}</td>
					<td class="col-5 small">{{ entry["PATH"] }}</td>
					<td class="col-1">
						<button type="button" class="btn btn-link" v-on:click="encoder_add_songs([entry])"><i class="fa fa-hdd-o fa-fw"></i></button>
						<button type="button" class="btn btn-link" v-on:click="playlist_add_songs([entry])"><i class="fa fa-list fa-fw"></i></button>
						<button type="button" class="btn btn-link" v-on:click="player_add_songs([entry])"><i class="fa fa-play-circle fa-fw"></i></button>
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
	methods: {
		sortBy: function (key) {
			this.sortKey = key
			this.sortOrders[key] = this.sortOrders[key] * -1
		},
		extract_ids: function(songs){
			return songs.map(
				function(x) {
					return(x['PATH'])
				}
			);
		},
		playlist_add_songs: function(songs){
			this.$emit('playlist_add_songs', this.extract_ids(songs));
		},
		encoder_add_songs: function(songs){
			this.$emit('encoder_add_songs', this.extract_ids(songs));
		},
		player_add_songs: function(songs){
			this.$emit('player_add_songs', this.extract_ids(songs));
		}
	}
});
