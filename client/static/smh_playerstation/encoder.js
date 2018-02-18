var encoder_template = `
<!-- ENCODER -->
<div class="container-fluid ">
	<form class="container">
		<div class="form-group row">
			<div class="col-1">
				<label class="col-form-label font-weight-bold">Path</label>
			</div>
			<div class="col-11">
				<input name="query" class="form-control" v-model="path" />
			</div>
		</div>

		<div  class="form-group">
			<label class="col-form-label font-weight-bold">Songs</label>
			<ul class="list-group container-fluid list-group-flush" >
				<li class="list-group-item" v-for="(song, index) in song_ids">
					<div class="row">
						<div class="col-9">
							{{ song }}
						</div>
						<div class="col-2">
							<button type="button" class="btn btn-link" v-on:click="remove_song(index)"><i class="fa fa-remove fa-fw"></i></button>
						</div>
					</div>
				</li>
			</ul>
		</div>

		<div class="form-group row">
			<div class="col-1">
				<label class="col-form-label font-weight-bold">Quality</label>
			</div>
			<div class="col-2">
				<select class="form-control" v-model="bitrate">
		      <option>245</option>
		      <option>225</option>
		      <option>190</option>
		      <option>175</option>
		      <option>165</option>
		      <option>130</option>
					<option>115</option>
		      <option>110</option>
		      <option>85</option>
		      <option>65</option>
		    </select>
			</div>
		</div>

		<div class="form-group row">
			<div class="col-1">
				<label class="col-form-label font-weight-bold">Mono</label>
			</div>
			<div class="col-2">
				<input type="checkbox" class="form-check-input" v-model="mono" />
			</div>
		</div>


		<div class="row">
			<div class="col text-right">
				<button type="button" class="btn btn-primary" v-on:click="encode"><i class="fa fa-hdd-o fa-fw"></i> Encode</button>
			</div>
		</div>


		<div class="form-group row">
		</div>


	</div>
</div>
`;


Vue.component('smh-playerstation-encoder', {
  template: encoder_template,
	data: function () {
		return {
			bitrate: "245",
			mono: false
		}
	},
	props: ['song_ids', 'path'],
	methods: {
		remove_song: function (song_index){
			this.$emit('remove_song', song_index);
		},
		encode: function(){
			this.$emit('encoder_encode', this.bitrate, this.mono);
		}
	}
});
