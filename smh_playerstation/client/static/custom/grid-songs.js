// https://vuejs.org/v2/examples/grid-component.html
// register the grid component
Vue.component('demo-grid', {
  template: '#template-grid-songs',
  props: {
    data: Array,
    columns: Array,
    filterKey: String
  },
  data: function () {
    var sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders
    }
  },
  computed: {
    filteredData: function () {
      var sortKey = this.sortKey
      var filterKey = this.filterKey && this.filterKey.toLowerCase()
      var order = this.sortOrders[sortKey] || 1
      var data = this.data
      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
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
    song_to_playlist: function(song_id){
      //Global playlist TODO:change
      playlists.playlists[playlists.selected_id].push(song_id);
    },
    song_to_player: function(song_id){
      //Global playlist TODO:change
      player.playlist.push(song_id);
    }
  },
})
