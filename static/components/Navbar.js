export default {
  template: `
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Live Session</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
        </li>
        <li class="nav-item" v-if="role==null">
          <router-link class="nav-link" aria-current="page" to="/login">Login</router-link>
        </li>
        <li class="nav-item" v-if="role==null">
          <router-link class="nav-link" aria-current="page" to="/register">Register As Student</router-link>
        </li>
        <li class="nav-item" v-if="role==null">
          <router-link class="nav-link" aria-current="page" to="/creator">Register As Creator</router-link>
        </li>
        <li class="nav-item" v-if="role=='admin'">
          <router-link class="nav-link" to="/users">Users</router-link>
        </li>
        <li class="nav-item" v-if="role=='stud'">
          <router-link class="nav-link" to="/create-resource">Create Resource</router-link>
        </li>
        <li class="nav-item" v-if="role=='creator'">
          <router-link class="nav-link" to="/create-album">Add Album</router-link>
        </li>
        <li class="nav-item" v-if="is_login">
          <button class="nav-link" @click='logout' >logout</button>
        </li>
      </ul>
    </div>
  </div>
</nav>`,
  data() {
    return {
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token'),
    }
  },
  methods: {
    async logout() {
        const res = await fetch('/user-logout', {
          headers: {
            'Authentication-Token': this.is_login,
            'Content-Type': 'application/json',
          },
        })
        const data = await res.json()
        console.log(data)
        if (res.ok) {
          localStorage.removeItem('auth-token')
          localStorage.removeItem('role')
          this.$router.push({ path: '/login' })
        } else {
          alert(data.message)
        }
    },
  },
}
