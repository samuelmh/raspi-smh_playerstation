// https://vuejs.org/v2/examples/grid-component.html

var download_ytb_template = `
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
			<div class="form-group">
    		<label for="ytb_ids" class="font-weight-bold">Ids</label>
    		<textarea class="form-control" v-model="ytb_ids" rows="10"></textarea>
			</div>
	    <div class="row">
        <div class="col text-right">
					<button type="button" class="btn btn-primary" v-on:click="download"><i class="fa fa-download fa-fw"></i> Download</button>
				</div>
	    </div>
		</form>
	</div>
`;


Vue.component('smh-playerstation-download_ytb', {
  template: download_ytb_template,
	data: function () {
		return {
			path: "",
			ytb_ids: "",
		}
	},
	props:['url_api'],
	methods: {
		download: function(){
			var self = this;
			console.log(self.path);
			console.log(self.ytb_ids);
	    axios.post(
				self.url_api+'/songs/youtube/download',
				{path:self.path, youtube_ids: self.ytb_ids}
			).then(function (response) {
        console.log("OK: download_ytb");
				self.$emit('downloading');
      }).catch(function (error) {
        console.log("ERROR: download_ytb");
        console.log(error);
      });
		}
	}
});
