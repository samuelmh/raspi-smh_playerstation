var settings_template = `
<div class="container-fluid ">

	<div class="card">
	  <div class="card-header">
	    <h4>Workers</h4>
		</div>
	  <div class="card-body">
			<h5>Database</h5>
			<ul>
				<li><strong>Status:</strong>
						<span v-if="status.workers.db.alive" class="badge badge-success">Alive</span>
						<span v-else class="badge badge-error">Dead</span>
				</li>
				<li><strong>Queue:</strong> {{status.workers.db.queue_size}}</li>
			</ul>
		</div>
		<div class="card-body">
			<h5>Youtube downloader</h5>
			<ul>
				<li><strong>Status:</strong>
						<span v-if="status.workers.youtube_dl.alive" class="badge badge-success">Alive</span>
						<span v-else class="badge badge-error">Dead</span>
				</li>
				<li><strong>Queue:</strong> {{status.workers.youtube_dl.queue_size}}</li>
			</ul>
		</div>
	  <div class="card-body">
			<h5>Encoder</h5>
			<ul>
				<li><strong>Status:</strong>
						<span v-if="status.workers.encoder.alive" class="badge badge-success">Alive</span>
						<span v-else class="badge badge-error">Dead</span>
				</li>
				<li><strong>Queue:</strong> {{status.workers.encoder.queue_size}}</li>
			</ul>
		</div>
	</div>

	</br>
	<div class="card">
	  <div class="card-header">
	    <h4>
				<a data-toggle="collapse" href="#settings_songs_scan" role="button" aria-expanded="true" aria-controls="settings_songs_scan">
					Song collection
				</a>
			</h4>
  		</button>
	  </div>
	  <div class="card-body collapse" id="settings_songs_scan">
			<p>
				<button type="button" class="btn btn-primary" v-on:click="songs_scan"><i class="fa fa-search-plus fa-fw"></i> Find new songs</button>
				<button type="button" class="btn btn-primary" v-on:click="songs_rescan"><i class="fa fa-warning fa-fw"></i> Rescan all</button>
			</p>
	  </div>
	</div>

	</br>
	<div class="card">
	  <div class="card-header">
	    <h4>
				<a data-toggle="collapse" href="#settings_url_api" role="button" aria-expanded="true" aria-controls="settings_url_api">
					Connection to server
				</a>
			</h4>
	  </div>
	  <div class="card-body collapse" id="settings_url_api">
			<form>
			  <div class="form-group">
			    <label for="exampleInputEmail1">URL Endpoint</label>
					<input class="form-control" v-model="url_api" />
			    <small id="emailHelp" class="form-text text-muted">Example: http://localhost:8000/api/v1.0</small>
			  </div>
			  <button class="btn btn-primary" v-on:click="url_api_set">Save</button>
			</form>
	  </div>
	</div>

</div>
`;

Vue.component('smh-playerstation-settings', {
  template: settings_template,
	props: ['url_api', 'status'],
	methods: {
		songs_scan: function(){
			this.$emit('songs_scan', this.url_api);
			$('#settings_songs_scan').collapse('hide');
		},
		songs_rescan: function(){
			this.$emit('songs_rescan', this.url_api);
			$('#settings_songs_scan').collapse('hide');
		},
		url_api_set: function(){
			this.$emit('url_api_set', this.url_api);
			$('#settings_url_api').collapse('hide');
		}
	}
});
