// Root instance

var smh_playerstation = new Vue({
	el: '#smh_playerstation',
	data: {
	    url_api: 'http://localhost:8000'+'/api/v1.0',
			playlists: [],
			playlist_selected_id: "tmp",
	    songs: [],  //Tuples of songs
			songs_index: {},  // Index over the songs titles
			player: {mode:'LIST', playlist:[]}  // Don't bind an empty playlist
	  },
  methods: {

		//==> SONG Utilities
		song_filter_title: function(path_file){
  		var elems = path_file.split("/").pop().split("-");
  		elems.pop();
  		return elems.join();
    },


    //
    //==> SONGS
    //
		songs_get: function(){
      var self = this;
      axios.get(self.url_api+'/songs')
        .then(function (response) {
					console.log("OK: songs_get");
          self.songs_index = {};
          self.songs = Object.keys(response.data).map(
            function(key){
              response.data[key]['TITLE'] = self.song_filter_title(response.data[key]['PATH']);
              self.songs_index[key] = response.data[key];
              return response.data[key];
            }
          );
        })
        .catch(function (error) {
          console.log("ERROR: get_songs");
          console.log(error);
        });
    },


    //
    //==> PLAYLISTS
    //
		playlists_get: function(){
			var self = this;
			axios.get(self.url_api+'/playlists')
				.then(function (response) {
					console.log("OK: playlists_get");
					self.playlists = response.data;
					self.playlist_selected_id = 'tmp';
					// Create temporal playlist
					if (!self.playlists['tmp']){
						Vue.set(self.playlists, 'tmp', []);  // Reactivity
					}
				})
				.catch(function (error) {
					console.log("ERROR: get_playlists");
					console.log(error);
				});
		},
		playlist_delete: function(){
			var self = this;
			var id =  self.playlist_selected_id;
			console.log("delete_playlist "+id);
			axios.delete(self.url_api+'/playlists/'+id)
				.then(function (response) {
						console.log("OK: delete_playlist");
						Vue.delete(self.playlists, id);  // Reactivity
						if (id=="tmp"){
							Vue.set(self.playlists, 'tmp', []);  // Reactivity
						}
				})
				.catch(function (error) {
					console.log("ERROR: delete_playlist");
					console.log(error);
				});
		},
		playlist_upsert: function(playlist_id){
			var self = this;
			var songs = self.playlists[self.playlist_selected_id];
			axios.post(self.url_api+'/playlists/'+playlist_id, {songs: songs})
				.then(function (response) {
					console.log("OK: upsert_playlist "+playlist_id);
					Vue.set(self.playlists, playlist_id, songs);  //Changes in DOM
					self.playlist_selected_id = playlist_id;  //Move to new playlist
				})
				.catch(function (error) {
					console.log("ERROR: upsert_playlist");
					console.log(error);
				});
		},
		playlist_set_selected: function(playlist_id){
			this.playlist_selected_id = playlist_id;
		},
		playlist_remove_song: function(song_index){
			Vue.delete(this.playlists[this.playlist_selected_id], song_index);
		},
		playlist_add_song: function(song_id){
			this.playlists[this.playlist_selected_id].push(song_id);
		},


		//
		//==> PLAYER
		//
		player_get: function(){
	    var self = this;
	    axios.get(self.url_api+'/player')
	      .then(function (response) {
	        console.log("OK: player_get");
	        self.player = response.data;
	      })
	      .catch(function (error) {
	        console.log("ERROR: player_get");
	        console.log(error);
	      });
		},
		player_playlist_upsert: function(){
	    var self = this;
	    axios.put(self.url_api+'/player/playlist', {song_ids: this.player.playlist})
	      .then(function (response) {
	        console.log("OK: player_playlist_upsert");
	      })
	      .catch(function (error) {
	        console.log("ERROR: player_playlist_upsert");
	        console.log(error);
	      });
		},
		player_remove_song: function(song_index){
			Vue.delete(this.player.playlist, song_index);
			this.player_playlist_upsert();
		},
		player_add_songs: function(song_ids){
			this.player.playlist = this.player.playlist.concat(song_ids);
			this.player_playlist_upsert();
		},
		player_action: function(action){
	    var self = this;
	    axios.post(self.url_api+'/player/action/'+action)
	      .then(function (response) {
	        console.log("OK: player_action");
	      })
	      .catch(function (error) {
	        console.log("ERROR: player_action");
	        console.log(error);
	      });
		},
		player_mode: function(mode){
	    var self = this;
	    axios.post(self.url_api+'/player/mode/'+mode)
	      .then(function (response) {
	        console.log("OK: player_mode");
					self.player.mode = mode;
	      })
	      .catch(function (error) {
	        console.log("ERROR: player_mode");
	        console.log(error);
	      });

		}
	},

});
