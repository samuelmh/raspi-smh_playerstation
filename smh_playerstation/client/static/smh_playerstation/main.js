// Root instance

var smh_playerstation = new Vue({
	el: '#smh_playerstation',
	data: {
	    url_api: 'http://localhost:8000'+'/api/v1.0',
			playlists: [],
			playlist_selected_id: "tmp",
	    songs: [],  //Tuples of songs
			songs_index: {},  // Index over the songs titles
			player: {mode:'LIST', playlist:[]},  // Don't bind an empty playlist
			status: {},
			encoder_songs: [],
			encoder_path: ''
	  },
  methods: {

		//==> SONG Utilities
		song_filter_title: function(path_file){
  		var elems = path_file.split("/").pop().split("-");
  		elems.pop();
  		return elems.join();
    },
		song_filter_length: function (seconds){
			function pad(num, size){ return ('00' + num).substr(-size); }
			seconds = Number(seconds)
			return Math.floor(seconds/3600) + ":" + pad(Math.floor((seconds%3600)/60),2) + ":" + pad(Math.floor(seconds%60),2)
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
							response.data[key]['LENGTH_HMS'] = self.song_filter_length(response.data[key]['LENGTH']);
              self.songs_index[key] = response.data[key];
              return response.data[key];
            }
          );
        })
        .catch(function (error) {
          console.log("ERROR: songs_get");
          console.log(error);
        });
    },
		songs_scan: function(){
      var self = this;
      axios.get(self.url_api+'/songs/scan')
        .then(function (response) {
					console.log("OK: songs_scan");
					self.to_status();
        })
        .catch(function (error) {
          console.log("ERROR: songs_scan");
          console.log(error);
        });
		},
		songs_rescan: function(){
      var self = this;
      axios.get(self.url_api+'/songs/rescan')
        .then(function (response) {
					console.log("OK: songs_rescan");
					self.to_status();
        })
        .catch(function (error) {
          console.log("ERROR: songs_rescan");
          console.log(error);
        });
		},

		// ENCODER
		encoder_encode: function(bitrate, mono){
			console.log(bitrate);
			console.log(mono);
			console.log(this.encoder_path);
			var self = this;
      axios.post(
				self.url_api+'/songs/encode',
				{
					song_ids: self.encoder_songs,
					path: self.encoder_path,
					bitrate: bitrate,
					mono: mono
				}
			).then(function (response) {
				console.log("OK: encoder_encode");
				self.to_status();
				self.encoder_songs = [];
      }).catch(function (error) {
        console.log("ERROR: encoder_encode");
        console.log(error);
      });
		},
		encoder_add_songs: function(song_ids){
			this.encoder_songs = this.encoder_songs.concat(song_ids);
		},
		encoder_remove_song: function(song_index){
			Vue.delete(this.encoder_songs, song_index);
		},
		encoder_set_path: function(path){
			this.encoder_path = path;
			this.to_encoder();
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
					if (self.player["playing_time"]!=-1) {
						// TODO: interface timer is better
						// playing time, song time,
						// setTimeout(self.player_get, 1000);  // If playing update status
					}
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
					self.player_get();
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

		},


		//
		//==> OTHERS
		//
		to_encoder:function(){
			$('#tabs a[href="#encoder"]').tab('show');  // See workers
		},
		to_status: function(){
			$('#tabs a[href="#settings"]').tab('show');  // See workers
			setTimeout(self.status_get, 3000);
		},
		update_data: function(){
			smh_playerstation.songs_get();
      smh_playerstation.playlists_get();
      smh_playerstation.player_get();
		},
		url_api_set: function(url_api){
			this.url_api = url_api;
		},
		status_get: function(){ //Update the workers status until queues==0
	    var self = this;
	    axios.get(self.url_api+'/status')
	      .then(function (response) {
	        console.log("OK: status_get");
	        self.status = response.data;
					var workers = self.status.workers;
					var repeat = false;
					for (var worker in workers) {
		  			if (workers[worker]['queue_size']>0){
							repeat = true;
							break;
						}
					}
					if (repeat){
						setTimeout(self.status_get, 1000);
					} else {  //Update playlists/songs
						self.update_data();
					}
	      })
	      .catch(function (error) {
	        console.log("ERROR: status_get");
	        console.log(error);
					setTimeout(self.status_get, 3000);
	      });
		},
},


});
