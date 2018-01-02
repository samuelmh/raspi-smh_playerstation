var player_template = `
<div class="container-fluid ">
	<!-- PLAYER -->
	<div class="btn-group" role="group">
		<div v-if="player.playing_time==-1">
			<button type="button" class="btn btn-light" v-on:click="player_action('play')"><i class="fa fa-play fa-fw"></i></button>
		</div>
		<div v-else>
			<button type="button" class="btn btn-light" v-on:click="player_action('stop')"><i class="fa fa-stop fa-fw"></i></button>
		</div>
		<button type="button" class="btn btn-light" v-on:click="player_action('play_next')"><i class="fa fa-step-forward fa-fw"></i></button>
		<div class="btn-group" role="group">
			<button id="btnGroupDrop1" type="button" class="btn btn-light dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
				Mode <i class="fa fa-fw" :class="{ 'fa-list':player.mode=='LIST', 'fa-repeat':player.mode=='REPEAT_LIST', 'fa-random':player.mode=='RANDOM', 'fa-file-o':player.mode=='REPEAT_FILE'}"></i>
			</button>
			<div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
				<a class="dropdown-item" href="#" v-on:click="player_mode('LIST')"><i class="fa fa-list fa-fw"></i> List</a>
				<a class="dropdown-item" href="#" v-on:click="player_mode('REPEAT_LIST')"><i class="fa fa-repeat fa-fw"></i> Repeat list</a>
				<a class="dropdown-item" href="#" v-on:click="player_mode('RANDOM')"><i class="fa fa-random fa-fw"></i> Random</a>
				<a class="dropdown-item" href="#" v-on:click="player_mode('REPEAT_FILE')"><i class="fa fa-file-o fa-fw"></i> Repeat song</a>
			</div>
		</div>
	</div>
	<br/>
	<!-- PLAYLIST -->
	<ul class="list-group container-fluid list-group-flush" >
		<draggable :list="player.playlist" :options="{handle:'.drag-handle'}" v-on:end="drag_update">
			<li class="list-group-item" :class="{ 'bg-warning': player.position==index }" v-for="(song, index) in player.playlist">
				<div class="row">
					<div class="col-1 drag-handle">
						<i class="fa fa-arrows-v fa-fw"></i>
					</div>
					<div class="col-9">
						{{ song }}
					</div>
					<div class="col-2">
						<button type="button" class="btn btn-link" v-on:click="player_remove_song(index)"><i class="fa fa-remove fa-fw"></i></button>
						<button type="button" class="btn btn-link"><i class="fa fa-play-circle fa-fw"></i></button>
					</div>
				</div>
			</li>
		</draggable>
	</ul>
</div>
`;


Vue.component('smh-playerstation-player', {
  template: player_template,
	props: ['player'],
	methods: {
		player_remove_song: function (song_index){
			this.$emit('player_remove_song', song_index);
		},
		player_action: function(action){
			this.$emit('player_action', action);
		},
		player_mode: function(mode){
			this.$emit('player_mode', mode);
		},
		drag_update: function(){
			this.$emit('drag_update');
		}
	}
});
