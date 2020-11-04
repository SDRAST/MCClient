var sourceDisplay = {
    props: ["sourceNames", "something"],
    computed:{
        somethingNew: function(){
            return this.something
        }
    },
    template: `<div><ul>
               <li v-for="name in sourceNames">{{name}}</li>
               </ul>
               <h5>{{somethingNew}}</h5>
               </div>`
}
