export default {
  template: `
  <div class='d-flex justify-content-center' style="margin-top: 25vh">
    <div class="mb-3 p-5 bg-light">
        <div class='text-danger'>*{{error}}</div>
        <label for="album" class="form-label">album title</label>
        <input type="text" class="form-control" id="album" placeholder="best album" v-model="album.title" required>
        <label for="genre" class="form-label">album genre</label>
        <input type="text" class="form-control" id="genre" v-model="album.genre" required>
        <button class="btn btn-primary mt-2" @click='addAlbum' > Add </button>
    </div> 
  </div>
  `,
  data() {
    return {
      album: {
        title: null,
        genre: null,
      },
      error: null,
      authToken: localStorage.getItem('auth-token')
    }
  },
  methods: {
    async addAlbum() {
      const res = await fetch('/api/album', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': this.authToken,
        },
        body: JSON.stringify(this.album),
      })
      const data = await res.json()
      if (res.ok) {
        this.$router.push({ path: '/' })
        alert(data.message)
      } else {
        this.error = data.message
      }
    },
  },
}
