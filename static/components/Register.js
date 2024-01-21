export default {
  template: `
  <div class='d-flex justify-content-center' style="margin-top: 25vh">
    <div class="mb-3 p-5 bg-light">
        <div class='text-danger'>*{{error}}</div>
        <label for="user-email" class="form-label">Email address</label>
        <input type="email" class="form-control" id="user-email" placeholder="name@example.com" v-model="cred.email">
        <label for="user-password" class="form-label">Password</label>
        <input type="password" class="form-control" id="user-password" v-model="cred.password">
        <label for="user-confirm-password" class="form-label">Confirm Password</label>
        <input type="password" class="form-control" id="user-confirm-password" v-model="cred.Confirmpassword">
        <button class="btn btn-primary mt-2" @click='register' > Register </button>
    </div> 
  </div>
  `,
  data() {
    return {
      cred: {
        email: null,
        password: null,
        Confirmpassword: null,
      },
      error: null,
    }
  },
  methods: {
    async register() {
      if (this.cred.password !== this.cred.Confirmpassword) {
        this.error = 'Passwords do not match'
      }
      else{
        const res = await fetch('/user-register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.cred),
        })
        const data = await res.json()
        if (res.ok) {
          this.$router.push({ path: '/login' })
          alert(data.message)
        } else {
          this.error = data.message
        }
      }
    },
  },
}
