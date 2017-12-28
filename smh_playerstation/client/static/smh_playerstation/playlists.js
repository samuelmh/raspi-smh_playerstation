var playlists_template = `
<div class="container-fluid ">
	<ul class="list-group list-group-flush">
		<li class="list-group-item" v-for="(songs, id) in playlists" >
			<div class="row">
				<button class="btn btn-light col-9" v-on:click="playlist_set_selected(id)">{{ id }}</button>
				<div class="col-3">
					<button type="button" class="btn btn-light"><i class="fa fa-hdd-o fa-fw"></i></button>
					<button type="button" class="btn btn-light" v-on:click="player_add_songs_playlist(id)"><i class="fa fa-play-circle fa-fw"></i></button>
				</div>
			</div>
			<br/>

			<div v-bind:class="{ 'collapse': playlist_selected_id!=id}">
				<form>
					<div class="form-row">
						<div class="col-10">
							<input type="text" class="form-control" v-model="id" name="id">
						</div>
						<div class="col-2">
							<button type="button" class="btn btn-success" v-on:click="playlist_upsert(id)"><i class="fa fa-floppy-o"> Save</i></button>
							<button type="button" class="btn btn-danger" v-on:click="playlist_delete()"><i class="fa fa-trash"></i> Delete</button>
						</div>
					</div>
				</form>

				<ul class="list-group container-fluid list-group-flush" >
					<draggable :list="songs" :options="{handle:'.drag-handle'}">
						<li class="list-group-item" v-for="(song, index) in songs">
							<div class="row">
								<div class="col-1 drag-handle">
									<i class="fa fa-arrows-v fa-fw"></i>
								</div>
								<div class="col-9">
									{{ song }}
								</div>
								<div class="col-2">
									<button type="button" class="btn btn-link" v-on:click="remove_song(index)"><i class="fa fa-remove fa-fw"></i></button>
									<button type="button" class="btn btn-link"><i class="fa fa-hdd-o fa-fw"></i></button>
									<button type="button" class="btn btn-link" v-on:click="player_add_song(song)"><i class="fa fa-play-circle fa-fw"></i></button>
								</div>
							</div>
						</li>
					</draggable>
				</ul>
			</div>
		</li>
	</ul>
</div>
`;


Vue.component('smh-playerstation-playlists', {
  template: playlists_template,
	props: ['playlists', 'playlist_selected_id'],
	methods: {
		playlist_set_selected: function(playlist_id){
			this.$emit('playlist_set_selected', playlist_id);
		},
		playlist_upsert: function(playlist_id){
			this.$emit('playlist_upsert', playlist_id);
		},
		playlist_delete: function(){
			this.$emit('playlist_delete');
		},
		remove_song: function(song_index){
			this.$emit('playlist_remove_song', song_index);
		},
		player_add_song: function(song_id){
			this.$emit('player_add_songs', [song_id]);
		},
		player_add_songs_playlist: function(playlist_id){
			this.$emit('player_add_songs', this.playlists[playlist_id]);
		}
	}
});
