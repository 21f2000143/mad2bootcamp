const CreateCatCompo = Vue.component('CreateCatCompo', {
  template: `
  <div class="row justify-content-center m-3 text-color-light">
  <div class="card bg-light" style="width: 18rem;">
    <div class="card-body">
    <div class="d-flex justify-content-end">
      <!-- Cross button to close the card -->
      <button type="button" class="btn-close" aria-label="Close" @click="closeCard"></button>
    </div>
      <h5 class="card-title">Add Category</h5>
      <form @submit.prevent="addcategory">
        <div class="mb-3">
        <label for="name" class="form-label">Category Name</label>
        <input type="text" class="form-control" v-model="name" required>
          <div v-if="message" class="alert alert-warning">
            {{message}}
          </div>
        </div>
        <button type="submit" class="btn btn-outline-primary">Add</button>
      </form>
    </div>
  </div>
</div>
    `,
  data() {
    return {
      name:'',
      message: ''
    }
  },
  methods: {
    closeCard(){
      if(this.$store.state.authenticatedUser.role==='admin'){
        if(this.$route.path!='/admin'){
          this.$router.push('/admin')
        }
      }
      else{
        if(this.$route.path!='/manager'){
          this.$router.push('/manager')
        }
      }
    },
    async addcategory() {
      try {
        const response = await fetch('http://127.0.0.1:5000/add/cat',{
          method: 'POST',
          headers: {
            
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.name
          }),
        });
        if (response.status === 201) {
          const data = await response.json();
          console.log(data.resource)
          if(this.$store.state.authenticatedUser.role==='admin'){
            this.$store.commit('addCat', data.resource)
          }
          else{
            this.$store.commit('addNoti', data.resource)
          }          
          this.closeCard()
        } else {
          alert(data.message);
        }
      } catch (error) {
        console.error(error);
      }
    }
  },
})
export default CreateCatCompo;