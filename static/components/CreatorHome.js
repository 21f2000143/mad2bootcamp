export default {
  template: `<div>
      <h1>Welcome Creator {{ email }}</h1> 
      <div class="row">
      <div v-for="(album, index) in albums" :key='index' class="col-sm-6 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ album.title }}</h5>
            <p class="card-text">{{ album.genre }}</p>
            <a href="#" class="btn btn-primary" disabled>Go somewhere</a>
          </div>
        </div>
      </div>
    </div>
  </div> `,
  data() {
    return {
      email: '',
      albums: [],
      authToken: localStorage.getItem('auth-token'),
    }
  },
  methods: {
    async downlodResource() {
      this.isWaiting = true
      const res = await fetch('/download-csv')
      const data = await res.json()
      if (res.ok) {
        const taskId = data['task-id']
        const intv = setInterval(async () => {
          const csv_res = await fetch(`/get-csv/${taskId}`)
          if (csv_res.ok) {
            this.isWaiting = false
            clearInterval(intv)
            window.location.href = `/get-csv/${taskId}`
          }
        }, 1000)
      }
    },
  },
  async mounted() {
    const res = await fetch('/api/album', {
      headers: {
        'Authentication-Token': this.authToken,
      }
    })
    const data = await res.json()
    if (res.ok) {
      this.albums = data
    }
  }
}
