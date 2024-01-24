import StudentHome from './StudentHome.js'
import InstructorHome from './InstructorHome.js'
import AdminHome from './AdminHome.js'
import StudyResource from './StudyResource.js'
import CreatorHome from './CreatorHome.js'

export default {
  template: `<div>
  <StudentHome v-if="userRole=='stud'"/>
  <AdminHome v-if="userRole=='admin'" />
  <InstructorHome v-if="userRole=='inst'" />
  <CreatorHome v-if="userRole=='creator'" />
  <StudyResource v-for="(resource, index) in resources" :key='index' :resource = "resource" />
  <div class="container-fluid text-center">
    <div class="row">
        <div class="col-2 border">
        <nav id="navbar-example3" class="h-100 flex-column align-items-stretch pe-4 border-end">
        <nav class="nav nav-pills flex-column">
            <a class="nav-link" href="#item-1">Item 1</a>
            <nav class="nav nav-pills flex-column">
                <a class="nav-link ms-3 my-1" href="#item-1-1">Item 1-1</a>
                <a class="nav-link ms-3 my-1" href="#item-1-2">Item 1-2</a>
            </nav>
            <a class="nav-link" href="#item-2">Item 2</a>
            <a class="nav-link" href="#item-3">Item 3</a>
            <nav class="nav nav-pills flex-column">
                <a class="nav-link ms-3 my-1" href="#item-3-1">Item 3-1</a>
                <a class="nav-link ms-3 my-1" href="#item-3-2">Item 3-2</a>
            </nav>
        </nav>
    </nav>
        </div>
        <div class="col-8 border">
            <div data-bs-spy="scroll" data-bs-target="#navbar-example3" data-bs-smooth-scroll="true"
                class="scrollspy-example-2" tabindex="0">
                <div id="item-1">
                    <h4>Item 1</h4>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut voluptatem saepe autem id esse incidunt accusantium quidem ex facilis. Corrupti fugiat cupiditate eum. Sunt culpa est nulla unde, dolore laudantium.</p>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut voluptatem saepe autem id esse incidunt accusantium quidem ex facilis. Corrupti fugiat cupiditate eum. Sunt culpa est nulla unde, dolore laudantium.</p>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut voluptatem saepe autem id esse incidunt accusantium quidem ex facilis. Corrupti fugiat cupiditate eum. Sunt culpa est nulla unde, dolore laudantium.</p>
                </div>
                <div id="item-1-1">
                    <h5>Item 1-1</h5>
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
</p>
                </div>
                <div id="item-1-2">
                    <h5>Item 1-2</h5>
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
</p>
                </div>
                <div id="item-2">
                    <h4>Item 2</h4>
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
</p>
                </div>
                <div id="item-3">
                    <h4>Item 3</h4>
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
</p>
                </div>
                <div id="item-3-1">
                    <h5>Item 3-1</h5>
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
</p>
                </div>
                <div id="item-3-2">
                    <h5>Item 3-2</h5>
                    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Necessitatibus aspernatur odio voluptatum sapiente quisquam minima accusantium! Nesciunt quasi beatae, dolorem architecto iste neque quod blanditiis facilis quibusdam similique quisquam reiciendis!
</p>
                </div>
            </div>
        </div>
    </div>
    <div class="col-2 border">
        
    </div>
</div>
</div>
  </div>`,

  data() {
    return {
      userRole: localStorage.getItem('role'),
      authToken: localStorage.getItem('auth-token'),
      resources: [],
    }
  },

  components: {
    StudentHome,
    InstructorHome,
    AdminHome,
    StudyResource,
    CreatorHome
  },
  async mounted() {
    const res = await fetch('/api/study_material', {
      headers: {
        'Authentication-Token': this.authToken
      },
    })
    const data = await res.json()
    if (res.ok) {
      this.resources = data
    } else {
      alert(data.message)
    }
  },
}
